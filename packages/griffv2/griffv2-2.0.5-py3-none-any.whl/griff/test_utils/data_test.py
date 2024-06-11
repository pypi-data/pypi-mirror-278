from abc import ABC

from griff.services.date.fake_date_service import FakeDateService
from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.uniqid_service import UniqIdService


class DataTest(ABC):
    def __init__(self, start_id=1):
        self.uniqid_service = UniqIdService(FakeUniqIdGenerator(start_id))
        self.date_service = FakeDateService()


class DomainDataTest(DataTest):
    pass
