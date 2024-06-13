import collections
from enum import Enum
from functools import partial
import json
import math
import mimetypes
import os
import threading
from typing import Callable
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
import warnings

import requests

from .base import GenericAPI, ERROR_THRESHOLD
from ..metadata import MetadataItem, to_api_format
from .. import utils


INVALID_FILENAME_CHARACTERS = {"\\", "/", ":"}
DEFAULT_CONTENT_TYPE = "application/octet-stream"
VALID_SOURCES = {
    "Spike",
    "HyperDrive",
    "UI",
    "hyperthought package",
}


class InvalidSourceException(Exception):
    pass


class ThreadCounter():
    """ Thread safe counter"""

    def __init__(self):
        self._count = 0
        self.lock = threading.Lock()

    @property
    def count(self):
        with self.lock:
            return self._count

    def add(self):
        with self.lock:
            self._count += 1

    def subtract(self):
        with self.lock:
            self._count -= 1


class FileTransferProgressHandler:
    """
    Invokes a callback when transfer size thresholds have been reached.

    Parameters
    ----------
    chunk_size : int or None
        The constant interval between size thresholds.
    total_size : int
        The total size of a file in bytes.
    callback : callable
        The callback to be invoked when a size threshold has been crossed.
    """
    MINIMUM_CHUNK_SIZE = 1

    def __init__(self, chunk_size, total_size, callback):
        if not isinstance(chunk_size, int) or chunk_size < 0:
            raise ValueError("chunk_size must be a non-negative integer")

        if chunk_size < self.MINIMUM_CHUNK_SIZE:
            chunk_size = self.MINIMUM_CHUNK_SIZE

        if not isinstance(total_size, int) or total_size < 0:
            raise ValueError("total_size must be a non-negative integer")

        if not callable(callback):
            raise ValueError("callback must be callable")

        # TODO:  Callback must accept an integer
        #        (number of chunks already added).

        self.chunk_size = chunk_size
        self.total_size = total_size
        self.callback = callback

        # Invoke callback when current size is >= threshold.
        self.current_size = 0
        self.callback_threshold = chunk_size

    def add(self, increment):
        """
        Update total size (number of bytes transferred) by increment.

        self.callback will be invoked if the addition of the new increment
        crosses a size threshold.

        Parameters
        ----------
        increment : int
            The number of bytes transferred since the last invocation.
        """
        if not increment:
            return

        self.current_size += increment

        if self.current_size >= self.total_size:
            # NOTE:  Do not use self.current_size as the numerator.
            #        It may be larger than self.total_size, for reasons
            self.callback(math.ceil(self.total_size / self.chunk_size))
            return

        if self.current_size >= self.callback_threshold:
            self.callback(math.floor(self.current_size / self.chunk_size))

            while self.callback_threshold <= self.current_size:
                self.callback_threshold = min(
                    self.callback_threshold + self.chunk_size,
                    self.total_size
                )


class FilesAPI(GenericAPI):
    """
    Files API switchboard.

    Contains methods that (roughly) correspond to endpoints for the
    HyperThought files app.  The methods simplify some tasks, such as
    uploading and downloading files.

    Parameters
    ----------
    auth : hyperthought.auth Authentication class
        Authorization object used to get headers needed to call HyperThought
        endpoints.
    """
    VERSION = 'v1'

    class FileType(Enum):
        """
        Enum describing types of file documents to be returned from methods.

        See the get_from_location method for an example.
        """
        FILES_ONLY = 'file'
        FOLDERS_ONLY = 'folder'
        FILES_AND_FOLDERS = 'all'

    def __init__(self, auth):
        super().__init__(auth)
        self._backend = None
        self._files_base_url = f"{self._base_url}/api/files/"

        if self.VERSION:
            self._files_base_url += f"{self.VERSION}/"

    def get_document(self, id):
        """
        Get a database document for a file, given its id.

        Parameters
        ----------
        id : str
            The database id for a file or folder.

        Returns
        -------
        A dict-like database document for the file with the given id.
        """
        url = f"{self._files_base_url}{id}"
        curried_request = partial(
            requests.get,
            url=url,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def get_from_location(
        self,
        space_id: str,
        path: Optional[str] = None,
        file_type: Optional[FileType] = None,
        start: int = 0,
        length: int = 25,
        recurse: bool = False,
        fields: Optional[Iterable[str]] = None,
    ):
        """
        Get HyperThought files/folders from a specific location.

        Parameters
        ----------
        space_id : str
            The id of a workspace.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        file_type : FileType or None
            An enum value for the type of files to get.  A None value will
            default to FileType.FILES_AND_FOLDERS.
        start : int
            Start index for results pagination (0-based).
        length : int
            Pagination page length.
        recurse : bool
            If True, get all progeny of the location, not just immediate
            children.
        fields : list-like of str or None
            If provided, results will only include the specified fields.

        Returns
        -------
        A list of documents (dicts) from the database corresponding to
        files/folders at the specified path in the specified space.
        """
        # Validate parameters.
        space_id = self._validate_space_id(space_id=space_id)
        path = self._validate_path(path)
        file_type = self._validate_file_type(file_type)

        url = f"{self._files_base_url}workspace/{space_id}/"
        params = {
            "path": path,
            "start": start,
            "pageLength": length,
            "recurse": recurse,
        }

        if file_type is None:
            params["type"] = self.FileType.FILES_AND_FOLDERS.value
        else:
            params["type"] = file_type.value

        if fields is not None:
            params["fields"] = fields

        curried_request = partial(
            requests.get,
            url,
            params=params,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        output = r.json()

        # TODO:  Make sure this is necessary.
        if output is None:
            output = []

        # TODO:  Make sure this is necessary.
        if not isinstance(output, list):
            output = [output]

        return output

    def generate_from_location(
        self,
        space_id: str,
        path: Optional[str] = None,
        file_type: Optional[FileType] = None,
        start: int = 0,
        length: int = 25,
        recurse: bool = True,
        all: bool = True,
        fields: Optional[Iterable[str]] = None,
    ) -> Generator[None, None, Dict]:
        """
        Get HyperThought files/folders from a specific location.

        Parameters
        ----------
        space_id : str
            The id of a workspace.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        file_type : FileType or None
            An enum value for the type of files to get.  A None value will
            default to FileType.FILES_AND_FOLDERS.
        start : int
            Start index for results pagination (0-based).
        length : int
            Pagination page length.
        recurse : bool
            If True, get all progeny of the location, not just immediate
            children.
        all : bool
            If True, get all content for the location from the starting point
            (see start parameter).
        fields : list-like of str or None
            If provided, results will only include the specified fields.

        Yields
        ------
        Documents (dicts) from the database corresponding to files/folders
        at the specified path in the specified space.
        """
        stop = False

        while not stop:
            files = self.get_from_location(
                space_id=space_id,
                path=path,
                file_type=file_type,
                start=start,
                length=length,
                recurse=recurse,
                fields=fields,
            )

            for file in files:
                yield file

            if not files or not all:
                stop = True
            else:
                start += length

    def get_all_from_location(
        self,
        space_id: str,
        path: Optional[str] = None,
        file_type: Optional[FileType] = None,
        recurse: bool = False,
        fields: Optional[Iterable[str]] = None,
    ) -> List[Dict]:
        """
        Get all files/folders in a given file system location.

        Parameters
        ----------
        space_id : str
            The id of a workspace.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        file_type : FileType or None
            An enum value for the type of files to get.  A None value will
            default to FileType.FILES_AND_FOLDERS.
        recurse : bool
            If True, get all progeny of the location, not just immediate
            children.
        fields : list-like of str or None
            If provided, results will only include the specified fields.

        Returns
        -------
        A list of dicts containing information on files and/or folders in a
        given file system location.
        """
        warnings.warn(
            "This method is deprecated.  Use generate_from_location, "
            "with the 'all' parameter set to True, instead."
        )
        start = 0
        length = 25
        all = True
        generator = self.generate_from_location(
            space_id=space_id,
            path=path,
            file_type=file_type,
            start=start,
            length=length,
            recurse=recurse,
            fields=fields,
            all=all,
        )
        return list(generator)

    def get_id(self, name, space_id, path=None):
        """
        Get an id for a file/folder with a given name at a given location.

        Parameters
        ----------
        name : str
            The name of the file system entry.
        space_id : str
            The id of a workspace.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'

        Returns
        -------
        An id, if the specified file/folder exists, else None.
        """
        # Validate parameters.
        name = self._validate_name(name)
        space_id = self._validate_space_id(space_id=space_id)
        path = self._validate_path(path)

        url = f"{self._files_base_url}workspace/{space_id}/"
        params = {
            'path': path,
            'start': 0,
            'pageLength': 25,
        }

        while True:
            curried_request = partial(
                requests.get,
                url=url,
                params=params,
            )
            r = self.attempt_api_call(curried_request=curried_request)

            if r.status_code >= ERROR_THRESHOLD:
                # NOTE:  This method will throw an exception.
                self._report_api_error(response=r)

            documents = r.json()

            if not isinstance(documents, list):
                raise Exception(f"results from {url} are not a list")

            if not documents:
                return None

            for document in documents:
                if document['name'] == name:
                    # Return the first match found.
                    # Ideally, there should be only one.
                    return document['pk']

            params['start'] += params['pageLength']

    def get_id_at_path(self, path, space_id):
        """
        Get a file id given a human readable path.

        Parameters
        ----------
        space_id : str
            The id of a workspace.
        path : str
            A human-readable path, e.g. 'path/to/file.txt'

        Returns
        -------
        The id for the file corresponding to the given path if one exists,
        otherwise None.  Only the terminal id (for the last file or folder)
        will be returned.  Use get_id_path to get a full id path.
        """
        space_id = self._validate_space_id(space_id=space_id)

        if not isinstance(path, str):
            raise ValueError("path must be a string")

        sep = utils.PATH_SEP
        id_sep = utils.ID_PATH_SEP
        tokens = path.strip(sep).split(sep)
        id_path = id_sep
        id_ = None

        for token in tokens:
            id_ = self.get_id(
                name=token,
                space_id=space_id,
                path=id_path,
            )

            if id_ is None:
                break

            id_path += id_ + id_sep

        return id_

    def get_id_path(
        self,
        path: str,
        space_id: str,
        create_folders: bool = False,
    ) -> str:
        """
        Get an id path given a human readable path.

        The path will include the terminal id, whether or not the last element
        in the path is a  file.  If this is not desired, don't include the file
        in the input path.

        Parameters
        ----------
        space_id : str
            The id of a workspace.
        path : str
            A human-readable path, e.g. 'path/to/file.txt'
        create_folders : bool
            If true, any folders in the path that do not exist will be
            created.  CAUTION:  All tokens will be treated as folders,
            even those with file names, e.g. if the input is `/a/b/c/test.txt`
            and `/a/b` exists in HyperThought but folder `c` does not,
            then folders `c` and `test.txt` will be created.

        Returns
        -------
        The id path corresponding to the human-readable path,
        e.g. ',uuid,uuid,uuid,' for '/path/to/folder'.

        Exceptions
        ----------
        A FileNotFoundError will be raised in create_folders is False and
        an id corresponding to a path token could not be found.
        """
        sep = utils.PATH_SEP
        id_sep = utils.ID_PATH_SEP

        if path == sep:
            return id_sep

        space_id = self._validate_space_id(space_id=space_id)

        if not isinstance(path, str):
            raise ValueError("path must be a string")

        tokens = path.strip(sep).split(sep)
        id_path = id_sep

        for token in tokens:
            id_ = self.get_id(
                name=token,
                space_id=space_id,
                path=id_path,
            )

            if id_ is None:
                if create_folders:
                    id_ = self.create_folder(
                        name=token,
                        space_id=space_id,
                        path=id_path,
                        avoid_duplicates=True,
                    )
                else:
                    raise FileNotFoundError(f"File not found: {token}")

            id_path += id_ + id_sep

        return id_path

    def get_object_link(self, space_id=None, id_=None, path=None):
        """
        Get an object link string to store a link as a metadata value.

        Parameters
        ----------
        id_ : str or None
            The id for the file of interest.
        space_id : str or None
            The id of a workspace.
        path : str
            A human-readable path to the file of interest,
            e.g. 'path/to/file.txt'

        If id_ is not provided, the other parameters must be.

        Returns
        -------
        An object link string.
        """
        if id_ is not None and not isinstance(id_, str):
            raise ValueError(f"string expected for id_, found {type(path)}")

        if id_ is None:
            if space_id is None:
                raise ValueError("space_id must be provided if id_ is not")

            if path is None:
                raise ValueError("path must be provided if id_ is not")

        get_link = lambda id_: f"/files/filesystementry/{id_}"

        if id_ is None:
            id_ = self.get_id_at_path(space_id=space_id, path=path)

            if not id_:
                raise FileNotFoundError(
                    f"No file found at path {path} "
                    f"in workspace with id {space_id}"
                )

        return get_link(id_)

    def create_folder(
        self,
        name: str,
        space_id: str,
        path: Optional[str] = None,
        metadata: Optional[Iterable[MetadataItem]] = None,
        avoid_duplicates: bool = False,
    ) -> str:
        """
        Create a folder in HyperThought.

        Parameters
        ----------
        name : str
            The name of the folder to create.
        space_id : str
            The id of a workspace.
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        metadata : list of metadata.MetadataItem or None
            A list of MetadataItem objects.  See metadata.MetadataItem.

        Returns
        -------
        The id of the new folder.
        """
        name = self._validate_name(name)
        space_id = self._validate_space_id(space_id=space_id)
        path = self._validate_path(path)
        metadata = self._validate_metadata(metadata)

        # At the time of last modification (9/7/21), there was no v1 version
        # of the create-folder endpoint.
        url = '{}/api/files/create-folder/'.format(self._auth.get_base_url())

        # Reformat metadata as needed to pass via API.
        if metadata:
            metadata = [item.to_api_format() for item in metadata]

        curried_request = partial(
            requests.post,
            url=url,
            json={
                'space_id': space_id,
                'path': path,
                'name': name,
                'metadata': metadata,
                "avoidDuplicates": avoid_duplicates,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        folder_id = r.json()['document']['content']['pk']
        return folder_id

    def move(
        self,
        source_space_id: str,
        destination_space_id: str,
        file_ids: Iterable[str],
        source_parent_folder_id: Optional[str] = None,
        destination_parent_folder_id: Optional[str] = None,
    ) -> Dict:
        """
        Move files from one file system location to another.

        Parameters
        ----------
        source_space_id : str
            The id of the workspace from which the files are being moved.
        destination_space_id : str
            The id of the workspace to which the files are being moved.
        file_ids = list of str
            ids of files in the source location that will be moved to the
            destination location.
        source_parent_folder_id : str or None
            The id of the parent folder in the source location.
            If None, the root folder will be assumed.
        destination_parent_folder_id : str or None
            The id of the parent folder in the destination location.
            If None, the root folder will be assumed.

        Returns
        -------
        A dict containing a 'message' key.  The message indicates whether
        the request was received successfully.
        """
        if not isinstance(source_space_id, str):
            raise ValueError("source_space_id must be a string")

        if not isinstance(destination_space_id, str):
            raise ValueError("destination_space_id must be a string")

        if not isinstance(file_ids, collections.abc.Sequence):
            raise ValueError("file_ids must be a sequence (e.g., list)")

        for file_id in file_ids:
            if not isinstance(file_id, str):
                raise ValueError("all file ids must be strings")

        if (
            source_parent_folder_id is not None
            and
            not isinstance(source_parent_folder_id, str)
        ):
            raise ValueError(
                "source_parent_folder_id must be a string if provided")

        if (
            destination_parent_folder_id is not None
            and
            not isinstance(destination_parent_folder_id, str)
        ):
            raise ValueError(
                "destination_parent_folder_id must be a string if provided")

        url = f"{self._files_base_url}move/"
        curried_request = partial(
            requests.post,
            url=url,
            json={
                'sourceSpaceId': source_space_id,
                'sourceParentFolderId': source_parent_folder_id,
                'destinationSpaceId': destination_space_id,
                'destinationParentFolderId': destination_parent_folder_id,
                'fileIds': file_ids,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def copy(
        self,
        source_space_id: str,
        destination_space_id: str,
        file_ids: Iterable[str],
        source_parent_folder_id: Optional[str] = None,
        destination_parent_folder_id: Optional[str] = None,
    ) -> Dict:
        """
        Move files from one file system location to another.

        Parameters
        ----------
        source_space_id : str
            The id of the workspace from which the files are being moved.
        destination_space_id : str
            The id of the workspace to which the files are being moved.
        file_ids = list of str
            ids of files in the source location that will be moved to the
            destination location.
        source_parent_folder_id : str or None
            The id of the parent folder in the source location.
            If None, the root folder will be assumed.
        destination_parent_folder_id : str or None
            The id of the parent folder in the destination location.
            If None, the root folder will be assumed.

        Returns
        -------
        A dict containing a 'message' key.  The message indicates whether
        the request was received successfully.
        """
        if not isinstance(source_space_id, str):
            raise ValueError("source_space_id must be a string")

        if not isinstance(destination_space_id, str):
            raise ValueError("destination_space_id must be a string")

        if not isinstance(file_ids, collections.abc.Sequence):
            raise ValueError("file_ids must be a sequence (e.g., list)")

        for file_id in file_ids:
            if not isinstance(file_id, str):
                raise ValueError("all file ids must be strings")

        if (
            source_parent_folder_id is not None
            and
            not isinstance(source_parent_folder_id, str)
        ):
            raise ValueError(
                "source_parent_folder_id must be a string if provided")

        if (
            destination_parent_folder_id is not None
            and
            not isinstance(destination_parent_folder_id, str)
        ):
            raise ValueError(
                "destination_parent_folder_id must be a string if provided")

        url = f"{self._files_base_url}copy/"
        curried_request = partial(
            requests.post,
            url=url,
            json={
                'sourceSpaceId': source_space_id,
                'sourceParentFolderId': source_parent_folder_id,
                'destinationSpaceId': destination_space_id,
                'destinationParentFolderId': destination_parent_folder_id,
                'fileIds': file_ids,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def find(
        self,
        name: str,
        is_folder: bool,
        space_id: str,
        path: str = utils.ID_PATH_SEP,
        size: Optional[int] = None,
    ) -> Optional[Dict]:
        """
        Find a document given non-id params.

        The name and location must match to find a folder.
        The name, size, and location must match to find a file.

        Parameters
        ----------
        name : str
            The name of the file or folder of interest.
        is_folder : bool
            True iff the item of interest is a folder.
        space_id : str
            The id of the workspace of interest.
        path : str
            The id path to the file or folder.
        size : int or None
            The size of a file.  Must be provided if is_folder is False;
            otherwise, it will be ignored.

        Returns
        -------
        The matching document, or None.
        """
        if not isinstance(name, str):
            raise ValueError("'name' must be a str")

        if not isinstance(is_folder, bool):
            raise ValueError("'is_folder' must be a bool")

        if not isinstance(space_id, str):
            raise ValueError("'space_id' must be a str")

        if not isinstance(path, str):
            raise ValueError("'path' must be a str")

        if size is not None and not isinstance(size, int):
            raise ValueError("'size' must be an int if provided")

        if not is_folder and size is None:
            raise ValueError("'size' must be an int if 'is_folder' is False")

        # Look for the file/folder of interest.
        start = 0
        page_length = 25
        url = f"{self._files_base_url}workspace/{space_id}/"
        params = {
            "path": path,
            "type": "folder" if is_folder else "file",
            "pageLength": page_length,
        }

        while True:
            params["start"] = start
            curried_request = partial(
                requests.get,
                url=url,
                params=params,
            )
            r = self.attempt_api_call(curried_request=curried_request)

            if r.status_code >= ERROR_THRESHOLD:
                # NOTE:  This method will throw an exception.
                self._report_api_error(response=r)

            documents = r.json()

            if not isinstance(documents, list):
                raise Exception(f"results from {url} are not a list")

            if not documents:
                return None

            for document in documents:
                if document["name"] == name:
                    if is_folder:
                        return document
                    else:
                        if document["size"] == size:
                            return document
                        else:
                            return None

            start += page_length

    def exists(
        self,
        name: str,
        is_folder: bool,
        space_id: str,
        path: str = utils.ID_PATH_SEP,
        size: Optional[int] = None,
    ) -> Optional[Dict]:
        """
        Determine whether a file/folder already exists.

        The name and location must match for a folder.
        The name, size, and location must match for a file.

        Parameters
        ----------
        name : str
            The name of the file or folder of interest.
        is_folder : bool
            True iff the item of interest is a folder.
        space_id : str
            The id of the workspace of interest.
        path : str
            The id path to the file or folder.
        size : int or None
            The size of a file.  Must be provided if is_folder is False;
            otherwise, it will be ignored.

        Returns
        -------
        A bool indicating whether the file/folder already exists.
        """
        document = self.find(
            name=name,
            is_folder=is_folder,
            space_id=space_id,
            path=path,
            size=size,
        )
        return document is not None

    def upload(
        self,
        local_path: str,
        space_id: str,
        source: Optional[str] = "hyperthought package",
        path: Optional[str] = None,
        metadata: Optional[Iterable[MetadataItem]] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
        n_chunks: int = 100,
        avoid_duplicates: bool = False,
        distribution: Optional[utils.Distribution] = None,
        name_override: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Upload a file to HyperThought.

        Parameters
        ----------
        local_path : str
            The path to a file on the local system.
        space_id : str
            The id of a workspace.
        source : str
            The source of the API call, e.g. "Spike" or "HyperDrive".
        path : str or None
            The id path to the location of interest.  If none, will default to
            id root path (e.g., ',').
            Ex: an id path for '/path/to/folder' would have the form
                ',uuid,uuid,uuid,'
        metadata : list of metadata.MetadataItem or None
            A list of MetadataItem objects.  See metadata.MetadataItem.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        distribution : utils.Distribution or None
            Enum value corresponding to the file's distribution.
        name_override : str
            Name for the file in HyperThought if different from name
            of local_path.

        Returns
        -------
        A tuple containing the file id and the name of the file.  (The name is
        returned in case it is changed by HyperThought™ to ensure uniqueness.)
        """
        # Validate parameters.
        local_path = self._validate_local_path(local_path)
        space_id = self._validate_space_id(space_id=space_id)
        path = self._validate_path(path)

        if metadata is None:
            metadata = []

        metadata = self._validate_metadata(metadata)

        if not (
            distribution is None
            or
            isinstance(distribution, utils.Distribution)
        ):
            raise ValueError(
                "If provided, distribution must be an instance of "
                "hyperthought.utils.Distribution."
            )

        # TODO:  Move this into a validation function.
        if progress_callback is not None and not callable(progress_callback):
            raise ValueError("progress_callback must be a callable or None")

        if not isinstance(n_chunks, int):
            raise ValueError("n_chunks must be an int")

        # Get file name and size using the local path.
        name = (
            name_override
            if name_override is not None
            else os.path.basename(local_path)
        )
        size = os.path.getsize(local_path)
        content_type = mimetypes.guess_type(local_path)

        if not content_type:
            content_type = DEFAULT_CONTENT_TYPE

        if avoid_duplicates:
            document = self.find(
                name=name,
                is_folder=False,
                space_id=space_id,
                path=path,
                size=size,
            )

            if document:
                return (document["pk"], document["name"],)

        url = f"{self._files_base_url}upload/"
        params = {
            "workspaceId": space_id,
            "source": source,
        }

        if path is not None:
            params["path"] = path

        if metadata is not None:
            params["metadata"] = json.dumps(to_api_format(metadata=metadata))

        if distribution is not None:
            params["distribution"] = distribution.value

        file_handle = open(local_path, 'rb')

        if progress_callback is not None:
            chunk_size = math.ceil(size / n_chunks)
            progress_handler = FileTransferProgressHandler(
                chunk_size=chunk_size,
                total_size=size,
                callback=progress_callback,
            )
            original_read = file_handle.read

            def new_read(size):
                progress_handler.add(size)
                return original_read(size)

            file_handle.read = new_read

        headers = self.auth.get_headers()

        # Content-Disposition (with file name) is required by Django 2.2.
        headers.update({
            "Content-Disposition": f"inline;filename={name}",
            "Content-Length": f"{size}",
        })
        kwargs = {
            "url": url,
            "data": file_handle,
            "params": params,
            "verify": self.auth.verify,
            "stream": True,
            "headers": headers,
        }
        r = requests.put(**kwargs)
        file_handle.close()

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        result = r.json()
        file_id = result["fileId"]

        if "fileName" in result:
            return file_id, result["fileName"]
        else:

            document = self.get_document(id=file_id)
            return file_id, document["name"]

    def download(
        self,
        file_id: str,
        directory: str,
        progress_callback: Optional[Callable] = None,
        n_chunks: int = 100,
        source: Optional[str] = "hyperthought package",
    ) -> None:
        """
        Download a file from HyperThought to the local file system.

        Parameters
        ----------
        file_id : str
            The HyperThought id for a file to be downloaded.
        directory : str
            A local directory path to which the file will be downloaded.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        """
        # Validate parameters.
        self._validate_id(file_id)
        self._validate_local_path(directory)

        # Make sure the path is a directory.
        if not os.path.isdir(directory):
            print(f"{directory} is not a directory")
            raise ValueError(f"{directory} is not a directory")

        # Get the file name.
        file_info = self.get_document(id=file_id)
        file_size = file_info['size']
        file_name = file_info['name']
        file_path = os.path.join(directory, file_name)

        # Get a download url.
        url = self._get_download_url(file_id=file_id, source=source)

        # Use the url to download the file.
        # NOTE:  Download attempts will not be curried and passed to
        #        self.attempt_api_call, since it is not clear that multiple
        #        attempts can be made with a presigned url.
        self._download_using_url(
            download_url=url,
            local_path=file_path,
            file_size=file_size,
            progress_callback=progress_callback,
            n_chunks=n_chunks,
        )

    def delete(self, ids):
        """
        Delete a file or folder.

        Parameters
        ----------
        ids : str
            Ids of files/folders to be deleted.
        """
        # Validate parameters.
        for id_ in ids:
            self._validate_id(id_)

        curried_request = partial(
            requests.delete,
            url='{}/api/files/'.format(self._base_url),
            json={'ids': ids},
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

    def update_metadata(self, file_id, new_metadata):
        """
        Update metadata for a file.

        Parameters
        ----------
        file_id : str
            The id (uuid) for the file of interest.
        new_metadata : list of MetadataItem or None
            New metadata for the file.
            This will replace any existing metadata.
            Merging will need to be done client-side.
        """
        if new_metadata is None:
            new_metadata = []

        # NOTE:  This method throws exceptions.
        new_metadata = self._validate_metadata(new_metadata)
        new_metadata = [item.to_api_format() for item in new_metadata]
        curried_request = partial(
            requests.patch,
            url=f"{self._base_url}/api/files/",
            json={
                'file_id': file_id,
                'updates': {
                    'metadata': new_metadata,
                }
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method throws exceptions.
            self._report_api_error(r)

    def bulk_metadata_update(self, file_ids, new_metadata):
        """
        Updates metadata for a group of files.

        Parameters
        -------------------------------------
        file_ids : str
            List of the unique file id numbers for the files that are
            being updated.

        new_metadata : list of MetadataItem or None
            New metadata being written to the file. Will replace any
            existing metadata. Merging will need to be done client
            side.
        """
        # Validate input parameters
        new_metadata = self._validate_metadata(new_metadata)
        api_formatted_metadata = to_api_format(metadata=new_metadata)

        for id_ in file_ids:
            self._validate_id(id_)

        curried_request = partial(
            requests.patch,
            url=f"{self._base_url}/api/files/bulk-update/",
            json={
                'fileIds': file_ids,
                'newMetadata': api_formatted_metadata,
            }
        )

        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE: This method throws exceptions.
            self._report_api_error(r)

    def update_name(self, file_id, new_name):
        """
        Update name for a file.

        Parameters
        ----------
        file_id : str
            The id (uuid) for the file of interest.
        new_metadata : str
            New name for the file.
        """
        # NOTE:  This method throws exceptions.
        new_name = self._validate_new_name(new_name)
        curried_request = partial(
            requests.patch,
            url=f"{self._base_url}/api/files/",
            json={
                'file_id': file_id,
                'updates': {
                    'content': {
                        'name': new_name
                    }
                }
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method throws exceptions.
            self._report_api_error(r)

    def upload_using_url(
        self,
        upload_url: str,
        local_path: str,
        source: str = "hyperthought package",
        progress_callback: Optional[Callable] = None,
        n_chunks: int = 100,
    ):
        """
        Use a url to upload a file.

        Called from self.upload.

        Parameters
        ----------
        upload_url : str
            The url to which the file should be uploaded.
        local_path : str
            The local path to the file to be uploaded.
        progress_callback : callable(int -> None) or None
            A callable to provide progress on upload status.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        source : str
            The source of the API call, e.g. "Spike" or "HyperDrive".
        """
        upload_url = self._validate_url(upload_url)
        local_path = self._validate_local_path(local_path)
        source = self._validate_source(source)

        file_size = os.path.getsize(local_path)
        file_handle = open(local_path, 'rb')

        if progress_callback is not None:
            chunk_size = math.ceil(file_size / n_chunks)
            progress_handler = FileTransferProgressHandler(
                chunk_size=chunk_size,
                total_size=file_size,
                callback=progress_callback,
            )
            original_read = file_handle.read

            def new_read(size):
                progress_handler.add(size)
                return original_read(size)

            file_handle.read = new_read

        kwargs = {
            "url": upload_url,
            "data": file_handle,
            "verify": False,
            "stream": True,
            "headers": self._auth.get_headers(),
        }

        # NOTE:  This request will not be curried and passed to
        #        self.attempt_api_call, since it is not clear that multiple
        #        attempts could be made with a presigned url.
        if source is not None:
            kwargs["params"] = {
                "source": source,
            }

        # Content-Disposition (with file name) is required by Django 2.2.
        sep = utils.PATH_SEP
        file_name = local_path.strip(sep).split(sep)[-1]
        kwargs['headers'].update({
            "Content-Disposition": f"inline;filename={file_name}",
            "Content-Length": f"{file_size}",
        })

        r = requests.put(**kwargs)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        file_handle.close()

    def generate_blank_upload_urls(self, url_count):
        """
        Generate blank upload urls.

        Blank urls can be used with any file.

        Parameters
        ----------
        url_count : int
            The number of urls to generate.

        Returns
        -------
        A dictionary (file key -> url).  See the create_permanent_files method
        for instructions on how to use the file keys after the urls have been
        used to upload the files.
        """
        if not isinstance(url_count, int) or url_count <= 0:
            raise ValueError("url_count must be a positive integer")

        curried_request = partial(
            requests.post,
            url=f"{self._files_base_url}generate-blank-upload-urls/",
            json={
                'urlCount': url_count,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

        key_to_url = r.json()["urls"]

        for key in key_to_url:
            url = key_to_url[key]

            if not url.startswith(self._base_url):
                key_to_url[key] = f"{self._base_url}{url}"

        return key_to_url

    def create_files_after_upload(
        self,
        file_info: Iterable[Mapping],
        source: Optional[str] = "hyperthought package",
    ) -> None:
        """
        Create file database documents after using blank urls to upload files.

        Parameters
        ----------
        file_info : list of dict
            Each element must contain the following keys:
                id : str
                    The id for the file/folder to be created.
                    Must be pre-specified.
                name : str
                    The name of the file, including its extension.
                type : str
                    The type of the file system object.  Must be "file" or
                    "folder".
                spaceId : str
                    The id of the workspace of interest.
                path : str
                    Comma-separated list of ancester folder ids,
                    e.g. ",UUID,UUID,UUID,"
                size : int
                    Size of the file in bytes.
                    Only required for files.  Will be ignored for folders.
                key : str
                    The key to the file in the file storage backend.
                    Only required for files.  Will be ignored for folders.
            In addition, the following key may be provided:
                metadata : list of dict
                    API-formatted metadata to associate with the file.
                    See the metadata module for more information.
        source : str
            The source of the API request, e.g. "Spike" or "HyperDrive".
        """
        # Add backend to file info.
        backend = self.get_backend()

        for item in file_info:
            item["backend"] = backend

        # The endpoint will take care of validating file info.
        curried_request = partial(
            requests.post,
            url=f"{self._files_base_url}create-files-after-upload/",
            json={
                "fileInfo": file_info,
                "source": source,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            # NOTE:  This method will throw an exception.
            self._report_api_error(response=r)

    def get_backend(self):
        """
        Get the files backend.

        Returns
        -------
        A string describing the file backend, e.g. 's3' or 'default'.
        """
        if self._backend is not None:
            return self._backend

        curried_request = partial(
            requests.get,
            url=f'{self._base_url}/api/files/backend/',
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        self._backend = r.json()['backend']
        # TODO:  Replace assertion with proper error handling.
        assert self._backend in ('s3', 'default',), (
            f"Unexpected backend: {self._backend}. "
            f"Expected 's3' or 'default'."
        )
        return self._backend

    def is_folder(self, document):
        """Determine whether a document represents a folder in the
        HyperThought file system."""
        if not isinstance(document, collections.Mapping):
            return False

        if 'content' in document:
            if 'ftype' in document['content']:
                return document['content']['ftype'] == utils.FOLDER_TYPE

        if 'ftype' in document:
            return document['ftype'] == utils.FOLDER_TYPE

        return False

    def _get_download_url(
        self,
        file_id: str,
        source: Optional[str] = "hyperthought package",
    ) -> str:
        """
        Get a url that can be used to download a file.

        Parameters
        ----------
        id : str
            The HyperThought id for a file of interest.

        Returns
        -------
        A url that can be used to download the file.
        """
        file_id = self._validate_id(file_id)
        curried_request = partial(
            requests.get,
            url=f"{self._files_base_url}generate-download-url/",
            params={
                "id": file_id,
                "source": source,
            },
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code >= ERROR_THRESHOLD:
            self._report_api_error(response=r)

        return r.json()['url']

    def _download_using_url(self, download_url, local_path, file_size,
                            progress_callback, n_chunks):
        """
        Use a generated url to download a file.

        Parameters
        ----------
        download_url : str
            The generated url for downloading the file of interest.
            See self._get_download_url.
        local_path : str
            The local system path where the downloaded file will be saved.
        progress_callback : callable (int -> None) or None
            A callback for handling upload progress.  Will be called each time
            a given number of bytes (chunk) is uploaded.
        n_chunks : int
            The number of chunks to be handled by progress_callback.
            Will be ignored if progress_callback is None.
        """
        kwargs = {
            'url': download_url,
            'stream': True,
            'verify': False,
        }

        if self.get_backend() == 'default':
            kwargs['headers'] = self._auth.get_headers()

        progress_handler = None

        if progress_callback is not None:
            progress_chunk_size = math.ceil(file_size / n_chunks)
            progress_handler = FileTransferProgressHandler(
                chunk_size=progress_chunk_size,
                total_size=file_size,
                callback=progress_callback,
            )

        DOWNLOAD_CHUNK_SIZE = 8192

        with requests.get(**kwargs) as r:
            r.raise_for_status()

            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if chunk:   # filter out keep-alive new chunks
                        f.write(chunk)

                        if progress_handler:
                            progress_handler.add(DOWNLOAD_CHUNK_SIZE)

    def _validate_id(self, id_):
        assert isinstance(id_, str), (
            f"expected string as id, found {type(id_)}")
        return id_

    def _validate_space(self, space=None):
        if space is None:
            space = 'user'

        # TODO:  Call error-handling function instead of raising an
        #        AssertionError.
        #        Same goes for all assertions in validation methods.
        assert space in ('group', 'project', 'user',), (
            f"Invalid space: {space}")

        return space

    def _validate_space_id(self, space=None, space_id=None):
        assert isinstance(space_id, str), (
            f"string expected, found {type(space_id)}")
        return space_id

    def _validate_path(self, path):
        if path is None:
            path = utils.ID_PATH_SEP

        assert isinstance(path, str)
        assert path.startswith(utils.ID_PATH_SEP)
        assert path.endswith(utils.ID_PATH_SEP)
        return path

    def _validate_name(self, name):
        assert isinstance(name, str)
        return name

    def _validate_new_name(self, name):
        name = self._validate_name(name)
        for char in name:
            assert char not in INVALID_FILENAME_CHARACTERS
        return name

    def _validate_size(self, size):
        assert isinstance(size, int) and size >= 0
        return size

    def _validate_metadata(self, metadata):
        # Validate metadata structure.
        if metadata is None:
            return None

        error_message = (
            "metadata must be a list of hyperthought.metadata.MetadataItem")

        if not isinstance(metadata, list):
            raise ValueError(error_message)

        for item in metadata:
            if not isinstance(item, MetadataItem):
                raise ValueError(error_message)

        return metadata

    def _validate_url(self, url):
        # TODO:  Use regex?
        assert isinstance(url, str)
        return url

    def _validate_local_path(self, local_path):
        assert isinstance(local_path, str)
        local_path = os.path.abspath(local_path)
        assert os.path.exists(local_path)
        return local_path

    def _validate_file_type(self, file_type):
        if file_type is None:
            file_type = self.FileType.FILES_AND_FOLDERS

        assert isinstance(file_type, self.FileType)

        return file_type

    def _validate_source(self, source):
        """
        Raise an exception if source is not valid.

        Parameters
        ----------
        source : str
            The source of an API call, e.g. "Spike" or "HyperDrive".
        """
        # This function was copied from hyperthought, apps.files.api.v1.utils.
        # TODO:  Consider adding a service to get valid sources.

        if source is not None and source not in VALID_SOURCES:
            raise InvalidSourceException(
                f"{source} is not a valid source. "
                f"Valid sources: {VALID_SOURCES}"
            )

        # Return a validated value, in keeping with other validation functions.
        return source
