from abc import abstractmethod, ABC
from typing import Type

from griff.context_entry_point import ContextEntryPoint
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.testcase import TestCase


class CliTestCase(RuntimeTestMixin, TestCase, ABC):
    @classmethod
    @abstractmethod
    def entry_point_class(cls) -> Type[ContextEntryPoint]:
        pass

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().cli_test(cls.entry_point_class())
