def check_substring(result: str, query: str) -> bool:
    result = result.lower().replace(" ", "")
    query = query.lower().replace(" ", "")
    return result in query or query in result


def check_string(result: str, query: str) -> bool:
    result = result.lower().replace(" ", "")
    query = query.lower().replace(" ", "")
    return result == query
