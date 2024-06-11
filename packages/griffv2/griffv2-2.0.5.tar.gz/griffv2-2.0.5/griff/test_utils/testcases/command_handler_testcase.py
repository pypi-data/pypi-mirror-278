from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic

from griff.appli.command.command_handler import CommandHandler, CommandResponse
from griff.infra.persistence.dict_domain_persistence import DictDomainPersistence
from griff.test_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.test_utils.pytest_runtime_factory import PytestRuntimeFactory
from griff.test_utils.testcases.abstract_testcase import AbstractTestCase

CH = TypeVar("CH", bound=CommandHandler)


class CommandHandlerTestCase(Generic[CH], RuntimeTestMixin, AbstractTestCase, ABC):
    handler: CH

    @classmethod
    def runtime_factory(cls) -> PytestRuntimeFactory:
        return super().runtime_factory().command_test_handler()

    def setup_method(self):
        super().setup_method()
        self.handler = self.get_injected(self.handler_class)

    @staticmethod
    async def prepare_success_resultset(
        response: CommandResponse, persistence: DictDomainPersistence
    ):
        return {
            "response": response.model_dump(),
            "persistence": await persistence.run_query("list_all"),
        }

    @property
    @abstractmethod
    def handler_class(self) -> Type[CH]:
        pass
