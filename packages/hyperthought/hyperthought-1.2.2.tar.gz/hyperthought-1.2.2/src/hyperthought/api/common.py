from enum import Enum
from functools import partial
from typing import Dict
from typing import Iterable
from typing import Mapping
from typing import Union

import requests

from .. metadata import MetadataItem, to_api_format
from .base import GenericAPI, ERROR_THRESHOLD


class CommonAPI(GenericAPI):
    """
    Common API switchboard.

    Contains methods corresponding to endpoints that are called from multiple
    HyperThought™ components.

    Parameters
    ----------
    auth : auth.Authorization
        Authorization object used to get headers needed to call HyperThought
        endpoints.
    """

    class BugSeverity(Enum):
        """Severity levels used when reporting bugs."""
        LOW = 0
        MEDIUM = 1
        HIGH = 2
        CRITICAL = 3

        def to_string(self):
            """Convert enum instance to a string."""
            return self.name.title()

        @classmethod
        def to_enum(cls, severity):
            """
            Get an enum instance from corresponding text.

            Parameters
            ----------
            severity : str
                A string representing a severity level.

            Returns
            -------
            An enum instance.
            """
            # TODO:  Handle error case:  when severity string does not
            #        correspond to an enum value.
            return cls[severity.upper()]

    def __init__(self, auth):
        super().__init__(auth)

    def report_bug(self, description, severity=None):
        """
        Report a bug in the HyperThought™ API or a related application.

        Parameters
        ----------
        description : str
            A description of the error encountered.
        severity : BugSeverity or None
            The severity of the error being reported.  Default: MEDIUM.

        Returns
        -------
        A dictionary representing the bug report.  Keys will include the
        following:
            id : int
                The database id associated with the bug report record.
            user : str
                The username of the reported.
            email : str
                The email address of the reporter.
            description : str
                The description of the error, same value as the parameter.
            severity : str
                The severity level of the error, parameter value converted to
                title-case string.
            location : str
                A url supplied to the endpoint to identify which component
                the error is associated with.  The value used here is simply
                the base url plus "/api".
        """
        # Validate inputs.
        # TODO:  improve error handling, document exceptions in docstring.
        assert isinstance(description, str)
        if severity is None:
            severity = self.BugSeverity.MEDIUM
        assert isinstance(severity, self.BugSeverity)

        # Report the bug.
        url = f"{self._base_url}/api/common/user_incident/"
        data = {
            'user': self._auth.get_username(),
            'email': self._auth.get_email(),
            # This is a hack.  The location field expects a URL.
            'location': f"{self._base_url}/api",
            'description': description,
            'severity': severity.to_string(),
        }
        curried_request = partial(
            requests.post,
            url=url,
            data=data,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def get_units(self):
        """Get list of QUDT units."""
        url = f"{self._base_url}/api/common/units/"
        curried_request = partial(
            requests.get,
            url=url,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def get_vocab(self):
        """Get AFRL vocabulary (materials properties, etc)."""
        url = f"{self._base_url}/api/common/afrl-vocab/"
        curried_request = partial(
            requests.get,
            url=url,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)

    def update_metadata(
        self,
        metadata_info: Iterable[Mapping[str, Union[str, Iterable[MetadataItem]]]],  # noqa: E501
    ) -> Dict:
        """
        Update metadata for multiple documents at a time.

        Parameters
        ----------
        metadata_info : list-like of dict-like
            Each element must have keys "documentId" and "metadata".
            The values must be a string and valid, API-formatted metadata,
            respective.

        Returns
        -------
        A dict containing a 'message' key.  The message indicates whether
        the request was received successfully.

        Exceptions
        ----------
        TypeError or KeyError will be raised if the input is not valid.
        An APIError will be raised if there is a problem with the API call.
        """
        # Validate inputs.
        if not isinstance(metadata_info, Iterable):
            raise TypeError('metadata_info must be iterable')

        for element in metadata_info:
            if not isinstance(element, Mapping):
                raise TypeError('Each item in metadata_info must be a dict')

            if "documentId" not in element:
                raise KeyError(
                    "Each element of metadata_info must have a 'documentId' "
                    "key"
                )

            if (
                not element["documentId"]
                or
                not isinstance(element["documentId"], str)
            ):
                raise ValueError(
                    "The value of 'documentId' must be a non-empty string"
                )

            if "metadata" not in element:
                raise KeyError("Each item must have a 'metadata' key")

            if not isinstance(element["metadata"], Iterable):
                raise TypeError("The value of 'metadata' must be an Iterable")

            element["metadata"] = to_api_format(element["metadata"])

        url = f"{self._base_url}/api/common/v1/update-metadata/"
        data = {"metadataInfo": metadata_info}
        curried_request = partial(
            requests.patch,
            url=url,
            json=data,
        )
        r = self.attempt_api_call(curried_request=curried_request)

        if r.status_code < ERROR_THRESHOLD:
            return r.json()
        else:
            self._report_api_error(response=r)
