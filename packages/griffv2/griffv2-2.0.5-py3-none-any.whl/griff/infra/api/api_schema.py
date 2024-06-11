from abc import ABC

from pydantic import BaseModel

from griff.domain.common_types import EntityId


class ApiSchema(BaseModel, ABC):  # pragma: no cover
    ...


class EntityIdSchema(ApiSchema):  # pragma: no cover
    entity_id: EntityId
