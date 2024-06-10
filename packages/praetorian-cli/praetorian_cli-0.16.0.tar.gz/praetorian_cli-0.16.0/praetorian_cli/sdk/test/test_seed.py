import time

import pytest

from praetorian_cli.handlers.utils import Asset
from praetorian_cli.sdk.test import BaseTest
from praetorian_cli.sdk.test.utils import Utils


@pytest.fixture(scope="class", params=[f"contoso-{int(time.time())}.com", "10.1.1.1/32"])
def seed(request):
    request.cls.seed = request.param


@pytest.mark.usefixtures("seed")
@pytest.mark.coherence
class TestSeed(BaseTest):

    def setup_class(self):
        self.chariot, self.username = BaseTest.setup_chariot(self)
        self.utils = Utils(self.chariot)

    def test_add_seed(self):
        response = self.chariot.add('seed', dict(dns=self.seed))[0]
        assert response['dns'] == self.seed, "Response does not have correct seed"
        assert response['status'] == Asset.ACTIVE.value, "Response does not have correct status"

    def test_my_seed(self):
        response = self.chariot.my(dict(key=f'#seed#'))
        assert any(my_seed['dns'] == self.seed for my_seed in response['seeds']), "None of the seeds matched self.seed"

    def test_my_job(self):
        response = self.chariot.my(dict(key=f'#job#{self.seed}'))
        assert response is not None, "Received empty response for my Jobs"
        for job in response['jobs']:
            assert job['source'] is not '', "Job Capability is empty"
            assert job['status'] is not None, "Job Status is empty"

    def test_freeze_seed(self):
        response = self.chariot.update('seed', dict(key=f'#seed#{self.seed}', status=Asset.FROZEN.value))[0]
        assert response['status'] == Asset.FROZEN.value, "Response does not have correct status"

    def test_delete_seed(self):
        self.chariot.delete('seed', key=f'#seed#{self.seed}')
        response = self.chariot.my(dict(key=f'#seed#{self.seed}'))
        assert response == {}
