import os
import re
import time
import unittest
import uuid

import yaml

import hyperthought as ht
from hyperthought.metadata import MetadataItem


UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$',
    flags=re.IGNORECASE
)


class TestFiles(unittest.TestCase):
    def setUp(self):
        with open('setup.yml', 'r') as f:
            config_data = yaml.safe_load(f)

        # Authenticate and get a FileAPI object.
        auth_info = config_data['auth']['info']
        self.auth = ht.auth.TokenAuthentication(
            auth_info,
            verify=False, delayed_refresh=True,
        )
        self.files_api = ht.api.files.FilesAPI(auth=self.auth)

        # Setup workspace.
        self.workspace_id = config_data['api']['files']['workspace_id']

        # Create folder "test" in workspace, if such a folder does not exist.
        self.folder_name = "test"
        self.folder_path_string = f"/{self.folder_name}"
        folder_id = self.files_api.get_id_at_path(
            space_id=self.workspace_id,
            path=self.folder_path_string,
        )

        if not folder_id:
            folder_id = self.files_api.create_folder(
                name=self.folder_name,
                space_id=self.workspace_id,
            )

        self.folder_id = folder_id

        # Upload file to workspace, if it doesn't already exist there.
        self.local_file_path = config_data['api']['files']['local_file_path']
        self.file_name = os.path.basename(self.local_file_path)
        self.file_path_string = f"{self.folder_path_string}/{self.file_name}"
        self.file_size = os.path.getsize(self.local_file_path)

        file_id = self.files_api.get_id_at_path(
            path=self.file_path_string,
            space_id=self.workspace_id,
        )

        if not file_id:
            file_id, _ = self.files_api.upload(
                local_path=self.local_file_path,
                space_id=self.workspace_id,
                path=f",{self.folder_id},",
                metadata=[
                    MetadataItem(key="a", value="g"),
                    MetadataItem(key="b", value="m"),
                    MetadataItem(key="c", value="L"),
                ]
            )

        self.file_id = file_id

        # Store the directory for the download test.
        self.download_directory = (
            config_data['api']['files']['download_directory'])

        # Store the destination workspace where the file will be moved.
        self.destination_workspace_id = (
            config_data['api']['files']['destination_workspace_id'])

    def test_upload(self):
        local_path = os.path.join(os.path.dirname(__file__), "test_file.txt")

        with open(local_path, 'w') as f:
            f.write('This is a test.')

        metadata = [
            ht.metadata.MetadataItem(key="test", value=12345),
            ht.metadata.MetadataItem(key="testy", value="this is a test..."),
            ht.metadata.MetadataItem(
                key="testier",
                value=3.14,
                units="radians"
            )
        ]

        file_id, new_name = self.files_api.upload(
            local_path=local_path,
            space_id=self.workspace_id,
            metadata=metadata
        )

        self.assertIsNotNone(file_id)
        self.assertIsNotNone(new_name)
        self.assertIsNotNone(self.files_api.get_document(file_id))

        # Remove test file
        self.files_api.delete(file_id)

        os.remove(local_path)

    def test_get_id(self):
        response = self.files_api.get_id(
            name=self.file_name,
            space_id=self.workspace_id,
            path=f",{self.folder_id},",
        )
        self.assertIsNotNone(response)
        self.assertRegex(
            response, UUID_RE,
            msg="Does the response look like a file ID?"
        )

    def test_get_id_at_path(self):
        file_id = self.files_api.get_id_at_path(
            path=self.file_path_string,
            space_id=self.workspace_id,
        )
        self.assertRegex(
            file_id, UUID_RE,
            msg="Does the response look like a file ID?"
        )

    def test_get_object_link(self):
        object_link = self.files_api.get_object_link(
            space_id=self.workspace_id,
            path=self.file_path_string,
        )
        self.assertTrue(isinstance(object_link, str))
        parts = [part for part in object_link.strip('/').split('/')]
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0], 'files')
        self.assertEqual(parts[1], 'filesystementry')
        self.assertRegex(
            parts[2], UUID_RE,
            msg="Does the tail of the response look like a file ID?"
        )

    def test_get_from_location(self):
        id_path = self.files_api.get_id_path(
            space_id=self.workspace_id,
            path=self.folder_path_string,
        )
        self.assertIsNotNone(id_path)
        start = 0
        length = 10
        found = False

        while not found:
            files = self.files_api.get_from_location(
                space_id=self.workspace_id,
                path=id_path,
                start=start,
                length=length,
            )

            for file_ in files:
                if file_['name'] == self.file_name:
                    found = True
                    break

            if len(files) == 0:
                break

        self.assertTrue(found)

    def test_get_all_from_location(self):
        # TODO: also test FILES_ONLY and FOLDERS_ONLY in the no recursion case.
        # Prepare nested folders.
        root_folder_name = f"recursion_test{str(uuid.uuid4())}"
        parent_folder_name = f"test_{str(uuid.uuid4())}"
        child_folder_name = f"test_{str(uuid.uuid4())}"

        # Create a folder for the test, nested folders will be created here.
        root_folder_id = self.files_api.create_folder(
            name=root_folder_name,
            space_id=self.workspace_id,
            path=f",{self.folder_id},"
        )

        root_id_path = f",{self.folder_id},{root_folder_id},"

        # Create the nested folders.
        parent_folder_id = self.files_api.create_folder(
            name=parent_folder_name,
            space_id=self.workspace_id,
            path=root_id_path
        )

        parent_folder_id_path = root_id_path + f"{parent_folder_id},"

        child_folder_id = self.files_api.create_folder(
            name=child_folder_name,
            space_id=self.workspace_id,
            path=parent_folder_id_path
        )

        child_folder_id_path = parent_folder_id_path + f"{child_folder_id},"

        # Upload files to the nested folders.
        parent_file_id, new_file_name = self.files_api.upload(
            local_path=self.local_file_path,
            space_id=self.workspace_id,
            path=parent_folder_id_path,
        )
        child_file_id, new_file_name = self.files_api.upload(
            local_path=self.local_file_path,
            space_id=self.workspace_id,
            path=child_folder_id_path,
        )

        # Get all from location four ways.
        no_recursion = self.files_api.get_all_from_location(
            space_id=self.workspace_id,
            path=root_id_path
        )
        files_and_folders = self.files_api.get_all_from_location(
            space_id=self.workspace_id,
            path=root_id_path,
            recurse=True
        )
        files_only = self.files_api.get_all_from_location(
            space_id=self.workspace_id,
            path=root_id_path,
            file_type=self.files_api.FileType.FILES_ONLY,
            recurse=True
        )
        folders_only = self.files_api.get_all_from_location(
            space_id=self.workspace_id,
            path=root_id_path,
            file_type=self.files_api.FileType.FOLDERS_ONLY,
            recurse=True
        )

        # Prepare to verify the results
        no_recursion_checklist = [parent_folder_id]
        files_checklist = [parent_file_id, child_file_id]
        folders_checklist = [parent_folder_id, child_folder_id]
        files_folders_checklist = files_checklist + folders_checklist

        # Verification consists of two steps:
        #   1. Verify that all expected pk's are present in the response
        #   2. Check the length of the response list to make sure nothing
        #      extra was returned

        # Verify non-recursive response
        no_recursion_response = [
            response_dict["pk"] for response_dict in no_recursion
        ]

        for checklist_pk in no_recursion_checklist:
            self.assertIn(
                checklist_pk,
                no_recursion_response,
                msg=f"Item {checklist_pk} is missing from the response."
            )

        self.assertEqual(
            len(no_recursion),
            1,
            msg=f"Expected 1 top-level item but found {len(no_recursion)}."
        )

        # Verify files-and-folders response
        files_folders_response = [
            response_dict["pk"] for response_dict in files_and_folders
        ]

        for checklist_pk in files_folders_checklist:
            self.assertIn(
                checklist_pk,
                files_folders_response,
                msg=f"Item {checklist_pk} is missing from the response."
            )

        self.assertEqual(
            len(files_and_folders),
            4,
            msg=f"Expected 4 total items but found {len(files_and_folders)}."
        )

        # Verify files-only response
        files_response = [
            response_dict["pk"] for response_dict in files_only
        ]

        for checklist_pk in files_checklist:
            self.assertIn(
                checklist_pk,
                files_response,
                msg=f"File {checklist_pk} is missing from the response."
            )

        self.assertEqual(
            len(files_only),
            2,
            msg=f"Expected 2 files but found {len(files_only)}."
        )

        # Verify folders-only response
        folders_response = [
            response_dict["pk"] for response_dict in folders_only
        ]

        for checklist_pk in folders_checklist:
            self.assertIn(
                checklist_pk,
                folders_response,
                msg=f"Folder {checklist_pk} is missing from the response."
            )

        self.assertEqual(
            len(folders_only),
            2,
            msg=f"Expected 2 folders but found {len(folders_only)}."
        )

        # Remove test files and folders
        self.files_api.delete(ids=[root_folder_id])

    def test_delete(self):
        # Upload the file.
        file_id, new_file_name = self.files_api.upload(
            local_path=self.local_file_path,
            space_id=self.workspace_id,
        )

        # Verify that the file has arrived.
        file_document = self.files_api.get_document(id=file_id)
        self.assertIsNotNone(file_document)

        # Delete the file.
        self.files_api.delete(ids=[file_id])

        # Wait for the file to be deleted before performing the test.
        sleep_count = 0

        while sleep_count <= 10:
            file_document = self.files_api.get_document(id=file_id)

            if 'deleted' in file_document:
                break

            time.sleep(1)
            sleep_count += 1

        # Verify that the file is gone.
        # TODO:  Fix file GET endpoints so they don't return documents
        #        from collections other than "files.filesystementry".
        #        We are not interested in deleted or temporary files!

        if file_document:
            self.assertIn('deleted', file_document)
            self.assertTrue(bool(file_document['deleted']))

    def test_get_document(self):
        document = self.files_api.get_document(id=self.file_id)
        self.assertIsNotNone(document)

    def test_get_id_path(self):
        id_path = self.files_api.get_id_path(
            space_id=self.workspace_id,
            path=self.file_path_string,
        )
        self.assertTrue(isinstance(id_path, str))
        path_tokens = self.file_path_string.strip('/').split('/')
        ids = id_path.strip(',').split(',')
        self.assertEqual(len(path_tokens), len(ids))

    def test_create_folder(self):
        folder_name = f"test_{str(uuid.uuid4())}"
        metadata = [
            MetadataItem(key="test", value=1234.56, units="bof"),
            MetadataItem(key="test2", value="testing...")
        ]

        # Get the id path associated with the human-readable path.
        id_path = f",{self.folder_id},"

        # Create the folder.
        folder_id = self.files_api.create_folder(
            name=folder_name,
            space_id=self.workspace_id,
            path=id_path,
            metadata=metadata,
        )
        self.assertIsNotNone(folder_id)
        self.assertRegex(
            folder_id, UUID_RE,
            msg=f"response, '{folder_id}, does not look like a folder id"
        )

        # Delete the folder.
        self.files_api.delete(ids=[folder_id])

    def test_update_metadata(self):
        # Get original metadata.
        file_document = self.files_api.get_document(id=self.file_id)
        self.assertIsNotNone(
            file_document,
            f"No file found having id {self.file_id}"
        )
        original_metadata = file_document['metadata']

        # Update metadata.
        new_metadata = [
            MetadataItem(key="test", value="unit"),
            MetadataItem(key="testy", value="tests"),
            MetadataItem(key="testier", value="are"),
            MetadataItem(key="testiest", value="fun"),
            MetadataItem(key="null test", value=None),
        ]
        self.files_api.update_metadata(
            file_id=self.file_id,
            new_metadata=new_metadata,
        )

        # Get document again and verify that the change has been made.
        file_document = self.files_api.get_document(id=self.file_id)
        updated_metadata = file_document['metadata']
        new_keys = {item.key for item in new_metadata}
        updated_keys = {item['keyName'] for item in updated_metadata}
        self.assertEqual(
            new_keys, updated_keys,
            f"expected keys {new_keys} do not match actual keys "
            f"{updated_keys}"
        )

        # Change metadata back.
        # This will require a transformation of the original metadata.

        def transform_metadata(api_formatted_metadata):
            transformed_metadata = []

            for item in api_formatted_metadata:
                kwargs = {
                    'key': item['keyName'],
                    'value': item['value']['link'],
                }

                if 'unit' in item:
                    kwargs['units'] = item['unit']

                if 'annotation' in item:
                    kwargs['annotation'] = item['annotation']

                transformed_metadata.append(MetadataItem(**kwargs))

            return transformed_metadata

        transformed_metadata = transform_metadata(original_metadata)
        self.files_api.update_metadata(
            file_id=self.file_id,
            new_metadata=transformed_metadata,
        )
        file_document = self.files_api.get_document(id=self.file_id)
        updated_metadata = file_document['metadata']
        original_keys = {item.key for item in transformed_metadata}
        updated_keys = {item['keyName'] for item in updated_metadata}
        self.assertEqual(
            original_keys, updated_keys,
            f"expected keys {original_keys} do not match actual keys "
            f"{updated_keys}"
        )

    def test_update_name(self):
        # Get original name.
        file_document = self.files_api.get_document(id=self.file_id)
        self.assertIsNotNone(
            file_document,
            f"No file found having id {self.file_id}"
        )
        original_name = file_document['name']

        # Update metadata.
        new_name = "Test Update Name Unit Test"
        self.files_api.update_name(
            file_id=self.file_id,
            new_name=new_name,
        )

        # Get document again and verify that the change has been made.
        file_document = self.files_api.get_document(id=self.file_id)
        updated_name = file_document['name']
        self.assertEqual(
            new_name, updated_name,
            f"expected name {new_name} do not match actual name "
            f"{updated_name}"
        )

        # Change name back.
        self.files_api.update_name(
            file_id=self.file_id,
            new_name=original_name,
        )
        file_document = self.files_api.get_document(id=self.file_id)
        updated_name = file_document['name']
        self.assertEqual(
            original_name, updated_name,
            (
                f"expected keys {original_name} do not match actual keys "
                f"{updated_name}"
            ),
        )

    def test_download(self):
        total_bytes = 0
        n_chunks = 50

        def progress_callback(n_bytes):
            nonlocal total_bytes
            total_bytes += n_bytes
            print('n_bytes:', n_bytes, 'total_bytes:', total_bytes)

        self.files_api.download(
            file_id=self.file_id,
            directory=self.download_directory,
            progress_callback=progress_callback,
            n_chunks=n_chunks,
        )
        path = os.path.join(self.download_directory, self.file_name)
        self.assertTrue(os.path.exists(path))

    def test_move(self):
        # Forward move.
        file_ids = [self.file_id]
        destination_parent_folder_id = None

        self.files_api.move(
            source_space_id=self.workspace_id,
            destination_space_id=self.destination_workspace_id,
            source_parent_folder_id=self.folder_id,
            destination_parent_folder_id=destination_parent_folder_id,
            file_ids=file_ids,
        )

        for file_id in file_ids:
            file_document = self.files_api.get_document(id=file_id)
            id_path = file_document['path']
            sep = ht.utils.ID_PATH_SEP

            if id_path == ht.utils.ID_PATH_SEP:
                parent_id = None
            else:
                parent_id = id_path.strip(sep).split(sep)[-1]

            self.assertEqual(parent_id, destination_parent_folder_id)

        # Backwards move.
        self.files_api.move(
            source_space_id=self.destination_workspace_id,
            destination_space_id=self.workspace_id,
            source_parent_folder_id=destination_parent_folder_id,
            destination_parent_folder_id=self.folder_id,
            file_ids=file_ids,
        )

        for file_id in file_ids:
            file_document = self.files_api.get_document(id=file_id)
            id_path = file_document['path']
            sep = ht.utils.ID_PATH_SEP

            if id_path == ht.utils.ID_PATH_SEP:
                parent_id = None
            else:
                parent_id = id_path.strip(sep).split(sep)[-1]

            self.assertEqual(parent_id, self.folder_id)

    def test_copy(self):
        file_ids = [self.file_id]
        destination_parent_folder_id = None

        self.files_api.copy(
            source_space_id=self.workspace_id,
            destination_space_id=self.destination_workspace_id,
            source_parent_folder_id=self.folder_id,
            destination_parent_folder_id=destination_parent_folder_id,
            file_ids=file_ids,
        )

        file_exists = self.files_api.exists(
            name=self.file_name,
            is_folder=False,
            space_id=self.destination_workspace_id,
            size=self.file_size,
        )
        self.assertTrue(file_exists)

    def test_get_backend(self):
        response = self.files_api.get_backend()
        valid = ['s3', 'default']
        self.assertIn(response, valid, msg="Is the backend a valid backend?")

    def test_get_blank_upload_urls(self):
        """
        Test the method to get blank upload urls.

        Blank upload urls can be used to upload any file.
        """
        url_count = 5
        urls = self.files_api.generate_blank_upload_urls(url_count=url_count)
        self.assertIsInstance(urls, dict)
        self.assertEqual(len(urls), url_count)
        # Note:  The presigned urls will not be used.

    def test_create_file_after_upload(self):
        """
        Test the method to create database file documents after upload via
        blank presigned urls.
        """
        file_id = str(uuid.uuid4())
        file_info = [
            {
                "id": file_id,
                "name": f"test_{i}.txt",
                "type": "file",
                "spaceId": self.workspace_id,
                "path": ",",
                "size": 123,
                "key": str(uuid.uuid4()),
            }
            for i in range(3)
        ]
        self.files_api.create_files_after_upload(file_info=file_info)
        document = self.files_api.get_document(id=file_id)
        self.assertIsNotNone(document)
