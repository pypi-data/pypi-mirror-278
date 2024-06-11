#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2024- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

"""

# Imports from Standard Library
import base64
import hashlib

# Imports from Third Party Modules

# Imports from Django

# Local Imports

# Setup

# Constants

# Data Structure Definitions

# Private Functions


# Public Classes and Functions
def load_private_key(key_path):
    """load private key from file for encoding."""
    with open(key_path, 'rb') as pem_in:
        return pem_in.read()


def encode_left128bits(string):
    # 128 bits / 8 bits per byte = 16
    # ref https://github.com/18F/identity-idp/blob/799fc62621a30c54e7edba17e376d94606d0c956/app/services/id_token_builder.rb#L69  # noqa
    hashed = hashlib.sha256(string.encode("utf-8")).digest()[0:16]
    b64 = base64.urlsafe_b64encode(hashed)
    return b64.decode("utf-8").rstrip("=")
