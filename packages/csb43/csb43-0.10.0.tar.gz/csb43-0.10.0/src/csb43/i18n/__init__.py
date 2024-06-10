# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import locale
import gettext

try:
    import importlib_resources
except ImportError:
    from importlib import resources as importlib_resources

# Change this variable to your app name!
#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@DOMAIN_NAME@.mo
DOMAIN_NAME = "messages"

with importlib_resources.as_file(importlib_resources.files(__name__)) as path:
    LOCALE_DIR = path

DEFAULT_LANGUAGES = os.environ.get('LANG', '').split(':')
DEFAULT_LANGUAGES += ['en']

languages = []
try:
    lc, encoding = locale.getlocale()
except ValueError:
    lc, encoding = None, None
if lc:
    languages.append(lc)

languages += DEFAULT_LANGUAGES
mo_location = LOCALE_DIR

gettext.install(DOMAIN_NAME, localedir=None)

gettext.textdomain(DOMAIN_NAME)

#gettext.bind_textdomain_codeset(DOMAIN_NAME, "UTF-8")

language = gettext.translation(
    DOMAIN_NAME,
    mo_location,
    languages=languages,
    fallback=True
)

tr = language.gettext
