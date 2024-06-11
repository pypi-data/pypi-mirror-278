from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Dict, Any

from pydantic import BaseModel, Field

from griff.appli.message.message_handler import (
    Message,
    MessageResponse,
)

M = TypeVar("M", bound=Message)
MR = TypeVar("MR", bound=MessageResponse | None)


class MessageContext(BaseModel):
    context: Dict[str, Any] = Field(default_factory=dict)

    def get(self, key):
        if key not in self.context.keys():
            raise ValueError(f"{key} not found in command context")
        return self.context[key]

    def add(self, key, value):
        if key in self.context.keys():
            raise ValueError(
                f' "{key}" already set in command context, '
                f'with "{self.context[key]}" value'
            )
        self.context[key] = value

    def has(self, key) -> bool:
        return key in self.context.keys()


class MessageMiddleware(Generic[M, MR], ABC):
    def __init__(self):
        self._next = None

    def set_next(self, middleware: "MessageMiddleware") -> "MessageMiddleware":
        self._next = middleware
        return middleware

    @abstractmethod
    async def dispatch(
        self, message: M, context: MessageContext | None = None
    ) -> MR:  # pragma: no cover
        ...
