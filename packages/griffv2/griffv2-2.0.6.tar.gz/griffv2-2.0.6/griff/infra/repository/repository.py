from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from injector import inject
from pydantic import ValidationError

from griff.domain.common_types import Aggregate
from griff.infra.persistence.domain_persistence import (
    DomainPersistence,
)
from griff.services.date.date_service import DateService
from griff.utils.exceptions import EntityNotFoundException

A = TypeVar("A", bound=Aggregate)


class Repository(Generic[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        persistence: DomainPersistence,
        date_service: DateService,
    ):
        self._date_service = date_service
        self._persistence = persistence

    async def get_by_id(self, entity_id: str) -> A | None:
        raw_data = await self._get_by_id(entity_id)
        if raw_data is not None:
            return self._hydrate_result(raw_data)

        raise EntityNotFoundException(
            f"Entity '{self._aggregate_class(raw_data)._entity_label()}' "
            f"(entity_id={entity_id}) not found"
        )

    async def save(self, aggregate: A) -> None:
        existing_entity = await self._get_by_id(aggregate.entity_id)
        prepared_data = self._serialize_for_persistence(aggregate)
        if existing_entity is None:
            prepared_data = self._create_metadata(prepared_data)
            await self._persistence.insert(prepared_data)
            return None
        prepared_data = self._update_metadata(existing_entity, prepared_data)
        await self._persistence.update(prepared_data)
        return None

    async def delete(self, aggregate: A) -> None:
        await self.get_by_id(aggregate.entity_id)
        await self._persistence.delete(aggregate.entity_id)

    async def _get_by_id(self, entity_id: str) -> dict | None:
        try:
            return await self._persistence.get_by_id(entity_id)
        except ValueError:
            return None

    # noinspection PyMethodMayBeStatic
    def _serialize_for_persistence(self, aggregate: A) -> dict:
        return aggregate.model_dump()

    def _hydrate_aggregate(self, raw_data: dict) -> A:
        aggregate_class = self._aggregate_class(raw_data)
        try:
            aggregate = aggregate_class.model_validate(raw_data)
        except ValidationError as e:
            raise RuntimeError(
                f"Data from persistence are not valid, hydratation "
                f"{aggregate_class._entity_label()} impossible : {e.errors()}"
            )

        return aggregate

    def _hydrate_result(self, result: dict) -> A:
        raw_data = self._convert_to_hydratation_dict(result)
        return self._hydrate_aggregate(raw_data)

    def _create_metadata(self, target: dict) -> dict:
        now = self._date_service.now().to_datetime()
        target["created_at"] = now
        target["updated_at"] = now
        return target

    def _update_metadata(self, existing: dict, target: dict) -> dict:
        target["created_at"] = existing["created_at"]
        target["updated_at"] = self._date_service.now().to_datetime()
        return target

    # noinspection PyMethodMayBeStatic
    def _convert_to_hydratation_dict(self, results: dict) -> dict:
        return results

    @staticmethod
    @abstractmethod
    def _aggregate_class(raw_data: dict | None = None) -> Type[A]:  # pragma: no cover
        ...
