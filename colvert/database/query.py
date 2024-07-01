DISALLOWED = ["CREATE", "INSERT", "UPDATE", "DELETE"]

class Query():
    def __init__(self, query: str) -> None:
        self._query = query

    def __str__(self) -> str:
        return self._query
    
    def auto_runnable(self) -> bool:
        query = self._query.upper()
        for word in DISALLOWED:
            if word in query:
                return False
        return True