import unittest

import yaml

import hyperthought as ht


class TestSearch(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.auth = ht.auth.TokenAuthentication(
            self.setup['auth']['info'],
            verify=False,
            delayed_refresh=True,
        )
        self.search_api = ht.api.search.SearchAPI(auth=self.auth)

    def test_search(self):
        params = self.setup['api']['search']['search']
        query = params['query']
        start = params['start']
        length = params['length']
        results = self.search_api.search(
            query=query,
            start=start,
            length=length,
        )
        self.assertEqual(results['start'], start)
        self.assertEqual(results['end'], start + length - 1)
        self.assertEqual(results['totalRecords'], len(results['results']))
