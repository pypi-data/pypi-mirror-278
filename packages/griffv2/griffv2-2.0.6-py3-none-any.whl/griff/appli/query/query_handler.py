from abc import ABC
from typing import TypeVar, Generic

from griff.appli.message.message_handler import (
    MessageHandler,
    MessageErrorResponse,
    MessageSuccessResponse,
)
from griff.appli.query.query import Query
from griff.infra.registry.meta_registry import MetaQueryHandlerRegistry


class QuerySuccessResponse(MessageSuccessResponse, ABC):
    ...


class QueryErrorResponse(MessageErrorResponse, ABC):
    ...


QueryResponse = QuerySuccessResponse | QueryErrorResponse

QM = TypeVar("QM", bound=Query)
QR = TypeVar("QR", bound=QueryResponse)


class QueryHandler(
    Generic[QM, QR], MessageHandler[QM, QR], ABC, metaclass=MetaQueryHandlerRegistry
):
    ...
