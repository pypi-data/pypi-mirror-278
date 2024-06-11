from abc import ABC, abstractmethod
from typing import List

QueryRowResult = dict | None
QueryRowResults = List[QueryRowResult]

QueryResult = QueryRowResult | QueryRowResults


class DomainPersistence(ABC):
    @abstractmethod
    async def insert(self, data: dict) -> None:  # pragma: no cover
        ...

    @abstractmethod
    async def update(self, data: dict) -> None:  # pragma: no cover
        ...

    @abstractmethod
    async def delete(self, persistence_id: str) -> None:  # pragma: no cover
        ...

    @abstractmethod
    async def get_by_id(
        self, persistence_id: str
    ) -> QueryRowResult:  # pragma: no cover
        ...

    @abstractmethod
    async def run_query(
        self, query_name: str, **query_params
    ) -> QueryResult:  # pragma: no cover
        ...
