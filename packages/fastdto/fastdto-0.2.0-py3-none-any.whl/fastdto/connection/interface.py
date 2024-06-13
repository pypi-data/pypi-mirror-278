from typing import Protocol


class IAsyncExecutor(Protocol):
    """General interface for user code executor."""

    async def execute(self, query: str, **params) -> list[tuple]:
        """Single method to execute query.

        Note that order of elements in tuple `must` be
        similar to columns in query SELECT statement
        if it has ones.

        !WARNING!
        Also note that if your query has some parameters and you use
        custom executor, you need to handle sql injections on your own.

        Args:
            query (str): String that contains SQL query

        Returns:
            list[tuple]: List that contains result of query if it has result.
        """
        ...
