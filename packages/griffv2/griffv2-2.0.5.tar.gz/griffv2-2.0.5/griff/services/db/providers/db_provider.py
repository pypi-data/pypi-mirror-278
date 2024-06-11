import abc
from contextlib import asynccontextmanager
from typing import List, TypeVar, Generic, Dict

C = TypeVar("C")


class DbProvider(Generic[C], abc.ABC):
    @abc.abstractmethod
    async def start(self) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def stop(self) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def get_connection(self) -> C:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def close_connection(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def execute(
        self, connection: C, sql: str | List[str]
    ) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def fetch_one(self, connection: C, sql) -> Dict:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def fetch_all(self, connection: C, sql) -> List:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def start_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def commit_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    async def rollback_transaction(self, connection: C) -> None:  # pragma: no cover
        ...

    @abc.abstractmethod
    @asynccontextmanager
    async def transaction(self, connection):  # pragma: no cover
        ...
