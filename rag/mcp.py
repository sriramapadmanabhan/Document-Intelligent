from rag.models import cons_type
from rag.retriever import C_retrieve
from openai import OpenAI

class C_mcp():

    def create_MCP(self, value,value2):
        value = self.rag_instructions(value,value2)
        MCP = {"Task": value.task ,"Field": value.field ,"Field-constraints": value.constraints,"context": value.context ,"Rules": value.rules}
        value.MCP = MCP
        return value

    def rag_instructions(self, value,value2):
        if value2.current_rag =='summary':
            value.task = "summaries the Document"
            if len(value.missed) > 0 or len(value.failed_validation) > 0:
                value.missed.extend(value.failed_validation)
                value.field =value.missed
            else:
                value.field = ['summaries the Document','Document category']
            value.rules = """
            1) Output must be valid JSON
            2) Use EXACT field names as keys
            3) Do not rename keys
            4) Do not add prefixes
            5) If value missing return null
            6) Category must be one of:
               ['Railways','hospital','Tax']
            """
            value.constraints = {"summaries the Document": {cons_type.type.value: cons_type.string.value, cons_type.max_length.value: 1000},
                                 "Document category":{cons_type.type.value: cons_type.string.value}}

        elif value2.current_rag =='Railways':
            value.task = "Extract Railways Field"
            if len(value.missed) > 0 or len(value.failed_validation) > 0:
                value.missed.extend(value.failed_validation)
                value.field =value.missed
            else:
                value.field=['PNR' , 'Name', 'sex', 'boarding station', 'destination station',
                           'depature date and time', 'arrival date and time',
                           'Train number', 'train name', 'booking date and time', 'quota', 'distance',
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
                        1) Output must be valid JSON
                        2) Use EXACT field names as keys
                        3) Do not rename keys
                        4) Do not add prefixes
                        5) If value missing return null """

        if not value.field is None and len(value.field) > 0:
            C_R=C_retrieve()
            question_chunk = C_R.retrieve_context(value.field, value)
            #print('\n'.join(question_chunk))
            context = '\n'.join(question_chunk)
            value.context = context
        else:
            exit()
        return value
