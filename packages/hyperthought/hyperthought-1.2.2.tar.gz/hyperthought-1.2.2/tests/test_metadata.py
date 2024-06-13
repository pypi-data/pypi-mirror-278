import unittest

import hyperthought as ht


class TestParserPlugin(unittest.TestCase):
    def setUp(self):
        self.api_formatted_metadata = [
            {
                "keyName": "Build Conditions",
                "children": [
                    {
                        "keyName": "Parameters",
                        "children": [
                            {
                                "keyName": "Orientation",
                                "value": {
                                    "type": "string",
                                    "link": "X"
                                }
                            },
                            {
                                "keyName": "Melt",
                                "children": [
                                    {
                                        "keyName": "Time",
                                        "value": {
                                            "type": "number",
                                            "link": 53
                                        },
                                        "unit": "minute"
                                    },
                                    {
                                        "keyName": "Temperature",
                                        "value": {
                                            "type": "number",
                                            "link": 300
                                        },
                                        "unit": "degree-fahrenheit"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "keyName": "Ambient Conditions",
                        "children": [
                            {
                                "keyName": "Relative Humidity",
                                "value": {
                                    "type": "number",
                                    "link": 50
                                },
                                "unit": "%"
                            },
                            {
                                "keyName": "Temperature",
                                "value": {
                                    "type": "number",
                                    "link": 72
                                },
                                "unit": "degree-fahrenheit"
                            }
                        ]
                    }
                ]
            },
            {
                "keyName": "Materials Properties",
                "children": [
                    {
                        "keyName": "tensile ultimate strength",
                        "value": {
                            "type": "number",
                            "link": 6000
                        },
                        "unit": "ksi"
                    },
                    {
                        "keyName": "tensile yield strength",
                        "value": {
                            "type": "number",
                            "link": 6000
                        },
                        "unit": "ksi"
                    }
                ]
            }
        ]

        self.malformed_api_metadata = {
            "must be": "a list",
        }

    def test_to_api_format(self):
        pass

    def test_from_api_format(self):
        """
        Test metadata.from_api_format.

        Convert data, then assert lengths of unconverted and converted data
        are equal.  Then make sure the number of children for each top-level
        item is correct in the converted data.

        Attempt to convert malformed data.  Confirm that an exception is
        raised.
        """
        metadata = ht.metadata.from_api_format(self.api_formatted_metadata)

        # Make sure the result is a list.
        self.assertIsInstance(metadata, list)

        # Make sure each element of the list is a metadata item.
        for item in metadata:
            self.assertIsInstance(item, ht.metadata.MetadataItem)

        # Make sure the length of the list matches expectation.
        self.assertEqual(len(metadata), len(self.api_formatted_metadata))

        # Make sure children are present.
        key_to_len_children = {}

        for api_item in self.api_formatted_metadata:
            if "children" in api_item and api_item["children"]:
                key = api_item["keyName"]
                len_children = len(api_item["children"])
                key_to_len_children[key] = len_children

        for item in metadata:
            if item.key in key_to_len_children:
                self.assertEqual(
                    len(item.children),
                    key_to_len_children[item.key]
                )

        # Attempt to convert bad input.
        exception = None

        try:
            metadata = ht.metadata.from_api_format(self.malformed_api_metadata)
        except Exception as e:
            exception = e

        self.assertIsInstance(exception, ValueError)
