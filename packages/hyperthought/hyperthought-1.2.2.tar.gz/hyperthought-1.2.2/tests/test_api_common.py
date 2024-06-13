import re
import unittest

import yaml

import hyperthought as ht


class TestCommon(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            config_data = yaml.safe_load(f)

        self.auth = ht.auth.TokenAuthentication(
            config_data['auth']['info'],
            verify=False,
            delayed_refresh=True,
        )
        self.common_api = ht.api.common.CommonAPI(auth=self.auth)

        # Setup workspace.
        self.workspace_id = config_data['api']['files']['workspace_id']

    def test_report_bug(self):
        description1 = 'Something went wrong.'
        severity1 = self.common_api.BugSeverity.MEDIUM
        response = self.common_api.report_bug(description1)
        expected_keys = [
            'id', 'user', 'description', 'severity', 'location', 'email'
        ]

        for key in expected_keys:
            message = (
                f'Does the 1st .report_bug() response contain the "{key}" key?'
            )
            self.assertIn(key, response, msg=message)

        self.assertEqual(response['description'], description1)
        regex = re.compile(response['severity'], flags=re.IGNORECASE)
        message = (
            'Does the 1st .report_bug() response have the default severity?'
        )
        self.assertRegex(
            str(severity1), regex,
            msg=message
        )

        description2 = 'Something major went wrong.'
        severity2 = self.common_api.BugSeverity.CRITICAL
        response = self.common_api.report_bug(description2, severity=severity2)
        expected_keys = [
            'id', 'user', 'description', 'severity', 'location', 'email'
        ]

        for key in expected_keys:
            message = (
                f'Does the 2nd .report_bug() response contain the "{key}" key?'
            )
            self.assertIn(key, response, msg=message)

        self.assertEqual(response['description'], description2)
        regex = re.compile(response['severity'], flags=re.IGNORECASE)
        message = (
            'Does the 2nd .report_bug() response have the requested severity?'
        )
        self.assertRegex(str(severity2), regex, msg=message)

    def test_get_units(self):
        response = self.common_api.get_units()

        message = (
            "The .get_units() call responded with a non-zero length list.")
        self.assertTrue(len(response) > 1, msg=message)
        expected_keys = ['quantityKindLabel', 'unitLabel']
        found = {
            'lambert': {'found': False, 'expected': True},
            'newton-meter': {'found': False, 'expected': True},
            'erg-per-gram': {'found': False, 'expected': True},
            'waldo': {'found': False, 'expected': False},
            'frame-per-second': {'found': False, 'expected': True},
            'joule-per-cubic-meter-kelvin': {'found': False, 'expected': True}
        }

        for entry in response:
            for key in expected_keys:
                message = f'Does unit entry `{entry}` contain the "{key}" key?'
                self.assertIn(key, entry, msg=message)
            if 'unitLabel' in entry:
                for search_key in list(found.keys()):
                    if search_key == entry['unitLabel']:
                        found[search_key]['found'] = True

        for search_key in list(found.keys()):
            text = "found" if found[search_key]['expected'] else "did not find"
            message = f'We {text} the "{search_key}" unit.'
            got = found[search_key]['found']
            expected = found[search_key]['expected']
            self.assertEqual(got, expected, msg=message)

    def test_get_vocab(self):
        response = self.common_api.get_vocab()

        message = (
            "The .get_vocab() call responded with a non-zero length list.")
        self.assertTrue(len(response) > 1, msg=message)
        expected_keys = ['topic', 'key', 'definition']
        found = {
            'weight resistivity': {'found': False, 'expected': True},
            'coercivity': {'found': False, 'expected': True},
            'chord modulus': {'found': False, 'expected': True},
            'waldo': {'found': False, 'expected': False},
            'fracture toughness': {'found': False, 'expected': True},
            'corrosion rate': {'found': False, 'expected': True}
        }

        for entry in response:
            for key in expected_keys:
                message = (
                    f'Does vocab entry `{entry}` contain the "{key}" key?')
                self.assertIn(key, entry, msg=message)
            if 'key' in entry:
                for search_key in list(found.keys()):
                    if search_key == entry['key']:
                        found[search_key]['found'] = True

        for search_key in list(found.keys()):
            text = "found" if found[search_key]['expected'] else "did not find"
            message = f'We {text} the "{search_key}" vocab.'
            got = found[search_key]['found']
            expected = found[search_key]['expected']
            self.assertEqual(got, expected, msg=message)

    def test_update_metadata(self) -> None:
        """
        Test CommonAPI.update_metadata.

        Steps:
        1.  Create two folders.
        2.  Update metadata for the folders.
        3.  Get the folders and confirm the update.
        4.  Delete the folders.
        """
        # Create two folders.
        files_api = ht.api.files.FilesAPI(self.auth)

        folder1_id = files_api.create_folder(
            name='test_folder_1',
            space_id=self.workspace_id,
        )
        folder2_id = files_api.create_folder(
            name='test_folder_2',
            space_id=self.workspace_id,
        )

        # Update metadata for the folders.
        key1 = "test1"
        key2 = "test2"
        metadata1 = [
            ht.metadata.MetadataItem(key=key1)
        ]
        metadata2 = [
            ht.metadata.MetadataItem(key=key2)
        ]
        metadata_info = [
            {
                "documentId": folder1_id,
                "metadata": metadata1,
            },
            {
                "documentId": folder2_id,
                "metadata": metadata2,
            },
        ]
        self.common_api.update_metadata(metadata_info=metadata_info)

        # Get the folders.
        folder1 = files_api.get_document(id=folder1_id)
        folder2 = files_api.get_document(id=folder2_id)

        # Check the metadata.
        folder1_keys = {item["keyName"] for item in folder1["metadata"]}
        folder2_keys = {item["keyName"] for item in folder2["metadata"]}
        self.assertEqual(folder1_keys, {key1})
        self.assertEqual(folder2_keys, {key2})

        # Delete the folders.
        files_api.delete(ids=[folder1_id, folder2_id])
