#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2024- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

"""

# Imports from Standard Library
import secrets
import time
from collections import OrderedDict
from urllib.parse import urljoin, urlencode, urlparse, parse_qsl

# Imports from Third Party Modules
import jwt
import requests
from jwcrypto import jwk

# Local Imports
from logingov.settings.oidc_settings import (
    oidc_settings,
    OIDCSettings,
    DEFAULTS
)
from logingov.helpers import load_private_key, encode_left128bits

# Setup

# Constants
SANDBOX_URL = 'https://idp.int.identitysandbox.gov/'
PRODUCTION_URL = 'https://secure.login.gov/'
CONFIG_SETTINGS_ATTRIBS = {
    'ACR_VALUES': 'acr_values_supported',
    'SIGNING_ALGORITHM': 'token_endpoint_auth_signing_alg_values_supported',
    'GRANT_TYPE': 'grant_types_supported',
    'RESPONSE_TYPE': 'response_types_supported',
    'SCOPE': 'scopes_supported',
}
SPACE_SEPARATED_ATTRIBS = [
    'ACR_VALUES',
    'SCOPE'
]

# Data Structure Definitions

# Private Functions


# Public Classes and Functions
class LoginGovOIDCClientError(Exception):
    pass


class LoginGovOIDCAuthorizationError(LoginGovOIDCClientError):
    """Exception for errors in the Login.gov authorization response"""
    pass


class LoginGovOIDCRequestError(LoginGovOIDCClientError):
    """Exception for raising errors from Login.gov API requests"""
    def __init__(self, error, code, *args, **kwargs):
        self.error = error
        self.code = code
        super().__init__(error, *args)


class LoginGovOIDCInvalidTokenError(LoginGovOIDCClientError):
    """
    Exception for raising errors when Login.gov tokens are invalid
    or cannot be decoded
    """
    pass


class LoginGovOIDCConfigurationError(LoginGovOIDCClientError):
    """
    Exception for raising errors where the provided settings or
    client instantiation parameters are invalid
    """
    pass


class LoginGovOIDCClient(object):
    """
    A client for handling login.gov OIDC requests and responses.
    The client is framework-agnostic, and can be used in any Python
    application that needs to interact with the login.gov OIDC service.

    The client does not generate state or nonce values, or provide for
    storage of these values for use in later calls.  The calling code
    is responsible for generating and managing these values.

    Since the authorization is a redirect to the login.gov site, and the
    response is a redirect back to the client uri, with query params,
    the client does not handle the actual redirect. Therefore, it cannot
    directly call for the authorization response. The calling code must
    handle the redirect and pass the query params to the client, as a
    dict, or query string, for token and user info requests.

    Most of the client parameters are handled via settings. Settings must be
    passed to the client on instantiation as a dict or OIDCSettings instance,
    or may be configured within Django settings under the `LOGIN_GOV_OIDC`
    space (assuming the calling code is a Django app and has added `logingov`
    to the `INSTALLED_APPS`).
    """

    def __init__(self, state=None, nonce=None, locale=None,
                 authorization_response=None, settings=None):
        if isinstance(settings, OIDCSettings):               # pragma: no cover
            self.settings = settings
        else:
            self.settings = OIDCSettings(
                user_settings=settings, defaults=DEFAULTS
            ) if settings else oidc_settings
        self.settings.check_required_settings()

        self.state = state
        self.nonce = nonce
        self.locale = locale
        self.discovery_data = self._discovery()
        self._validate_settings()
        self.code = None
        self.jti = None
        if authorization_response:
            if isinstance(authorization_response, str):
                query = urlparse(authorization_response).query
                authorization_response = OrderedDict(parse_qsl(query))
            self._validate_authorization_response(authorization_response)
            self.code = authorization_response.get('code')

    def _get_base_url(self):
        """
        Get the base url for talking to the login.gov servers
        based on the `ENVIRONMENT` setting or the `BASE_URL` setting.
        """
        base_url = self.settings.BASE_URL
        env = self.settings.ENVIRONMENT
        if base_url:
            return base_url
        else:
            if env.lower().startswith('sand'):
                return SANDBOX_URL
            if env.lower().startswith('prod'):
                return PRODUCTION_URL

    def _discovery(self):
        """
        Uses the base url and DISCOVERY_ENDPOINT to get the OIDC discovery
        data. All other endpoints are pulled from the discovery results,
        rather than being hard-coded, or settings values, to ensure the client
        is always using the most up-to-date login.gov information.
        """
        endpoint = self.settings.DISCOVERY_ENDPOINT
        url = urljoin(self._get_base_url(), endpoint)
        return self.get(url)

    def _validate_settings(self):
        """
        Validates the relevant settings values against the discovery data
        supported values.
        """
        invalid = []
        for setting, config_key in CONFIG_SETTINGS_ATTRIBS.items():
            setting_val = getattr(self.settings, setting)
            config_val = self.discovery_data[config_key]
            if setting in SPACE_SEPARATED_ATTRIBS:
                setting_val = setting_val.split(' ')
                if any([val not in config_val for val in setting_val]):
                    invalid.append(setting)
            elif setting_val not in config_val:
                invalid.append(setting)
        if invalid:
            raise LoginGovOIDCConfigurationError(
                f'The following "LOGIN_GOV_OIDC" settings have values '
                f'that do not match the Login.gov supported values: '
                f'{", ".join(invalid)}'
            )

    def _prepare_authorize_params(self):
        """
        Prepares the query string parameters for inclusion in the authorization
        redirect URL based on provided settings and the client instantiation
        values.
        Both state and nonce are required, and should be setup and managed
        inside the code calling the client.  The same state and nonce will be
        needed again later to validate the authorization and token responses.
        """
        if not self.state or not self.nonce:
            raise LoginGovOIDCConfigurationError(
                'You must provide a state and nonce to the client '
                'to prepare an authorization redirect'
            )
        scope = self.settings.SCOPE.split(' ')
        if 'openid' not in scope:
            scope.insert(0, 'openid')
        params = {
            'acr_values': self.settings.ACR_VALUES,
            'client_id': self.settings.CLIENT_ID,
            'prompt': self.settings.PROMPT,
            'response_type': self.settings.RESPONSE_TYPE,
            'redirect_uri': self.settings.LOGIN_REDIRECT_URI,
            'state': self.state,
            'nonce': self.nonce,
        }
        if self.locale in self.settings.ACCEPTED_LOCALES:
            params['locale'] = self.locale
        return f'?{urlencode(params)}&scope={"+".join(scope)}'

    def _validate_authorization_response(self, auth_response):
        """
        Ensures the authorization response is not an error, contains a code,
        and that the state used to generate the authorization request matches
        the state returned in the response.
        """
        err = auth_response.get('error') or ''
        if err:
            err_desc = auth_response.get('error_description') or ''
            err_msg = ': '.join([err, err_desc])
            raise LoginGovOIDCAuthorizationError(err_msg)
        if not auth_response.get('code'):
            raise LoginGovOIDCAuthorizationError(
                'No authorization code provided'
            )
        if not self.state:
            raise LoginGovOIDCConfigurationError(
                'You must provide the state from your authorization request '
                'to the client to validate the authorization response.'
            )
        if auth_response.get('state') != self.state:
            raise LoginGovOIDCAuthorizationError('Invalid state in response')

    def _prepare_token_assertion(self):
        """Prepares the client assertion JWT for use in the token request."""
        self.jti = secrets.token_hex(16)
        args = {
            'iss': self.settings.CLIENT_ID,
            'sub': self.settings.CLIENT_ID,
            'aud': self.discovery_data['token_endpoint'],
            'jti': self.jti,
            'exp': int(time.time()) + 300,
        }
        if self.settings.PVT_KEY_PATH:
            key = load_private_key(self.settings.PVT_KEY_PATH)
        else:
            key = self.settings.PVT_KEY_PEM
        return jwt.encode(args, key, algorithm=self.settings.SIGNING_ALGORITHM)

    def _prepare_token_params(self):
        """Prepares the POST data for use in the token request."""
        return {
            'client_assertion': self._prepare_token_assertion(),
            'client_assertion_type': self.settings.CLIENT_ASSERTION_TYPE,
            'code': self.code,
            'grant_type': self.settings.GRANT_TYPE,
        }

    def _login_gov_pub_keys(self):
        """
        Gets the login.gov public keys for use in decoding and validating
        the token request response.
        """
        return self.get(self.discovery_data['jwks_uri'])['keys']

    def _decoded_id_token(self, id_token):
        """
        Decodes the ID token using the login.gov public keys.
        A LoginGovOIDCInvalidTokenError will be raised if the ID token cannot
        be decoded, or the aud, iss, exp, nbf, or iat values are determined
        to be invalid during the decoding.
        """
        for key in self._login_gov_pub_keys():
            jwk_key = jwk.JWK(**key)
            pem = jwk_key.export_to_pem().decode('utf-8')
            try:
                return jwt.decode(
                    id_token, pem,
                    algorithms=[self.settings.SIGNING_ALGORITHM],
                    audience=[self.settings.CLIENT_ID],
                    issuer=self.discovery_data['issuer'],
                    leeway=2
                )
            except Exception:
                continue
        else:
            raise LoginGovOIDCInvalidTokenError('Unable to decode ID token')

    def _validated_token(self, tokens):
        """
        Ensures the validity of the token response.
        Raises a LoginGovOIDCInvalidTokenError if the nonce, access token hash,
        code hash, or any of the base JWT values are invalid.
        """
        if not self.nonce:
            raise LoginGovOIDCConfigurationError(
                'You must provide the nonce from your authorization request '
                'to the client to validate the authorization token.'
            )
        id_token = self._decoded_id_token(tokens['id_token'])
        if id_token['nonce'] != self.nonce:
            raise LoginGovOIDCInvalidTokenError('Invalid nonce in ID token')
        if id_token['at_hash'] != encode_left128bits(tokens['access_token']):  # pragma: no cover  # noqa
            raise LoginGovOIDCInvalidTokenError(
                'Invalid access token hash in ID token'
            )
        if id_token['c_hash'] != encode_left128bits(self.code):  # pragma: no cover  # noqa
            raise LoginGovOIDCInvalidTokenError(
                'Invalid code hash in ID token'
            )
        tokens['id_token'] = id_token
        return tokens

    @staticmethod
    def post(url, data):
        """
        Sends a POST request to the provided URL with the provided data,
        handling any error statuses as a LoginGovOIDCRequestError.
        """
        rsp = requests.post(url, data=data)
        if rsp.status_code != 200:
            raise LoginGovOIDCRequestError(
                f'Error {rsp.status_code} from {url}: {rsp.json()["error"]}'
            )
        return rsp.json()

    @staticmethod
    def get(url, params=None, headers=None):
        """
        Sends a GET request to the provided URL with the provided params and/or
        headers, handling any error statuses as a LoginGovOIDCRequestError.
        """
        rsp = requests.get(url, params=params, headers=headers)
        if rsp.status_code != 200:
            raise LoginGovOIDCRequestError(
                f'Error {rsp.status_code} from {url}: {rsp.json()["error"]}'
            )
        return rsp.json()

    @property
    def authorize_redirect(self):
        """Generate the login.gov authorization redirect URI."""
        url = self.discovery_data['authorization_endpoint']
        return urljoin(url, self._prepare_authorize_params())

    @property
    def token_response(self):
        """
        Request tokens from login.gov using the code from
        the authorization login redirect.
        """
        if not self.code:
            raise LoginGovOIDCConfigurationError(
                'You must complete the Login.gov authorization and pass '
                'the results to the client before requesting tokens '
                'or user info.'
            )
        url = self.discovery_data['token_endpoint']
        token_rsp = self.post(url, data=self._prepare_token_params())
        return self._validated_token(token_rsp)

    @property
    def userinfo_id_token(self):
        """
        Request tokens and user info from login.gov using the code from
        the authorization login redirect.
        """
        token_rsp = self.token_response
        headers = {
            'Authorization':
                f'{token_rsp["token_type"]} {token_rsp["access_token"]}'
        }
        url = self.discovery_data['userinfo_endpoint']
        return self.get(url, headers=headers), token_rsp['id_token']

    @property
    def logout_redirect(self):
        """Generate the login.gov logout redirect URI."""
        redirect = self.settings.LOGOUT_REDIRECT_URI
        if not redirect:
            raise LoginGovOIDCConfigurationError(
                'You must configure a LOGOUT_REDIRECT_URI.'
            )
        params = {
            'client_id': self.settings.CLIENT_ID,
            'post_logout_redirect_uri': redirect
        }
        if self.state:
            params['state'] = self.state
        url = self.discovery_data['end_session_endpoint']
        return urljoin(url, f'?{urlencode(params)}')
