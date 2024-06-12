from abc import ABC, abstractmethod

from injector import inject

from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
    QueryRowResult,
    QueryResult,
)
from griff.services.query_runner.query_runner_service import QueryRunnerService


class DbDomainPersistence(DomainPersistence, ABC):
    @inject
    def __init__(self, query_runner_service: QueryRunnerService):
        self._query_runner_service = query_runner_service
        self._query_runner_service.set_sql_queries(
            self._get_relative_sql_queries_path()
        )

    async def insert(self, data: dict) -> None:
        await self.run_query(query_name="insert", **data)

    async def update(self, data: dict) -> None:
        await self.run_query(query_name="update", **data)

    async def delete(self, persistence_id: str) -> None:
        await self.run_query(query_name="delete", entity_id=persistence_id)

    async def get_by_id(self, persistence_id: str) -> QueryRowResult:
        return await self.run_query(query_name="get_by_id", entity_id=persistence_id)  # type: ignore # noqa: E501

    async def run_query(self, query_name, **query_params) -> QueryResult:
        return await self._query_runner_service.run_query(query_name, **query_params)

    @abstractmethod
    def _get_relative_sql_queries_path(self) -> str:  # pragma: no cover
        pass
