import unittest

import yaml

import hyperthought as ht


class TestMetatron(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.auth = ht.auth.TokenAuthentication(
            self.setup['auth']['info'],
            verify=False,
            delayed_refresh=True,
        )
        self.metatron_api = ht.api.metatron.MetatronAPI(auth=self.auth)

    def test_get_parsers(self):
        parsers = self.metatron_api.get_parsers()
        self.assertTrue(isinstance(parsers, list))
