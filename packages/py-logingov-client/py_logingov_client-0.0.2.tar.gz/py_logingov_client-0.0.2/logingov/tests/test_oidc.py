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
from collections import OrderedDict
from unittest import TestCase, mock
from urllib.parse import urlparse, parse_qsl

# Imports from Third Party Modules
from jwcrypto import jwk
from jwcrypto.common import json_decode

# Imports from Django

# Local Imports
from logingov.tests.mock_server import MockOIDCServer, BASE_URL, DISCOVERY
from logingov import oidc
# Setup

# Constants

# Data Structure Definitions


# Private Functions
def discovery(self):
    return DISCOVERY


# Public Classes and Functions
class OIDCTests(TestCase):

    def setUp(self):
        self.client_id = secrets.token_urlsafe(16)

        pvt_key_path = os.path.join(tempfile.gettempdir(), 'pvt_key')
        self.redirect_uri = 'http://localhost:8000/oidc/callback'
        self.settings = {
            'CLIENT_ID': self.client_id,
            'LOGIN_REDIRECT_URI': self.redirect_uri,
            'LOGOUT_REDIRECT_URI': 'http://localhost:8000/oidc/logout',
            'PVT_KEY_PATH': pvt_key_path,
            'BASE_URL': BASE_URL,
        }
        pkjwk = jwk.JWK.generate(kty='RSA', size=4096)
        pk_attrs = json_decode(pkjwk.export_public())
        self.pk_pem = pkjwk.export_to_pem(True, None).decode('utf-8')
        with open(pvt_key_path, 'w') as file:
            file.write(self.pk_pem)
        pub_jwk = jwk.JWK()
        pub_jwk.import_key(**pk_attrs)
        pub_pem = pub_jwk.export_to_pem().decode('utf-8')
        self.server = MockOIDCServer(
            self.client_id, pub_pem, self.redirect_uri
        )

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test__get_base_url(self):
        settings = dict(self.settings)
        settings['BASE_URL'] = ''
        settings['ENVIRONMENT'] = 'sandbox'
        client = oidc.LoginGovOIDCClient(settings=settings)
        self.assertEqual(client._get_base_url(), oidc.SANDBOX_URL)

        settings['ENVIRONMENT'] = 'production'
        client = oidc.LoginGovOIDCClient(settings=settings)
        self.assertEqual(client._get_base_url(), oidc.PRODUCTION_URL)

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test__validate_settings(self):
        client = oidc.LoginGovOIDCClient(settings=self.settings)
        self.assertIsNone(client._validate_settings())

        settings = dict(self.settings)
        settings['SCOPE'] = 'openid email occupation'
        with self.assertRaises(oidc.LoginGovOIDCConfigurationError) as err:
            _ = oidc.LoginGovOIDCClient(settings=settings)
            self.assertIn('SCOPE', str(err))

        settings = dict(self.settings)
        settings['SIGNING_ALGORITHM'] = 'invalid_value'
        with self.assertRaises(oidc.LoginGovOIDCConfigurationError) as err:
            _ = oidc.LoginGovOIDCClient(settings=settings)
            self.assertIn('SIGNING_ALGORITHM', str(err))

    def test__discovery(self):
        with mock.patch('logingov.oidc.requests.get',
                        side_effect=self.server.route_request):
            client = oidc.LoginGovOIDCClient(settings=self.settings)
            self.assertDictEqual(client.discovery_data, DISCOVERY)

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test_authorize_redirect(self):
        client = oidc.LoginGovOIDCClient(settings=self.settings)
        with self.assertRaises(oidc.LoginGovOIDCConfigurationError):
            _ = client.authorize_redirect

        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings,
            locale='es'
        )
        result = client.authorize_redirect
        self.assertIn(f'state={state}', result)
        self.assertIn(f'nonce={nonce}', result)
        self.assertIn(f'client_id={self.client_id}', result)
        self.assertIn('locale=es', result)

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test__validate_authorization_response(self):
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings
        )
        uri = client.authorize_redirect
        auth_response = self.server.authorize(uri)
        query = urlparse(auth_response).query
        auth_response = OrderedDict(parse_qsl(query))
        result = client._validate_authorization_response(auth_response)
        self.assertIsNone(result)  # no error raised

        # no code in response
        auth_response['code'] = None
        self.assertRaises(
            oidc.LoginGovOIDCAuthorizationError,
            client._validate_authorization_response, auth_response
        )

        # no state in client
        client = oidc.LoginGovOIDCClient(settings=self.settings)
        auth_response['code'] = secrets.token_urlsafe(16)
        self.assertRaises(
            oidc.LoginGovOIDCConfigurationError,
            client._validate_authorization_response, auth_response
        )

        # client state does not match response state
        client = oidc.LoginGovOIDCClient(
            state=secrets.token_urlsafe(16), settings=self.settings
        )
        self.assertRaises(
            oidc.LoginGovOIDCAuthorizationError,
            client._validate_authorization_response, auth_response
        )

        # unregistered client ID
        settings = dict(self.settings)
        settings['CLIENT_ID'] = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=settings
        )
        uri = client.authorize_redirect
        auth_response = self.server.authorize(uri)
        query = urlparse(auth_response).query
        auth_response = OrderedDict(parse_qsl(query))
        self.assertRaises(
            oidc.LoginGovOIDCAuthorizationError,
            client._validate_authorization_response, auth_response
        )

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test_token_response(self):
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)

        # missing authorization_response
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings
        )

        with self.assertRaises(oidc.LoginGovOIDCConfigurationError):
            _ = client.token_response

        # valid response
        uri = client.authorize_redirect
        auth_response = self.server.authorize(uri)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                result = client.token_response
                self.assertIn('id_token', result)

        # valid response with pem instead of path
        settings = dict(self.settings)
        settings['PVT_KEY_PATH'] = ''
        settings['PVT_KEY_PEM'] = self.pk_pem
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                result = client.token_response
                self.assertIn('id_token', result)

        # invalid id_token (invalid aud)
        settings = dict(self.settings)
        settings['CLIENT_ID'] = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce,
            settings=settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                with self.assertRaises(oidc.LoginGovOIDCInvalidTokenError):
                    _ = client.token_response

        # no nonce
        client = oidc.LoginGovOIDCClient(
            state=state, settings=self.settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                with self.assertRaises(oidc.LoginGovOIDCConfigurationError):
                    _ = client.token_response

        # invalid nonce
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=secrets.token_urlsafe(16),
            settings=self.settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                with self.assertRaises(oidc.LoginGovOIDCInvalidTokenError):
                    _ = client.token_response

        # invalid code
        query = urlparse(auth_response).query
        auth_response = OrderedDict(parse_qsl(query))
        auth_response['code'] = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                with self.assertRaises(oidc.LoginGovOIDCRequestError):
                    _ = client.token_response

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test_userinfo_id_token(self):
        state = secrets.token_urlsafe(16)
        nonce = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings
        )
        uri = client.authorize_redirect
        auth_response = self.server.authorize(uri)
        client = oidc.LoginGovOIDCClient(
            state=state, nonce=nonce, settings=self.settings,
            authorization_response=auth_response
        )
        with mock.patch('logingov.oidc.requests.post',
                        side_effect=self.server.route_request):
            with mock.patch('logingov.oidc.requests.get',
                            side_effect=self.server.route_request):
                result = client.userinfo_id_token
                self.assertIn('email', result[0])

    @mock.patch.object(oidc.LoginGovOIDCClient, '_discovery', discovery)
    def test_logout_redirect(self):
        state = secrets.token_urlsafe(16)
        client = oidc.LoginGovOIDCClient(
            state=state, settings=self.settings
        )
        result = client.logout_redirect
        self.assertIn(f'client_id={self.client_id}', result)

        settings = dict(self.settings)
        settings['LOGOUT_REDIRECT_URI'] = ''

        client = oidc.LoginGovOIDCClient(
            state=state, settings=settings
        )
        with self.assertRaises(oidc.LoginGovOIDCConfigurationError):
            _ = client.logout_redirect
