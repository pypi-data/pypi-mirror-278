#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2024- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

Settings for py-logingov-client are all namespaced in the
LOGIN_GOV_OIDC setting.
For example your project's `settings.py` file might look like this:

LOGIN_GOV_OIDC = {
}

This module provides the `oidc_setting` object, that is used to access
py-logingov settings, checking for user settings first, then falling
back to the defaults."""

# Imports from Standard Library

# Imports from Third Party Modules

# Imports from Django
try:                                                         # pragma: no cover
    from django.conf import settings
    from django.core.signals import setting_changed
except ImportError:
    settings = None

# Local Imports

# Setup

# Constants
DEFAULTS = {
    'CLIENT_ID': '',
    'LOGIN_REDIRECT_URI': '',
    'LOGOUT_REDIRECT_URI': '',
    'PVT_KEY_PATH': '',
    'PVT_KEY_PEM': '',
    'ACR_VALUES': 'http://idmanagement.gov/ns/assurance/ial/1',
    'SCOPE': 'openid email',
    'PROMPT': 'select_account',
    'RESPONSE_TYPE': 'code',
    'GRANT_TYPE': 'authorization_code',
    'CLIENT_ASSERTION_TYPE': (
        'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    ),
    'SIGNING_ALGORITHM': 'RS256',
    'DISCOVERY_ENDPOINT': '.well-known/openid-configuration',
    'ENVIRONMENT': 'sandbox',
    'BASE_URL': '',
    'ACCEPTED_LOCALES': ['es', 'fr']
}
REQUIRED_SETTINGS = (
    'CLIENT_ID',
    'LOGIN_REDIRECT_URI',
    'SCOPE',
    'ACR_VALUES'
)
ALTERNATE_REQUIRED_SETTINGS = (
    ('PVT_KEY_PATH', 'PVT_KEY_PEM'),
    ('ENVIRONMENT', 'BASE_URL')
)
# Data Structure Definitions

# Private Functions


# Public Classes and Functions
class OIDCSettings:
    """
    A settings object, that allows settings to be accessed as properties.
    For example:

        from django_logingov_oidc.settings import oidc_settings
        print(oidc_settings.DEFAULTS)

    For Django usage, settings must be namespaced under
    the `LOGIN_GOV_OIDC` name.
    """

    def __init__(self, user_settings=None, defaults=None):
        self._user_settings = user_settings

        self.defaults = defaults or DEFAULTS
        self._registered_attrs = set()

    @property
    def user_settings(self):
        return (
            self._user_settings or getattr(settings, "LOGIN_GOV_OIDC", {})
        )

    def __getattr__(self, attr):
        if attr != 'user_settings' and attr not in self.defaults:
            raise AttributeError(f"Invalid OIDC setting: '{attr}'")
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        self._registered_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def check_required_settings(self):
        """Validates that all required settings are present and not empty"""
        for setting in REQUIRED_SETTINGS:
            setting_val = getattr(self, setting, None)
            if setting_val in ['', None]:
                raise ValueError(f"Setting {setting} must not be empty")
        for keys in ALTERNATE_REQUIRED_SETTINGS:
            vals = [
                getattr(self, setting, None)
                for setting in keys
            ]
            if not any(vals):
                raise ValueError(
                    f'At least one of {", ".join(keys)} must not be empty'
                )

    def reload(self):
        """
        Resets all registered settings to ensure prior set values are not
        lingering when Django settings are changed.
        """
        for attr in self._registered_attrs:
            delattr(self, attr)
        self._registered_attrs.clear()
        self._user_settings = {}


oidc_settings = OIDCSettings(None, DEFAULTS)


def reload_oidc_settings(setting=None, *args, **kwargs):     # pragma: no cover
    if setting == "LOGIN_GOV_OIDC":
        oidc_settings.reload()


if settings:                                                 # pragma: no cover
    setting_changed.connect(reload_oidc_settings)
