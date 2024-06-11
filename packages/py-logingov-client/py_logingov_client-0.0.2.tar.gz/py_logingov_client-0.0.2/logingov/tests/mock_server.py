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
from urllib.parse import urlparse, parse_qsl, urljoin, urlencode

# Imports from Third Party Modules
import jwt
from jwcrypto import jwk
from jwcrypto.common import json_decode

# Imports from Django

# Local Imports
from logingov.helpers import encode_left128bits

# Setup

# Constants
BASE_URL = 'http://testserver'

DISCOVERY = {'acr_values_supported': [
    'http://idmanagement.gov/ns/assurance/loa/1',
    'http://idmanagement.gov/ns/assurance/loa/3',
    'http://idmanagement.gov/ns/assurance/ial/1',
    'http://idmanagement.gov/ns/assurance/ial/2',
    'http://idmanagement.gov/ns/assurance/ial/0',
    'http://idmanagement.gov/ns/assurance/ial/2?strict=true',
    'urn:gov:gsa:ac:classes:sp:PasswordProtectedTransport:duo',
    'http://idmanagement.gov/ns/assurance/aal/2',
    'http://idmanagement.gov/ns/assurance/aal/3',
    'http://idmanagement.gov/ns/assurance/aal/3?hspd12=true',
    'http://idmanagement.gov/ns/assurance/aal/2?phishing_resistant=true',
    'http://idmanagement.gov/ns/assurance/aal/2?hspd12=true'
],
    'claims_supported': [
        'iss',
        'sub',
        'email',
        'email_verified',
        'all_emails',
        'address',
        'phone',
        'phone_verified',
        'given_name',
        'family_name',
        'birthdate',
        'verified_at',
        'social_security_number',
        'x509_subject',
        'x509_presented',
        'x509_issuer'
    ],
    'grant_types_supported': ['authorization_code'],
    'response_types_supported': ['code'],
    'scopes_supported': [
        'email',
        'all_emails',
        'openid',
        'profile:verified_at',
        'x509',
        'x509:subject',
        'x509:issuer',
        'x509:presented',
        'address',
        'phone',
        'profile',
        'profile:name',
        'profile:birthdate',
        'social_security_number'
    ],
    'subject_types_supported': ['pairwise'],
    'authorization_endpoint': f'{BASE_URL}/openid_connect/authorize',
    'issuer': BASE_URL,
    'jwks_uri': f'{BASE_URL}/api/openid_connect/certs',
    'service_documentation': 'https://developers.login.gov/',
    'token_endpoint': f'{BASE_URL}/api/openid_connect/token',
    'userinfo_endpoint': f'{BASE_URL}/api/openid_connect/userinfo',
    'end_session_endpoint': f'{BASE_URL}/openid_connect/logout',
    'id_token_signing_alg_values_supported': ['RS256'],
    'token_endpoint_auth_methods_supported': ['private_key_jwt'],
    'token_endpoint_auth_signing_alg_values_supported': ['RS256']
}

USER_PAYLOAD = {
    'address': {
        'formatted': '123 Main St Apt 123\nWashington, DC 20001',
        'street_address': '123 Main St Apt 123',
        'locality': 'Washington',
        'region': 'DC',
        'postal_code': '20001'
    },
    'birthdate': '1970-01-01',
    'email': 'test@example.com',
    'email_verified': True,
    'all_emails': ['test@example.com', 'test2@example.com'],
    'family_name': 'Smith',
    'given_name': 'John',
    'phone': '+18881112222',
    'phone_verified': True,
    'social_security_number': '111223333',
    'sub': 'test-uuid',
    'verified_at': 1577854800
}
SCOPE = {
    'email': ['email', 'email_verified'],
    'profile': ['family_name', 'given_name', 'birthdate'],
    'profile:name': ['family_name', 'given_name'],
    'profile:verified_at': ['verified_at'],
    'address': ['address'],
    'phone': ['phone'],
    'social_security_number': ['social_security_number']
}
# Data Structure Definitions

# Private Functions


# Public Classes and Functions
class MockResponse:
    def __init__(self, json_rsp, status_code):
        self.json_rsp = json_rsp
        self.status_code = status_code

    def json(self):
        return self.json_rsp


class MockOIDCServer(object):
    authorized = {}

    def __init__(self, client_id, public_key, redirect_uri, algo=None):
        self.jwk = jwk.JWK.generate(kty='RSA', size=4096)
        self.pk_attrs = json_decode(self.jwk.export_public())
        self.pk_pem = self.jwk.export_to_pem(True, None).decode('utf-8')
        self.pub_jwk = jwk.JWK()
        self.pub_jwk.import_key(**self.pk_attrs)
        self.pub_key = self.pub_jwk.export_public(True)
        self.client_registry = {
            client_id: {
                'key': public_key,
                'redirect_uri': redirect_uri,
            }
        }
        self.signing_algo = algo if algo else 'RS256'

    @staticmethod
    def _nested_find(data, nested_key, nested_val):
        for top_key, sub_dict in data.items():
            lookup = sub_dict.get(nested_key)
            if lookup == nested_val:
                return data[top_key]
        return None

    @property
    def routes(self):
        return {
            f'{BASE_URL}/.well-known/openid-configuration': self.discovery,
            DISCOVERY['authorization_endpoint']: self.authorize,
            DISCOVERY['jwks_uri']: self.keys,
            DISCOVERY['token_endpoint']: self.token,
            DISCOVERY['userinfo_endpoint']: self.userinfo,
        }

    def route_request(self, uri, data=None, headers=None, params=None):
        route = uri.split('?')[0]
        route_method = self.routes[route]
        return route_method(data=data, headers=headers, params=params)

    def discovery(self, *args, **kwargs):
        return MockResponse(DISCOVERY, 200)

    def authorize(self, uri, **kwargs):
        query = urlparse(uri).query
        query = OrderedDict(parse_qsl(query))
        client = self.client_registry.get(query['client_id'])
        if not client or query['redirect_uri'] != client['redirect_uri']:
            params = {
                'error': 'invalid_request ',
                'error_description': 'invalid request'
            }
        else:
            code = secrets.token_hex(16)
            scope = query['scope'].replace('+', ' ').split(' ')
            self.authorized[code] = {
                'client_id': query['client_id'],
                'state': query['state'],
                'nonce': query['nonce'],
                'acr': query['acr_values'],
                'scope': scope,
                'access_token': secrets.token_hex(16),
            }
            params = {'code': code, 'state': query['state']}
        uri = urljoin(query['redirect_uri'], f'?{urlencode(params)}')
        return uri

    def keys(self, *args, **kwargs):
        return MockResponse(
            {
                'keys': [
                    {
                        **self.pub_key,
                        'kid': self.pub_jwk.thumbprint(),
                    }
                ]
            },
            200
        )

    def token(self, data=None, *args, **kwargs):
        code = data['code']
        auth = self.authorized.get(code)
        if not auth:
            return MockResponse(
                {'error': 'invalid code'},
                400
            )
        client = self.client_registry[auth['client_id']]
        client_assertion = data['client_assertion']
        client_jwt = jwt.decode(
            client_assertion, client['key'],
            algorithms=[self.signing_algo],
            options={'verify_signature': False}
        )
        id_params = {
            'iss': BASE_URL,
            'sub': 'test-uuid',
            'aud': auth['client_id'],
            'acr': auth['acr'],
            'at_hash': encode_left128bits(auth['access_token']),
            'c_hash': encode_left128bits(code),
            'exp': time.time() + 60,
            'iat': time.time(),
            'jti': client_jwt['jti'],
            'nbf': time.time(),
            'nonce': auth['nonce']
        }
        id_token = jwt.encode(
            id_params, self.pk_pem, algorithm=self.signing_algo,
            headers={"kid": self.pub_jwk.thumbprint()},
        )
        rsp = {
            'id_token': id_token,
            'expires_in': 60,
            'token_type': 'Bearer',
            'access_token': auth['access_token']
        }
        return MockResponse(rsp, 200)

    def userinfo(self, headers=None, **kwargs):
        token = headers['Authorization'].split(' ')[1]
        auth = self._nested_find(self.authorized, 'access_token', token)
        if not auth:
            return MockResponse({'error': 'invalid token'}, 401)
        payload = {
            'iss': BASE_URL,
        }
        for scope, attrs in SCOPE.items():
            if scope in auth['scope']:
                payload.update({attr: USER_PAYLOAD[attr] for attr in attrs})
        return MockResponse(payload, 200)
