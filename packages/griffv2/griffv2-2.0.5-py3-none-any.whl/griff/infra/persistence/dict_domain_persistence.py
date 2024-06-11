import re
from typing import Dict, List

from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
    QueryRowResult,
    QueryResult,
)


class DictDomainPersistence(DomainPersistence):
    _default_queries = {"list_all": lambda data: list(data.values())}

    def __init__(
        self,
        initial_data: List[Dict] | None = None,
        queries: Dict | None = None,
    ):
        self._internal_storage: Dict[str, Dict] = {}
        self._queries: Dict = (
            {**self._default_queries, **queries} if queries else self._default_queries
        )
        self.reset(initial_data)

    async def insert(self, data: dict) -> None:
        if data["entity_id"] not in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' already exists")

    async def update(self, data: dict) -> None:
        if data["entity_id"] in self._internal_storage:
            self._internal_storage[data["entity_id"]] = data
            return None
        raise ValueError(f"id '{data['entity_id']}' does not exists")

    async def delete(self, persistence_id: str) -> None:
        if persistence_id in self._internal_storage:
            self._internal_storage.pop(persistence_id)
            return None
        raise ValueError(f"id '{persistence_id}' does not exists")

    async def get_by_id(self, persistence_id: str) -> QueryRowResult:
        if persistence_id in self._internal_storage:
            return self._internal_storage[persistence_id]
        raise ValueError(f"id '{persistence_id}' not found")

    async def run_query(self, query_name: str, **query_params) -> QueryResult:
        if self._queries and query_name in self._queries:
            return self._queries[query_name](self._internal_storage, **query_params)
        result = self._try_get_by_query(query_name, **query_params)
        if result is not False:
            return result
        raise RuntimeError(f"Query {query_name} not found")

    def reset(self, initial_data: List[Dict] | None = None):
        if initial_data is None:
            self._internal_storage = {}
            return None
        self._internal_storage = {e["entity_id"]: e for e in initial_data}

    def _try_get_by_query(self, query_name: str, **query_params):
        pattern = r"^get_by_([a-z_]+)$"
        match = re.match(pattern, query_name)
        if not match:
            return False
        attr_name = match.group(1)
        search = query_params.get(attr_name)
        for e in self._internal_storage.values():
            if e.get(attr_name) == search:
                return e
        return None
