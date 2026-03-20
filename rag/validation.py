import json, os, re, ast

class C_validate():
    def rag_validate(self, value):
        match = re.search(r"json-result(\{.*\})", value['rag_result'], re.DOTALL)
        if match is None:
            exit()
        elif value.get('ntry') <= 3:
            value['ntry'] = 1 if value.get('ntry') is None else value['ntry'] + 1
            validation = {type: {("int", "integer", "int()", "integer"): int, ('str', 'string', 'text'): str}}
            value.setdefault('rag_status', {}).setdefault(value['current_rag'], {}).setdefault(value['ntry'],
                                                                                               {value['ntry']})
            lst = json.loads(match.group(1)).keys()
            for i in value['MCP']['Field']:
                if i not in lst:
                    if validation.get('missed') is not None:
                        validation['missed'].append(i)
                    else:
                        validation['missed'] = [i]
                else:
                    if validation.get('available') is not None:
                        validation['available'].append(i)
                    else:
                        validation['available'] = [i]

            value['rag_status']['current_rag']['ntry'].defaultdict([value['ntry']], {})
            value['rag_status']['current_rag']['ntry']['missed'] = validation['missed']
            value['rag_status']['current_rag']['ntry']['available'] = validation['available']
            if value['MCP']['Field-constraints'] is not None:
                for i in value['MCP']['Field']:
                    if i in value['MCP']['Field-constraints'].keys():
                        for j in validation['type'].keys():
                            if i in j:
                                if type(i) is validation['type'][j]:
                                    value['rag_status']['current_rag']['ntry'].setdefault("constraint_success", []).append(
                                        i)
                                else:
                                    value['rag_status']['current_rag']['ntry'].setdefault("constraint_failure", []).append(
                                        i)

        return value