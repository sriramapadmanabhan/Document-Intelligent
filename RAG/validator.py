import re
import json


def validate(value):

    match = re.search(r"\{.*\}", value.rag_result, re.DOTALL)

    if not match:
        return value

    parsed = json.loads(match.group())

    missing = []
    available = []

    for field in value.field:
        if field in parsed:
            available.append(field)
        else:
            missing.append(field)

    value.rag_status = {
        "missing": missing,
        "available": available
    }

    return value