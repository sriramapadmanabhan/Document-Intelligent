import subprocess
import json, os, re, ast
from rag.models import Metadata,semantic_metadata,Rag_status,cons_type
from rag.retriever import C_retrieve

class C_mcp():
    def create_MCP(self, value,value2):
        value = self.rag_instructions(value,value2)
        MCP = {"Task": value.task ,"Field": value.field ,"Field-constraints": value.constraints,"context": value.context ,"Rules": value.rules}
        value.MCP = MCP
        value =self.RAG(value)
        return value

    # ---------------- SUMMARY MODE ----------------
    def rag_instructions(self, value,value2):
        if value2.current_rag =='summary':
            value.task = "summaries the Document"
            value.field = ['summaries-about-the-Document','Document about']
            value.rules = f"""
                        1) Retrieve only values in this list {value.field}, 
                        2) Remove unwanted other text
                        3) output format is strictly json only
                        4) Naming the json output as 'json-result'
                        5) No Explanation required in output
                        6) Format=json-result:key:value or None
                        7) Key is always any one of the Field name 
                        8) Do not skip key if not found
                        9) 'Document about' answer only from this given list [Railways,Lab-result,Bus-ticket]"""

            value.constraints = {"summaries-about-the-Document": {cons_type.type.value: cons_type.string.value, cons_type.max_length.value: 10}}

        elif value2.current_rag =='Railways':
            value.task = "Extract Railways Field"
            value.field = ['PNR , Passenger Name', 'sex', 'boarding station', 'destination station',
                           'depature date and time', 'arrival date and time',
                           'Train number', 'train name', 'bookind date and time', 'quota', 'distance',
                           'coach number', 'seat number',
                           'Seat confirm or not', 'Total amount paid', 'Total GST paid']
            value.constraints = {"PNR": {cons_type.type.value: cons_type.Integer.value, cons_type.min_length.value: 5, cons_type.max_length.value: 12,
                                         cons_type.location.value: "we can expect near to Name of the Passenger"},
                                 "Name": {cons_type.type.value: cons_type.string.value, cons_type.min_length.value: 3, cons_type.max_length.value: 30},
                                 "sex": {cons_type.type.value: cons_type.string.value, cons_type.alias.value: "gender"},
                                 "boarding station": {cons_type.type.value: cons_type.string.value, cons_type.max_length.value: 4},
                                 "destination station": {cons_type.type.value: cons_type.string.value, cons_type.max_length.value: 4},
                                 "arrival date and time": {cons_type.type.value:cons_type.Date_time.value,
                                                           cons_type.location: "under To-station or Destination station"},
                                 "any proof to take while traveling": {cons_type.alias.value: ["document", "card"]},
                                 "emergency-contact": {cons_type.alias.value: 'Enquiries'}, cons_type.alias.value: ["Enquiry", "help"],
                                 "seat number": {cons_type.type.value: cons_type.Numeric.value, cons_type.max_length.value: 4},
                                 'coach number': {cons_type.type.value: cons_type.Alpha_numeric.value, cons_type.max_length.value: 4},
                                 'Total amount paid': {cons_type.type.value: cons_type.decimal.value,cons_type.location.value: "payment related details"},"distance": {cons_type.type.value: cons_type.Integer.value}}
            value.rules = f"""
                        1) Retrieve only values in this list {value.field}, 
                        2) Remove unwanted other text
                        3) output format is strictly json only
                        4) Naming the json output as 'json-result'
                        5) No Explanation required in output
                        6) Format=json-result:key:value or None
                        7) Key is always any one of the Field name 
                        8) Do not skip key if not found"""

        if not value.field is None and len(value.field) > 0:
            C_R=C_retrieve()
            question_chunk = C_R.retrieve_context(value.field, value)
            print('\n'.join(question_chunk))
            context = '\n'.join(question_chunk)
            value.context = context
        else:
            exit()
        return value

    # ---------------- LLM CALL ----------------
    def RAG(self, value):
        prompt = f"""Role : You are a experienced content summarizer and extractor in few words based on MCP given
                    {json.dumps(value.MCP, indent=2)}"""
        value.rag_result = subprocess.run(["ollama", "run", "mixtral", prompt] ,capture_output=True,text=True).stdout.strip()
        print(value.rag_result)
                                             

        return value