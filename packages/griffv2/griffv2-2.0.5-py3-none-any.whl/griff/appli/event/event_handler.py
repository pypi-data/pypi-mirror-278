from abc import ABC
from typing import TypeVar, Generic

from griff.appli.event.event import Event
from griff.appli.message.message_handler import (
    MessageHandler,
)
from griff.infra.registry.meta_registry import MetaEventHandlerRegistry

EM = TypeVar("EM", bound=Event)


class EventHandler(
    Generic[EM], MessageHandler[EM, None], ABC, metaclass=MetaEventHandlerRegistry
):
    ...
