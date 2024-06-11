#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2024- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

"""

# Imports from Standard Library
import os
import secrets
import tempfile
from unittest import TestCase

# Imports from Django

# Local Imports
from logingov.tests.mock_server import BASE_URL
from logingov.settings.oidc_settings import OIDCSettings

# Setup

# Constants

# Data Structure Definitions

# Private Functions


# Public Classes and Functions
class OIDCTests(TestCase):

    def setUp(self):
        self.client_id = secrets.token_urlsafe(16)

        pvt_key_path = os.path.join(tempfile.gettempdir(), 'pvt_key')
        self.redirect_uri = 'http://localhost:8000/oidc/callback'
        self.user_settings = {
            'CLIENT_ID': self.client_id,
            'LOGIN_REDIRECT_URI': self.redirect_uri,
            'PVT_KEY_PATH': pvt_key_path,
            'BASE_URL': BASE_URL,
        }

    def test_check_required_settings(self):
        settings = OIDCSettings()
        self.assertRaises(
            ValueError,
            settings.check_required_settings
        )

        settings = OIDCSettings({
            'CLIENT_ID': self.client_id,
            'LOGIN_REDIRECT_URI': self.redirect_uri
        })
        self.assertRaises(
            ValueError,
            settings.check_required_settings
        )

        settings = OIDCSettings(user_settings=self.user_settings)
        self.assertIsNone(settings.check_required_settings())

    def test_reload(self):
        settings = OIDCSettings(user_settings=self.user_settings)
        self.assertDictEqual(settings.user_settings, self.user_settings)
        self.assertIsNotNone(settings.SCOPE)

        settings.reload()
        self.assertDictEqual(settings.user_settings, {})

    def test_getattr(self):
        settings = OIDCSettings(user_settings={'NOT_A_VALID_SETTING': 'test'})
        self.assertRaises(
            AttributeError,
            settings.__getattr__, 'NOT_A_VALID_SETTING'
        )
