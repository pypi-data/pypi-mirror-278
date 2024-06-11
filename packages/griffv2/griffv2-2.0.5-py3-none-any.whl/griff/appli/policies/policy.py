from abc import ABC, abstractmethod
from typing import Any

from returns.result import Result

from griff.utils.errors import BaseError


class Policy(ABC):
    @abstractmethod
    async def verify(self, *args, **kwargs) -> Result[Any, BaseError]:
        ...
