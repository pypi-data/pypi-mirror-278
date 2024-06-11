from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from injector import Binder, Injector


@runtime_checkable
class Runnable(Protocol):
    @abstractmethod
    def initialize(self, injector: Injector):
        ...

    @abstractmethod
    def start(self, injector: Injector):
        ...

    @abstractmethod
    def stop(self, injector: Injector):
        ...

    @abstractmethod
    def clean(self, injector: Injector):
        ...


@runtime_checkable
class AsyncRunnable(Protocol):
    @abstractmethod
    async def async_start(self, injector: Injector):
        ...

    @abstractmethod
    async def async_stop(self, injector: Injector):
        ...


@runtime_checkable
class InjectBindable(Protocol):
    @abstractmethod
    def configure(self, binder: Binder) -> None:
        ...


class RuntimeComponent(ABC):
    def __str__(self):
        return self.__class__.__name__
