from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.uniqid_service import UniqIdService
from griff.test_utils.testcases.abstract_testcase import AbstractTestCase


class AggregateTestCase(AbstractTestCase):
    uniqid_service: UniqIdService

    @classmethod
    def setup_class(cls):
        super().setup_class()
        ServiceLocator.reset()
        cls.uniqid_service = UniqIdService(
            FakeUniqIdGenerator(9999999999999999999999999999999990001)
        )
        ServiceLocator.register(UniqIdService, cls.uniqid_service)

    def setup_method(self):
        super().setup_method()
        self.uniqid_service.reset()
