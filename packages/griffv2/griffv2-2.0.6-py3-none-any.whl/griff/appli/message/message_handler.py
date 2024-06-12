from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar, Self, Any

from pydantic import BaseModel, model_validator

from griff.appli.message.message import Message
from griff.domain.common_types import EntityId
from griff.utils.errors import BaseError


class AbstractMessageResponse(BaseModel, ABC):
    code: int = 200


class MessageSuccessResponse(AbstractMessageResponse):
    content: Any | None = None

    @property
    def is_success(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_failure(self) -> bool:  # pragma: no cover
        return False


class EntityIdContent(BaseModel):  # pragma: no cover
    entity_id: EntityId


class MessageErrorResponse(AbstractMessageResponse):
    code: int = 500
    error: BaseError

    @property
    def is_success(self) -> bool:  # pragma: no cover
        return False

    @property
    def is_failure(self) -> bool:  # pragma: no cover
        return True

    @model_validator(mode="after")
    def set_code_from_error_code(self) -> Self:
        self.code = self.error.code
        return self


MessageResponse = MessageSuccessResponse | MessageErrorResponse | None
M = TypeVar("M", bound=Message)
MR = TypeVar("MR", bound=MessageResponse)


class MessageHandler(Generic[M, MR], ABC):
    @abstractmethod
    async def handle(self, message: M) -> MR:  # pragma: no cover
        pass

    @classmethod
    def handlers(cls):
        return cls.__subclasses__()

    @classmethod
    @abstractmethod
    def listen_to(cls) -> Type[M]:  # pragma: no cover
        pass
