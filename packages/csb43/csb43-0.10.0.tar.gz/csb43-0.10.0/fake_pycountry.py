#!/bin/python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-

import pycountry

if __name__ == '__main__':

    print("# -*- coding: utf-8 -*-")
    print("from __future__ import unicode_literals")
    print("CURRENCY_DATA = [")
    for el in pycountry.currencies:
        alpha_3 = getattr(el, 'alpha_3', None)
        numeric = getattr(el, 'numeric', None)
        print("    %s," % ((alpha_3, numeric),))

    print("]")
    print()
