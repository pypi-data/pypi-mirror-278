# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

'''Spanish banks' CSB norm 43 converter to OFX, Homebank, json, yaml, xls, xlsx, ods, csv, tsv'''

try:
    from ._version import version, version_tuple
    __version__ = version
    __version_tuple__ = version_tuple
except ImportError:
    __version__ = version = "0.0.0dev0"
    __version_tuple__ = version_tuple = (0, 0, 0, "dev0")

__all__ = ['csb43', 'homebank', 'ofx', 'formats', 'utils']
