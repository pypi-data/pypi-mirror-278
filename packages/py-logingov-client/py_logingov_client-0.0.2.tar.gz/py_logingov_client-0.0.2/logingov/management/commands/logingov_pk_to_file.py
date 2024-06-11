#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2023- Earth Advantage.
All rights reserved
..codeauthor::Fable Turas <fable@rainsoftware.tech>

"""

# Imports from Standard Library
import os

# Imports from Django
from django.core.management.base import BaseCommand

from logingov.settings.oidc_settings import oidc_settings

# Setup

# Constants

# Data Structure Definitions

# Private Functions


# Public Classes and Functions
class Command(BaseCommand):
    help = (
        'Write Private Key from env vars, or argument, to file'
    )

    def add_arguments(self, parser):                         # pragma: no cover
        parser.add_argument(
            '-k', '--key',
            help=(
                'Private key string, with escaped line '
                'breaks, to write to file.'
            )
        )
        parser.add_argument(
            '-e', '--env',
            help=(
                'Environment variable name where private key is stored'
            )
        )

    def handle(self, *args, **options):                      # pragma: no cover
        pk = options['key']
        env = options['env'] or 'LOGIN_GOV_OIDC_PVT_KEY'
        pk = pk if pk else os.environ[env]
        pk = pk.replace('\\n', '\n')
        with open(oidc_settings.PVT_KEY_PATH, 'w') as file:
            file.write(pk)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully generated private key file '
                f'at {oidc_settings.PVT_KEY_PATH}'
            ))
