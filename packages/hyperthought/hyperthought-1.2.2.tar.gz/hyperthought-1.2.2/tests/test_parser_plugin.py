import unittest

import yaml

import hyperthought as ht


class TestParserPlugin(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            self.setup = yaml.safe_load(f)

        self.parser_path = self.setup['parsers']['plugin']['parser_path']
        self.data_file_path = self.setup['parsers']['plugin']['data_file_path']
        self.parser_name = self.setup['parsers']['plugin']['parser_name']

    def test_adding_a_parser(self):
        ht.parsers.add(self.parser_path)
        parser_class = ht.parsers.get(self.parser_name)
        parser = parser_class(file_path=self.data_file_path)
        parser.parse()
        self.assertGreaterEqual(len(parser.metadata), 0)

        for item in parser.metadata:
            self.assertTrue(isinstance(item, ht.metadata.MetadataItem))
