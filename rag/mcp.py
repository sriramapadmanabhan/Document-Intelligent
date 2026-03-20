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
            value.field = ['summaries-about-the-Document']
            value.rules = f"""
                        1) Retrieve only values in this list {value.field}, 
                        2) Remove unwanted other text
                        3) output format is strictly json only
                        4) Naming the json output as 'json-result'
                        5) No Explanation required in output
                        6) Format=json-result:key:value or None
                        7) Key is always any one of the Field name 
                        8) Do not skip key if not found"""

        elif value2.current_rag =='Railways':
            value.task = "Extract Railways Field"
            value.field = ['PNR , Passenger Name', 'sex', 'boarding station', 'destination station',
                           'depature date and time', 'arrival date and time',
                           'Train number', 'train name', 'bookind date and time', 'quota', 'distance',
                           'coach number', 'seat number',
                           'Seat confirm or not', 'Total amount paid', 'Total GST paid']
            value.constraints = {"PNR": {cons_type.type: "Integer", cons_type.min_length: 5, cons_type.max_length: 12,
                                         cons_type.location: "we can expect near to Name of the Passenger"},
                                 "Name": {cons_type.type: "String", cons_type.min_length: 3, cons_type.max_length: 30},
                                 "sex": {cons_type.type: "string", cons_type.alias: "gender"},
                                 "boarding station": {cons_type.type: "string", cons_type.max_length: 4},
                                 "destination station": {cons_type.type: "string", cons_type.max_length: 4},
                                 "arrival date and time": {cons_type.type: "Date and time",
                                                           cons_type.location: "under To-station or Destination station"},
                                 "any proof to take while traveling": {cons_type.alias: ["document", "card"]},
                                 "emergency-contact": {cons_type.alias: 'Enquiries'}, cons_type.alias: ["Enquiry", "help"],
                                 "seat number": {cons_type.type: "Numeric", cons_type.max_length: 4},
                                 'coach number': {cons_type.type: "Alpha-numeric", cons_type.max_length: 4},
                                 'Total amount paid': {cons_type.type: "decimal"
                                                       ,cons_type.location: "payment related details"},
                                 "distance": {cons_type.type: "integer"}}
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
        value['rag_result'] = subprocess.run(["ollama", "run", "mixtral", prompt] ,capture_output=True
                                             ,text=True).stdout.strip()

        return value