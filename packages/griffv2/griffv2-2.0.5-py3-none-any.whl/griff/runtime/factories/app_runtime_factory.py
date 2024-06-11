from abc import ABC, abstractmethod
from typing import Self

from griff.runtime.factories.abstract_runtime_factory import AbstractRuntimeFactory


class AppRuntimeFactory(AbstractRuntimeFactory, ABC):
    def web_runtime(self) -> Self:
        (
            self.with_log_level()
            .with_default_services()
            .with_db()
            .with_command_bus()
            .with_query_bus()
            .with_event_bus()
            .with_fastapi()
            .with_all_apis()
        )
        return self

    def cli_runtime(self) -> Self:
        (
            self.with_log_level()
            .with_default_services()
            .with_db()
            .with_command_bus()
            .with_query_bus()
            .with_event_bus()
            .with_common_cli()
            .with_all_clis()
        )
        return self

    @abstractmethod
    def with_all_apis(self) -> Self:
        ...

    @abstractmethod
    def with_all_clis(self) -> Self:
        ...
