from importlib import import_module
from typing import Type

from injector import Injector, Binder, singleton

from griff.appli.event.event_bus import EventBus
from griff.appli.message.message_bus import ListMiddlewares
from griff.appli.message.message_middleware import MessageMiddleware
from griff.infra.registry.meta_registry import MetaEventHandlerRegistry
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
)
from griff.settings.griff_settings import GriffSettings


class EventBusRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(
        self, settings: GriffSettings, middlewares: list[Type[MessageMiddleware]]
    ):
        self._settings = settings
        self._middlewares = middlewares

    def configure(self, binder: Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=singleton)

    def initialize(self, injector: Injector):
        event_bus = injector.get(EventBus)
        middlewares: ListMiddlewares = [injector.get(m) for m in self._middlewares]
        for context in self._settings.bounded_contexts:
            self._import_handlers(context)
        handlers = [injector.get(h) for h in MetaEventHandlerRegistry.list_types()]
        event_bus.initialize(handlers, middlewares)

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass

    def _import_handlers(self, context):
        path = self._settings.get_context_path(context).joinpath("appli", "events")
        skip_dirs = ["__pycache__", "_tests"]
        event_handler_files = [
            str(f)
            for f in path.rglob("*.py")
            if set(f.parts).isdisjoint(skip_dirs) and not f.name.startswith("_")
        ]

        for file in event_handler_files:
            relative_path = file.replace(f"{str(self._settings.project_dir)}/", "")
            module = relative_path.replace(".py", "").replace("/", ".")
            package = module.split(".")[-1].replace("_", " ").title().replace(" ", "")

            if module in globals() and hasattr(globals()[module], package):
                continue
            imported_module = import_module(module)
            if hasattr(imported_module, package):
                globals().update({package: getattr(imported_module, package)})
                continue
            raise RuntimeError(f"package {package} not found in {module}")
        return None
