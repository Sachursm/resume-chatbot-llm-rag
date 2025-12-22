# Query Normalization
def normalize_query(query: str) -> str:
    query = query.lower()
    query = query.replace("are you", "")
    query = query.replace("?", "")
    return query.strip()
