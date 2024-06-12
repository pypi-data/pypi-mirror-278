import abc


class UniqIdGenerator(abc.ABC):
    @abc.abstractmethod
    def next_id(self) -> str:
        ...  # pragma: no cover

    def reset(self, start_id=None):  # pragma: no cover
        pass
