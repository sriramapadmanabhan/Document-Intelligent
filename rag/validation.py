import json, os, re, ast,builtins
from curses.ascii import isalnum

from pandas.core.dtypes.inference import is_decimal


class C_validate():
    def rag_validate(self, value,value2):
        match = re.search(r"json-result(\{.*\})", value.rag_result, re.DOTALL)
        if match is None:
            exit()
        lst = json.loads(match.group(1)).keys()
        for i in value.MCP['Field']:
            if i not in lst:
                value.missed.append(i)
            else:
                for j in value.MCP["Field-constraints"][i].keys():
                    if j !="Alpha-numeric" and j!="decimal":
                        if not isinstance(lst[i],getattr(builtins,value.MCP["Field-constraints"][i][j])):
                            value.failed_validation.append(i)
                        elif j =="Alpha-numeric":
                            if not isalnum(lst[i]):
                                value.failed_validation.append(i)
                        elif j=='decimal':
                            if not is_decimal(lst[i]):
                                value.failed_validation.append(i)
                        elif j=='min_length' or j=='max_length':
                                if 'min_length' in value.MCP["Field-constraints"][i].keys() and 'max_length' in lst.value.MCP["Field-constraints"][i].keys():
                                    if not len(str(lst[i])) > value.MCP["Field-constraints"][i]['min_length'] and len(str(lst[i])) < value.MCP["Field-constraints"][i]['max_length']:
                                        value.failed_validation.append(i)
                        elif j=='min_length':
                            if not len(str(lst[i]))>=value.MCP["Field-constraints"][i][j]:
                                value.failed_validation.append(i)
                        elif j=='max_length':
                            if not len(str(lst[i]))<=value.MCP["Field-constraints"][i][j]:
                                value.failed_validation.append(i)

