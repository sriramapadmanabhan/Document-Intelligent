import re
from datetime import datetime

class C_validate():
    def rag_validate(self, value,value2):
        value.missed=[]
        value.failed_validation=[]
        f_validator = {'str': lambda x: isinstance(x, str), 'Alpha-numeric': lambda x: bool(re.match(r"^[a-zA-Z0-9 \-]+$", str(x))),
                       'decimal': lambda x:bool(re.match(r'^\d+\.\d+$', str(x))), 'int': lambda x: isinstance(x, int),
                       'Date_time':lambda x:isinstance(x,datetime)}

        max_len=lambda x,y:len(str(x))<y
        min_len = lambda x, y: len(str(x)) > y

        for i in value.MCP['Field']:
            if i not in value.rag_result.keys():
                value.missed.append(i)
                value.log.info({'retry-count':value.retry_count,'missed':1})
            else:
                if value.MCP.get("Field-constraints").get(i) is not None:
                    for j in value.MCP["Field-constraints"][i].keys():
                        if j =="type" and f_validator.get(value.MCP["Field-constraints"][i][j]) is not None:
                                if not f_validator.get(value.MCP["Field-constraints"][i][j])(value.rag_result[i]):
                                    value.failed_validation.append(i)
                                    value.log.info({'parameter_name':i,'retry-count': value.retry_count, 'cons_name': j,'failed_value':value.MCP["Field-constraints"][i][j]})

                    if j=='max_length':
                        if not max_len(value.rag_result[i],value.MCP["Field-constraints"][i][j]):
                            value.failed_validation.append(i)
                            value.log.info({'parameter_name':i,'retry-count': value.retry_count, 'cons_name': j,'failed_value': value.MCP["Field-constraints"][i][j]})

                    if j=='min_length':
                        if not min_len(value.rag_result[i],value.MCP["Field-constraints"][i][j]):
                            value.failed_validation.append(i)
                            value.log.info({'parameter_name':i,'retry-count': value.retry_count, 'cons_name': j,'failed_value': value.MCP["Field-constraints"][i][j]})
        return value

