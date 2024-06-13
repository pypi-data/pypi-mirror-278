"""
Authentication classes used to interact with the HyperThought API.

Each app in HyperThought will have an associated API class in this package.
For example, the files app has hyperthought.api.files.FilesAPI.
These API classes are initialized with a self-refreshing auth object,
as defined below.

Two auth objects are available:  TokenAuthentication and ClientAuthentication.
The first receives encoded information from the profile page in HyperThought,
uses a bearer token to authenticate API calls, and automatically updates the
bearer token internally using a refresh token.  The second uses a client id
and secret.
"""

import abc
import base64
from datetime import datetime
from datetime import timedelta
import json
import sys
from threading import Thread
import time
from warnings import warn

import dateutil.parser
from dateutil.tz import tzlocal
import requests
import urllib3


# Attempt to refresh token if time to live is fewer than this many seconds.
REFRESH_WINDOW = 300

# Sleep time between refresh attempts.
REFRESH_RETRY_SLEEP_TIME = 1

# Disable insecure request warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AuthExpirationException(Exception):
    pass


class ManualTokenRefreshNotSpecifiedException(Exception):
    """
    To be called when a user attempts to manually refresh a token
    on a TokenAuthentication object for which manual refresh has not been
    specified.
    """
    pass


class Authentication(abc.ABC):
    """
    Abstract base class for authentication classes.  Defines common interface.
    """

    def __init__(self, verify=True):
        self._verify = verify

    @property
    def verify(self):
        return self._verify

    @abc.abstractmethod
    def get_headers():
        pass

    @abc.abstractmethod
    def get_base_url():
        pass


class TokenAuthentication(Authentication):
    """
    Authentication manager for token-based access to HyperThought API.

    Parameters
    ----------
    auth_payload : str
        Base-64 encoded text containing a dict with authorization info.
    verify : bool
        SSL verification, set to True by default.
    manual_refresh : bool
        If True, the client will be responsible for refreshing the token
        using the `refresh` method.  This must be done before the token
        expires.
    delayed_refresh : bool
        This parameter is mainly useful for unit tests.  Accept the default
        (False) otherwise.
        The default behavior is to refresh the auth token immediately, so that
        refresh failures can be detected and users will not have such a failure
        an hour into a long-running script.  Unit tests rely on an auth string,
        which will not be valid for subsequent tests if the token is refreshed.

    Public methods
    --------------
    *   get_headers
    *   get_base_url
    *   get_username
    *   get_first_name
    *   get_last_name
    *   get_email

    Usage
    -----
    1.  Go to the My Account page in HyperThought.  Copy the API Access code
        to the clipboard.
    2.  Instantiate an Authentication object using this code as the parameter
        value (auth_payload argument).
    3.  Make calls to the API using headers obtained from the get_headers
        method, as well as the verify property.
    4.  If using this module from an application (e.g. HyperDrive), use
        get_base_url to construct urls and the remaining methods (get_username,
        get_first_name, get_last_name, get_email) to get information on the
        currently logged-in user.
    """

    # Expected fields in the auth payload parameter.
    EXPECTED_AUTH_FIELDS = (
        'baseUrl',          # Base URL for HyperThought instance.
        'clientId',         # ID for auth client.
        'clientSecret',     # Needed for token refresh.
        'accessToken',      # Access token used to HyperThought endpoints.
        'expiresIn',        # Seconds to expiration for access token.
        'expiresAt',        # Time of expiration for access token.
        'refreshToken',     # Token to refresh access / get a new access token.
    )

    def __init__(
        self,
        auth_payload,
        verify=True,
        manual_refresh=False,
        delayed_refresh=False,
    ):
        super().__init__(verify)
        self._delayed_refresh = bool(delayed_refresh)
        self._manual_refresh = bool(manual_refresh)
        auth_payload = json.loads(base64.b64decode(auth_payload))

        # TODO:  Improve upon parameter validation.
        for field in self.EXPECTED_AUTH_FIELDS:
            assert field in auth_payload

        self._base_url = auth_payload['baseUrl']

        # TODO:  Is this needed?
        if '127.0.0.1' in self._base_url:
            self._base_url = self._base_url.replace('127.0.0.1', 'localhost')

        self._token_url = f'{self._base_url}/openid/token/'
        self._client_id = auth_payload['clientId']
        self._client_secret = auth_payload['clientSecret']
        self._access_token = auth_payload['accessToken']
        self._refresh_token = auth_payload['refreshToken']
        self._user_info = None

        # Time to sleep prior to requesting an access token refresh.
        self._expiration_time = dateutil.parser.parse(
            auth_payload['expiresAt'])
        current_time = datetime.now(tzlocal())
        time_delta = self._expiration_time - current_time
        self._seconds_to_expiration = time_delta.total_seconds()

        # Start a thread to refresh the token automatically, as needed.
        if not self._manual_refresh:
            self._refresh_thread = Thread(target=self._auto_refresh)
            self._refresh_thread.setDaemon(True)
            self._refresh_thread.start()

    @property
    def expiration_time(self):
        return self._expiration_time

    @property
    def seconds_to_expiration(self):
        return self._seconds_to_expiration

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        if not self._manual_refresh:
            raise ManualTokenRefreshNotSpecifiedException(
                "Manual reset not specified.  Reset not allowed.")

        self._access_token = value

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        if not self._manual_refresh:
            raise ManualTokenRefreshNotSpecifiedException(
                "Manual refresh not specified.  Reset not allowed.")

        self._refresh_token = value

    def get_base_url(self):
        """Get the base url for the auth client."""
        return self._base_url

    def get_base_url_dns(self):
        """Get the base url DNS for the auth client."""
        if '//' in self._base_url:
            split_dns_name = self._base_url.split('//')[1].split(':')

            if len(split_dns_name) > 1:
                return '.'.join(split_dns_name)

            return split_dns_name[0]
        else:
            return self._base_url

    def get_headers(self):
        """Get headers for authenticated REST API requests."""
        return {
            'Authorization': f'Bearer {self._access_token}'
        }

    def _set_user_info(self):
        """Set self._user_info by calling the userinfo endpoint."""
        url = '{}/api/auth/userinfo/'.format(self._base_url)
        r = requests.get(
            url=url,
            headers=self.get_headers(),
            verify=self.verify,
        )

        if r.status_code >= 400:
            raise Exception('Unable to set user info.')

        self._user_info = r.json()

    def get_username(self):
        """Get the username associated with the currently logged in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['username']

    def get_first_name(self):
        """Get the first name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['first_name']

    def get_last_name(self):
        """Get the last name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['last_name']

    def get_email(self):
        """Get the email address of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['email']

    def refresh(self, max_attempts=15):
        """
        Manually refresh auth token.

        This function will only work if it is called before the current token
        expires, and manual token refresh has been specified in the constructor
        parameters.
        """
        if not self._manual_refresh:
            raise ManualTokenRefreshNotSpecifiedException(
                "Manual refresh not specified.")

        refreshed = False
        attempts = 0

        while not refreshed and attempts < max_attempts:
            attempts += 1

            if self._seconds_to_expiration < 0:
                raise AuthExpirationException(
                    "Unable to authenticate with expired token")

            # Request object, defined here for post-loop error handling.
            r = None

            data = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }

            r = requests.post(
                url=self._token_url,
                data=data,
                verify=self.verify,
            )

            if r.status_code >= 400:
                time.sleep(REFRESH_RETRY_SLEEP_TIME)
                continue

            auth_info = r.json()
            self._access_token = auth_info['access_token']
            self._refresh_token = auth_info['refresh_token']
            self._seconds_to_expiration = auth_info['expires_in']
            self._expiration_time = datetime.now(tzlocal()) + timedelta(
                seconds=self._seconds_to_expiration)
            refreshed = True

        if not refreshed:
            raise AuthExpirationException(
                "Unable to refresh token. "
                f"Call to {self._token_url} has failed. "
                f"Status code: {r.status_code}. "
                f"Response: {r.content.decode()}."
            )

    def _auto_refresh(self):
        """
        Automatically refresh the token.

        This method is the target of a separate execution thread.
        It should run as long as the client application is running, to ensure
        that the user is continuously authorized.
        """
        if self._seconds_to_expiration < 0:
            raise AuthExpirationException(
                "Unable to authenticate with expired token")

        # Request object, defined here for post-loop error handling.
        r = None

        def remaining_time():
            """Time remaining until token expiration, in seconds."""
            return (
                self._expiration_time - datetime.now(tzlocal())
            ).total_seconds()

        while remaining_time() >= 0:
            if self._delayed_refresh:
                sleep_time = max(
                    self._seconds_to_expiration - REFRESH_WINDOW, 0)
                time.sleep(sleep_time)
                # Delayed refresh is only relevant for the first loop
                # iteration.
                self._delayed_refresh = False

            data = {
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self._refresh_token,
            }

            r = requests.post(
                url=self._token_url,
                data=data,
                verify=self.verify,
            )

            if r.status_code >= 400:
                time.sleep(REFRESH_RETRY_SLEEP_TIME)
                continue

            auth_info = r.json()
            self._access_token = auth_info['access_token']
            self._refresh_token = auth_info['refresh_token']
            self._seconds_to_expiration = auth_info['expires_in']
            self._expiration_time = datetime.now(tzlocal()) + timedelta(
                seconds=self._seconds_to_expiration)
            sleep_time = max(self._seconds_to_expiration - REFRESH_WINDOW, 0)
            time.sleep(sleep_time)

        if r is not None:
            raise AuthExpirationException(
                "Unable to refresh token. "
                f"Call to {self._token_url} has failed. "
                f"Status code: {r.status_code}. "
                f"Response: {r.content.decode()}."
            )


class Authorization(TokenAuthentication):
    """
    Deprecated Authentication manager for token-based access to HyperThought
    API, maintained for backwards compatibility.  Deprecated as of version
    0.9.26.4, replaced by TokenAuthentication.
    """
    def __init_subclass__(cls, **kwargs):
        """This throws a deprecation warning on subclassing."""
        warn(f'{cls.__name__} is deprecated. Use TokenAuthentication instead',
             DeprecationWarning, stacklevel=2)
        super().__init_subclass__(**kwargs)

    def __init__(self, auth_payload, verify=True, delayed_refresh=False):
        """This throws a deprecation warning on initialization."""
        warn(f'{self.__class__.__name__} is deprecated. '
             'Use TokenAuthentication instead.',
             DeprecationWarning, stacklevel=2)
        super().__init__(auth_payload, verify, delayed_refresh)


class ClientAuthentication(Authentication):
    """
    Authentication manager for OIDC client-based access to HyperThought API.

    Parameters
    ----------
    client_id : str
        The service account client id.
    client_secret : str
        The service account client secret.
    auth_base_url : str
        The base url of the HyperThought workspace that the service account
        is linked to.
    verify : bool
        Determine whether SSL verification will be used.
    """

    def __init__(self, client_id, client_secret, auth_base_url, verify=True):
        super().__init__(verify)
        self._auth_post_data = "grant_type=client_credentials"
        self._auth_content_type = "application/x-www-form-urlencoded"

        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_base_url = auth_base_url.rstrip("/")
        self._auth_target_url = f"{self._auth_base_url}/openid/token/"

        # These data members will be set by self._update_auth,
        # which will be called as needed by self.get_headers.
        self._access_token = None
        self._expiration = None

        self._user_info = None

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def auth_base_url(self):
        return self._auth_base_url

    def get_headers(self):
        """Get headers for authenticated REST API requests."""

        if self._is_expired():
            self._update_auth()

        return {
            'Authorization': f'Bearer {self._access_token}'
        }

    def get_base_url(self):
        """Get the base url for the auth client."""
        return self._auth_base_url

    def get_base_url_dns(self):
        """Get the base url DNS for the auth client."""
        if '//' in self._auth_base_url:
            split_dns_name = self._auth_base_url.split('//')[1].split(':')

            if len(split_dns_name) > 1:
                return '.'.join(split_dns_name)

            return split_dns_name[0]
        else:
            return self._auth_base_url

    def _update_auth(self):
        """
        Update bearer token used for authentication.

        The bootstrap request will yield
        """
        r = requests.post(
            url=self._auth_target_url,
            data=self._auth_post_data,
            headers={
                'Content-Type': self._auth_content_type,
            },
            auth=requests.auth.HTTPBasicAuth(
                self._client_id,
                self._client_secret,
            ),
            verify=self.verify,
        )

        # No need to raise an exception.
        # The expired token will result in an API error when used.
        # Retrying the request will result in another invocation of
        # get_headers, thus another invocation of this method.
        # TODO:  Log error rather than printing it.
        if r.status_code >= 300:
            print(
                f"Authentication failure. Status code: {r.status_code}. "
                f"Response content: {r.content}",
                file=sys.stderr,
                flush=True,
            )
            return

        self._access_token = r.json()['access_token']
        expires_in = r.json()['expires_in']
        now = datetime.now(tzlocal())
        self._expiration = now + timedelta(seconds=int(expires_in))

    def _is_expired(self):
        """Determine whether the current auth token is expired."""
        return (
            self._expiration is None
            or
            self._expiration <= datetime.now(tzlocal())
        )

    def _set_user_info(self):
        """Set self._user_info by calling the userinfo endpoint."""
        url = f"{self.auth_base_url.rstrip('/')}/api/auth/userinfo/"
        r = requests.get(
            url=url,
            headers=self.get_headers(),
            verify=self.verify,
        )

        if r.status_code >= 400:
            raise Exception('Unable to set user info.')

        self._user_info = r.json()

    def get_username(self):
        """Get the username associated with the currently logged in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['username']

    def get_first_name(self):
        """Get the first name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['first_name']

    def get_last_name(self):
        """Get the last name of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['last_name']

    def get_email(self):
        """Get the email address of the currently logged-in user."""
        if not self._user_info:
            self._set_user_info()

        return self._user_info['email']
