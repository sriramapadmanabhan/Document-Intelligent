import json, os, re, ast,builtins
from datetime import datetime
from pandas.core.dtypes.inference import is_decimal


class C_validate():

    def rag_validate(self, value,value2):
        f_validator = {'str': lambda x: isinstance(x, str), 'Alpha-numeric': lambda x: bool(re.match(r"^[a-zA-Z0-9 \-]+$", str(x))),
                       'decimal': lambda x:bool(re.match(r'^\d+\.\d+$', str(x))), 'int': lambda x: isinstance(x, int),
                       'Date_time':lambda x:isinstance(x,datetime)}
        max_len=lambda x,y:len(str(x))<y
        min_len = lambda x, y: len(str(x)) > y
        lst = {"json-result": {"summaries-about-the-Document": "This document contains information about a personal user ID ticket booking on a train, with details such as the train number and PNR. It also includes contact information for customer care regarding e-ticket booking, cancellation, and refund assistance."}}
        for i in value.MCP['Field']:
            if i not in lst['json-result'].keys():
                value.missed.append(i)
            else:
                for j in value.MCP["Field-constraints"][i].keys():
                    if j =="type":
                            if not f_validator[value.MCP["Field-constraints"][i][j]](lst['json-result'][i]):
                                value.failed_validation.append(i)

                    if j=='max_length':
                        if not max_len(lst['json-result'][i],value.MCP["Field-constraints"][i][j]):
                            value.failed_validation.append(i)

                    if j=='min_length':
                        if not min_len(lst['json-result'][i],value.MCP["Field-constraints"][i][j]):
                            value.failed_validation.append(i)
        return value

