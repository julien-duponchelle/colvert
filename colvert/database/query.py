import re

AUTO_RUN_DISALLOWED = [
    "COPY",
    "CREATE",
    "DELETE",
    "DROP",
    "EXPORT",
    "INSERT",
    "UPDATE",
    "ALTER",
    "IMPORT",
    "INSTALL",
    "LOAD",
]


class Query:
    def __init__(self, query: str) -> None:
        self._query = query

    def __str__(self) -> str:
        return self._query

    def auto_runnable(self) -> bool:
        pattern = re.compile(
            "^.*(" + "|".join(AUTO_RUN_DISALLOWED) + ").*$",
            re.IGNORECASE + re.MULTILINE,
        )
        return re.match(pattern, self._query) is None
