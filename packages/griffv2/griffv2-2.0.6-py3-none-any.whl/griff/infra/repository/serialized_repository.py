from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from injector import inject

from griff.domain.common_types import Aggregate
from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
)
from griff.infra.repository.repository import Repository
from griff.services.date.date_service import DateService
from griff.services.json.json_service import JsonService

A = TypeVar("A", bound=Aggregate)


class SerializedRepository(Generic[A], Repository[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: DomainPersistence,
        date_service: DateService,
        json_service: JsonService,
    ):
        super().__init__(persistence, date_service)
        self._json_service = json_service

    def _serialize_for_persistence(self, aggregate: A) -> dict:
        return {
            "entity_id": aggregate.entity_id,
            "serialized": self._get_serialized(aggregate),
        }

    def _get_serialized(self, aggregate: A) -> str:
        json_prepared = self._json_service.to_json_dumpable(aggregate.model_dump())
        return self._json_service.dump(json_prepared)

    def _convert_to_hydratation_dict(self, results: dict) -> dict:
        return self._json_service.load_from_str(results["serialized"])
