import inspect
from hashlib import sha256

from griff.domain.common_types import Aggregate
from griff.services.uniqid.generator.uniqid_generator import (
    UniqIdGenerator,
)


class FakeUniqIdGenerator(UniqIdGenerator):
    def __init__(self, start_id=1):
        self._start = 0
        self._start = start_id - 1
        self._referrer_last_uuid = {}

    def next_id(self) -> str:
        referrer = self._get_referrer_name()
        if referrer not in self._referrer_last_uuid:
            start_id = self._start + (len(self._referrer_last_uuid.keys()) * 1000)
            self._referrer_last_uuid[referrer] = self._format_id(start_id)

        self._referrer_last_uuid[referrer] = self._increment_id(
            self._referrer_last_uuid[referrer]
        )
        return self._referrer_last_uuid[referrer]

    def reset(self, start_id: int = 1):
        self._start = start_id - 1
        self._referrer_last_uuid = {}

    def _increment_id(self, str_id):
        str_id = int(str_id) + 1
        return self._format_id(str_id)

    @staticmethod
    def _format_id(str_id: int) -> str:
        return f"{str_id:036d}"

    def _get_referrer_name(self) -> str:
        entity_name = self._get_entity_name()
        if entity_name is None:
            entity_name = "__unknown__"
        return sha256(entity_name.encode()).hexdigest()

    @staticmethod
    def _get_entity_name():  # pragma: no cover
        contexts = [
            context
            for context in inspect.stack()
            if "/domain/" in context.filename
            and "pyddd" not in context.filename
            and "_tests" not in context.filename
        ]
        for context in contexts:
            try:
                klass = context[0].f_locals["cls"]
                if issubclass(klass, Aggregate):
                    return str(klass)
            except Exception:
                pass
        return None
