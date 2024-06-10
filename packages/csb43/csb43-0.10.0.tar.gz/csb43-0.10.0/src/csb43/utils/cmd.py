#!/usr/bin/env python

# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

# -*- coding: utf-8 -*-
'''
.. note::

    license: GNU Lesser General Public License v3.0 (see LICENSE)

Convert a **CSB/AEB norm 43** file to other file formats.

Supported formats:

- `OFX <http://www.ofx.net/>`_
- `HomeBank CSV <http://homebank.free.fr/help/06csvformat.html>`_
- *HTML*
- *JSON*
- *ODS*: OpenDocument spreadsheet
- *CSV*, *TSV*: comma- or tab- separated values
- *XLS*: Microsoft Excel spreadsheet
- *XLSX*: OOXML spreadsheet
- *YAML*


Examples
----------

- Converting to OFX format:

    ::

        $ csb2format transactions.csb transactions.ofx

        $ csb2format --format ofx transactions.csb transactions.ofx

    or

    ::

        $ csb2format transactions.csb - > transactions.ofx

    From another app to file

    ::

        $ get_my_CSB_transactions | csb2format - transactions.ofx

- Converting to XLSX spreadsheet format:

    ::

        $ csb2format --format xlsx transactions.csb transactions.xlsx


- Using cp850 as the input encoding:

    ::

        $ csb2format --encoding cp850 --format xlsx transactions.csb transactions.xlsx

Spreadsheets
-------------

*ODS* and *XLS* files are generated as books, with the first sheet containing
the accounts information, and the subsequent sheets containing the transactions
of each one of the accounts.

'''
import argparse
import sys
from pathlib import Path
import dataclasses
from functools import partial

from .. import __version__
from .. import csb43 as csb_43, formats as sheet
from ..ofx import converter as ofx
from ..homebank import converter as homebank
from ..i18n import tr as _
from ..aeb43 import Batch, read_batch, get_current_context
from ..aeb43.record.errors import ValidationException


_FORMATS = sorted(list(set(['ofx', 'ofx1', 'homebank'] + sheet.FORMATS)))

_DEFAULT_FORMAT = "ofx" if "ofx" in _FORMATS else _FORMATS[0]


def get_parser() -> argparse.ArgumentParser:
    "argument parser"
    context = get_current_context()
    parser = argparse.ArgumentParser(
        description=_("Convert a CSB43 file to another format"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-v', '--version', dest="version",
        action='version',
        version='%(prog)s ' + __version__
    )

    g_input = parser.add_argument_group("csb43 arguments")
    g_input.add_argument(
        'csb_file',
        type=Path,
        default=sys.stdin,
        help=_("a csb43 file ('-' for stdin)")
    )
    g_input.add_argument(
        '-s', '--strict', action='store_true',
        default=False,
        help=_('strict mode')
    )
    g_input.add_argument(
        '--no-sepa', action="store_false",
        default=True, dest="sepa",
        help=_("do not convert items to SEPA transfers or direct debits")
    )
    g_input.add_argument(
        '-df', '--dayfirst', dest="year_first",
        action='store_false', default=True,
        help=_(
            "use DDMMYY as date format while parsing the"
            " csb43 file instead of YYMMDD"
        )
    )
    g_input.add_argument(
        '-d', '--decimal', type=int,
        default=context.decimals,
        help=_(
            "set the number of decimal places for the money amount type"
        )
    )
    g_input.add_argument(
        '-e', '--encoding', type=str,
        default=csb_43.RecordSequence.ENCODING,
        help=_("set the input encoding ('cp850' for standard AEB file)")
    )
    g_input.add_argument(
        '--use-float',
        action="store_const", const="float", default="str",
        dest="decimal_fallback",
        help=_(
            'export monetary amounts using binary floating point '
            'numbers as a fallback'
        )
    )
    g_input.add_argument(
        '-V', '--verbose', dest="silent",
        action='store_false',
        default=True,
        help=_("show csb43 warnings")
    )

    g_output = parser.add_argument_group("output arguments")
    g_output.add_argument(
        'converted_file',
        type=Path,
        default=Path("-"),
        help=_("destination file ('-' for stdout)")
    )
    g_output.add_argument(
        '-f', '--format', type=str,
        choices=_FORMATS,
        default=_DEFAULT_FORMAT,
        help=_("format of the output file")
    )
    g_output.add_argument(
        '-E', '--output-encoding', type=str,
        default=sys.getdefaultencoding(),
        help=_("set the output encoding")
    )

    return parser


def write_text(path: Path, encoding: str, writer):
    "write to file or stdout"
    if str(path) == "-":
        writer(sys.stdout)
    else:
        with open(path, "wt", encoding=encoding) as stream:
            writer(stream)


def write_homebank(batch: Batch, path: Path, encoding: str):
    "convert to homebank and write to stream"
    write_text(path, encoding, partial(homebank.dump_from_aeb43, batch))


def write_ofx(batch: Batch, path: Path, encoding: str, ofx_mode: str):
    "convert to OFX and write to stream"
    data = ofx.convert_from_aeb43(batch, sgml=ofx_mode == "ofx1")
    write_text(path, encoding, lambda stream: stream.write(str(data)))


def convert(args: argparse.Namespace):
    "CLI: convert AEB43 input to another format"

    # read input
    context = dataclasses.replace(
        get_current_context(),
        strict=args.strict,
        decimals=args.decimal,
        year_first=args.year_first,
        silent=args.silent,
        encoding=args.encoding,
        sepa=args.sepa,
    )
    indent = ""
    if str(args.csb_file) == "-":
        batch = read_batch(sys.stdin.buffer, context=context)
    else:
        indent= "  "
        print(_("* File: {name}").format(name=args.csb_file.name), file=sys.stderr)
        with open(args.csb_file, "rb") as stream:
            batch = read_batch(stream, context=context)

    print(batch.describe(indent=indent), file=sys.stderr)

    # write output
    output_format: str = args.format.lower()

    if output_format in ("ofx", "ofx1"):
        write_ofx(batch, args.converted_file, args.output_encoding, output_format)
    elif output_format == "homebank":
        write_homebank(batch, args.converted_file, args.output_encoding)
    else:
        # tablib-like formats
        tablib_data = sheet.convert_from_aeb43(
            batch, output_format, decimal_fallback=args.decimal_fallback
        )

        content = getattr(tablib_data, output_format)
        if isinstance(content, bytes):
            # binary format
            if str(args.converted_file) == "-":
                raise ValueError(_("stdout not supported for binary formats"))
            with open(args.converted_file, "wb") as bstream:
                bstream.write(content)
        else:
            # text format
            write_text(args.converted_file, args.encoding, lambda stream: stream.write(content))


def main():
    "main function"
    try:
        convert(get_parser().parse_args())
    except ValidationException as e:
        print(str(e), file=sys.stderr)
        return 1

    return 0
