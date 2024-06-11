# py-logingov
Python client implementation for the Login.gov SSO

## About
py-logingov provides framework-agnostic support for integrating with the Login.gov SSO (currently only the OIDC protocol with private_key_jwt).
It can be used with any Python based application that needs to authenticate users via the Login.gov SSO,
but there are some convenience integrations for the Django framework.

## Installation
```bash
pip install py-logingov-client
```

## Django Integration (optional)
If you are using the Django framework, and wish to manage LoginGovOIDCClient settings via Django settings,
and/or use the provided Django management command for saving a private key, from a string or env var, to a file,
you will need to add `logingov` to your `INSTALLED_APPS` in your Django settings file and add your settings
under the `LOGIN_GOV_OIDC` namespace (see below for more information about available settings).

```python
INSTALLED_APPS = [
    ...
    'logingov',
    ...
]
```

#### Django Management Command
The `logingov` app provides a management command for saving a private key string to a file.
This is useful for saving the private key to a file, in conjunction with the `PVT_KEY_PATH` setting,
particularly when the private key is stored in an environment variable,
as might be necessary for handling in container deployments.
When storing a private key as and environment variable, you may find it necessary to escape the newlines in the key string. ie (`\n` -> `\\n`).

```bash
# Save private key from key argument to file
python manage.py logingov_pk_to_file --key 'your-private-key-string'

# Save private key from environment variable to file (default env var name is LOGIN_GOV_OIDC_PVT_KEY)
# You may provide a custom environment variable name with the --env option
python manage.py logingov_pk_to_file --env LOGIN_GOV_OIDC_PVT_KEY

```

## LoginGovOIDCClient Usage

### Settings
The `LoginGovOIDCClient` class requires a number of login.gov specific settings be provided,
either from Django settings (the `LOGIN_GOV_OIDC` namespace),
or on instantiation as a dict or instance of OIDCSettings.

```python
LOGIN_GOV_OIDC = {
    'CLIENT_ID': '',
    'LOGIN_REDIRECT_URI': '',
    'LOGOUT_REDIRECT_URI': '',
    'PVT_KEY_PATH': '',
    'PVT_KEY_PEM': '',
    'ACR_VALUES': 'http://idmanagement.gov/ns/assurance/ial/1',
    'SCOPE': 'openid email',
    'ENVIRONMENT': 'sandbox',
    'BASE_URL': '',
    'PROMPT': 'select_account',
    'RESPONSE_TYPE': 'code',
    'GRANT_TYPE': 'authorization_code',
    'CLIENT_ASSERTION_TYPE': (
        'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    ),
    'SIGNING_ALGORITHM': 'RS256',
    'DISCOVERY_ENDPOINT': '.well-known/openid-configuration',
    'ACCEPTED_LOCALES': ['es', 'fr']
}
```

#### CLIENT_ID
The client ID registered with Login.gov for your application.

#### LOGIN_REDIRECT_URI
The URI to redirect to after a successful login. This must be registered with Login.gov.

#### LOGOUT_REDIRECT_URI
The URI to redirect to after a successful logout. Required if you wish to use the `logout_redirect` method.

#### PVT_KEY_PATH
The path to the private key file used to sign the JWT assertion. This must match with the public key registered with Login.gov.
You must supply either this setting or `PVT_KEY_PEM`.

#### PVT_KEY_PEM
The private key as a PEM string. This must match with the public key registered with Login.gov.
You must supply either this setting or `PVT_KEY_PATH`.

#### ACR_VALUES
A string containing a space separated list of Login.gov ACR values to specify the type of service level or AAL. Defaults to `http://idmanagement.gov/ns/assurance/ial/1`.
See [Login.gov OIDC documentation](https://developers.login.gov/oidc/authorization) for more information.

#### SCOPE
A string containing a space separated list of the scopes being requested. Defaults to `openid email`.
See [Login.gov OIDC documentation](https://developers.login.gov/attributes/) for more information on available scopes
and the required IAL levels you must set as `ACR_VALUES` for your requested scopes.

#### ENVIRONMENT
The environment to use for the Login.gov OIDC base url for discovery.
Allows the client to select from hard coded values for the login.gov sandbox or production URLs. Valid values: `sandbox`, `production`. Defaults to `sandbox`.
Either this setting or `BASE_URL` must not be empty.

#### BASE_URL
The base URL for the Login.gov OIDC service. Either this setting or `ENVIRONMENT` must not be empty.
Provided to allow for custom URLs in the event the Login.gov URLs change and a package update is not yet available, and for testing purposes.

#### PROMPT
Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `select_account`.

#### RESPONSE_TYPE
Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `code`.

#### GRANT_TYPE
Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `authorization_code`.

#### CLIENT_ASSERTION_TYPE
Required for `private_key_jwt`. Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`.

#### SIGNING_ALGORITHM
Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `RS256`.

#### DISCOVERY_ENDPOINT
The OIDC discovery endpoint. Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `.well-known/openid-configuration`.

#### ACCEPTED_LOCALES
Provided as a configurable setting in the event login.gov changes the required value before a package update can be released. Defaults to `['es', 'fr']`.

#### Required settings
The following settings must not be empty: `CLIENT_ID`, `LOGIN_REDIRECT_URI`, `SCOPE`, `ACR_VALUES`.
At least one of each set of the following settings must not be empty: `PVT_KEY_PATH` or `PVT_KEY_PEM`, `BASE_URL` or `ENVIRONMENT`.

### Client Usage

#### Authorization
The LoginGovOIDCClient provides a method to generate the authorization URL for redirecting users to the Login.gov OIDC service.
Since this is only a redirect URL, it is up to the calling code to handle the redirect at the `LOGIN_REDIRECT_URI`.
The calling code must also handle the creation and management of the state and nonce parameters.
These values are required by the authorization redirect and must be stored for later use in the token exchange.
Each must be unique and at least 22 characters long.
See the [Login.gov OIDC documentation](https://developers.login.gov/oidc/authorization) for more information.

```python
import secrets
from logingov import LoginGovOIDCClient
settings = {
    'CLIENT_ID': 'your-client-id',
    'LOGIN_REDIRECT_URI': 'your-login-redirect-uri',
    'PVT_KEY_PATH': 'your-private-key-path',
}
state = secrets.token_urlsafe(16)
nonce = secrets.token_urlsafe(16)
client = LoginGovOIDCClient(state=state, nonce=nonce, settings=settings)
auth_redirect_url = client.authorize_redirect
```

#### Token Exchange/User Info
The LoginGovOIDCClient provides a method to exchange the authorization code, which is returned from login.gov
as a query parameter in the redirect URL, for an access token and retrieve the user info.
This method requires the authorization response and the state, and nonce from the initiating authorization redirect.
The authorization response must be the query parameters from the redirect URL as either a dict of params
or as a URL query string. (Hint: you may pass the entire login redirect URL to the client.)

You may request the tokens independent of the user info by using the `token_response` property method,
but it is assumed that general usage will require the user info as well.
See the [Login.gov OIDC documentation](https://developers.login.gov/oidc/user-info) for more information 
about the user info response and available scopes.

Note that both the `userinfo_id_token` and `token_response` results include the `id_token` as the decoded JWT.
The decoded JWT includes a `jti` claim that can be used to validate the token against replay attacks.
The LoginGovOIDCClient does not provide a method for this validation, but it is recommended that you implement this in your application.

```python
from logingov import LoginGovOIDCClient

settings = {
    'CLIENT_ID': 'your-client-id',
    'LOGIN_REDIRECT_URI': 'your-login-redirect-uri',
    'PVT_KEY_PATH': 'your-private-key-path',
}
state = your_session_storage.state
nonce = your_session_storage.nonce
auth_response = 'your-login-redirect-uri?state=state-returned-from-login&code=login.gov-provided-code'
client = LoginGovOIDCClient(state=state, nonce=nonce, settings=settings,
                            authorization_response=auth_response)
user_info, tokens = client.userinfo_id_token
```

#### Logout
The LoginGovOIDCClient provides a method to generate the logout URL for redirecting users to the Login.gov OIDC service.
You must provide a `LOGOUT_REDIRECT_URI` in the settings to use this method.
Since this is only a redirect URL, it is up to the calling code to handle the redirect at the `LOGOUT_REDIRECT_URI`.
The state parameter is optional for a logout redirect, but if desired,
must be managed by the calling code, and must be unique and at least 22 characters long.
See the [Login.gov OIDC documentation](https://developers.login.gov/oidc/logout) for more information.

```python
import secrets
from logingov import LoginGovOIDCClient
state = secrets.token_urlsafe(16)
settings = {
    'CLIENT_ID': 'your-client-id',
    'LOGIN_REDIRECT_URI': 'your-login-redirect-uri',
    'LOGOUT_REDIRECT_URI': 'your-logout-redirect-uri',
    'PVT_KEY_PATH': 'your-private-key-path',
}
client = LoginGovOIDCClient(state=state, settings=settings)
logout_redirect_url = client.logout_redirect
```

#### Exceptions
The LoginGovOIDCClient may raise the following exceptions:
- `LoginGovOIDCClientError`: Base exception for all client errors.
- `LoginGovOIDCClientConfigError`: Raised when the client has improperly configured settings and/or instantiation params.
- `LoginGovOIDCClientRequestError`: Raised when there is an error in the request to the Login.gov OIDC service.
- `LoginGovOIDCAuthorizationError`: Raised when there is an error in the authorization response.
- `LoginGovOIDCInvalidTokenError`: Raised when the id_token from login.gov is invalid or cannot be decoded.
