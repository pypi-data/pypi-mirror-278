from abc import ABC, ABCMeta


class AbstractMetaRegistry(ABCMeta, type):
    except_name = "None"
    REGISTRY: dict

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if ABC in bases:
            # no need to register Abstract class
            return new_cls

        class_name = f"{new_cls.__module__}.{new_cls.__name__}"
        cls.REGISTRY[class_name] = new_cls
        return new_cls

    @classmethod
    def list_types(cls):
        return dict(cls.REGISTRY).values()


class MetaQueryHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaEventHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaCommandHandlerRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaContextEntryPointRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaApiRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}


class MetaCliRouterRegistry(AbstractMetaRegistry):
    REGISTRY = {}
