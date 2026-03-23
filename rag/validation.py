import json, os, re, ast,builtins


from pandas.core.dtypes.inference import is_decimal




class C_validate():
    def rag_validate(self, value,value2):
        lst = {
            "json-result": {"summaries-about-the-Document": "This document contains information about a personal user ID ticket booking on a train, with details such as the train number and PNR. It also includes contact information for customer care regarding e-ticket booking, cancellation, and refund assistance."}
        }
        for i in value.MCP['Field']:
            if i not in lst['json-result'].keys():
                value.missed.append(i)
            else:
                for j in value.MCP["Field-constraints"][i].keys():
                    if j.value !="Alpha-numeric" and j.value !="decimal" and j.value >=0:
                        if not isinstance(lst['json-result'][i],getattr(builtins,value.MCP["Field-constraints"][i][j].value)):
                            value.failed_validation.append(i)
                        elif j.value =="Alpha-numeric":
                            if not isalnum(lst[i]):
                                value.failed_validation.append(i)
                        elif j.value =='decimal':
                            if not is_decimal(lst[i]):
                                value.failed_validation.append(i)
                        elif j.value =='min_length' or j=='max_length':
                                if 'min_length' in value.MCP["Field-constraints"][i].keys() and 'max_length' in lst.value.MCP["Field-constraints"][i].keys():
                                    if not len(str(lst[i])) > value.MCP["Field-constraints"][i]['min_length'].value and len(str(lst[i])) < value.MCP["Field-constraints"][i]['max_length'].value:
                                        value.failed_validation.append(i)
                        elif j.value =='min_length':
                            if not len(str(lst[i]))>=value.MCP["Field-constraints"][i][j]:
                                value.failed_validation.append(i)
                        elif j.value =='max_length':
                            if not len(str(lst[i]))<=value.MCP["Field-constraints"][i][j]:
                                value.failed_validation.append(i)
        return value

