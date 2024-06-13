import unittest

import re
import yaml

import hyperthought as ht


UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$',
    flags=re.IGNORECASE
)


class TestWorkspaces(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.auth = ht.auth.TokenAuthentication(
            self.setup['auth']['info'],
            verify=False,
            delayed_refresh=True,
        )
        self.workspaces_api = ht.api.workspaces.WorkspacesAPI(auth=self.auth)

    def test_get_workspaces(self):
        response = self.workspaces_api.get_workspaces()
        self.assertIsNotNone(response)
        self.assertTrue(
            len(list(response)) >= 1,
            msg='Did we find some workspaces?'
        )
