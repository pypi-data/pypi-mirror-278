.. SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
..
.. SPDX-License-Identifier: LGPL-3.0-or-later

Converter
==========

Convert a **CSB/AEB norm 43** file to other file formats.

Supported formats:

- OFX v1.0.3 (SGML) & v2.1.2 (XML)
- `HomeBank CSV <http://homebank.free.fr/help/06csvformat.html>`_
- *JSON*
- *YAML*

Additional formats are optionally provided by `tablib`:

- *HTML*
- *ODS*: OpenDocument spreadsheet
- *CSV*, *TSV*: comma- or tab- separated values
- *XLS*: Microsoft Excel spreadsheet
- *XLSX*: OOXML spreadsheet

For an exhaustive list, see package `tablib`.

Options:
-----------

::

    usage: csb2format [-h] [-v] [-s] [--no-sepa] [-df] [-d DECIMAL] [-e ENCODING] [--use-float] [-V]
                    [-f {csv,dbf,homebank,html,jira,json,latex,ods,ofx,ofx1,rst,tsv,xls,xlsx,yaml}] [-E OUTPUT_ENCODING]
                    csb_file converted_file

    Convert a CSB43 file to another format

    options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit

    csb43 arguments:
    csb_file              a csb43 file ('-' for stdin)
    -s, --strict          strict mode (default: False)
    --no-sepa             do not convert items to SEPA transfers or direct debits (default: True)
    -df, --dayfirst       use DDMMYY as date format while parsing the csb43 file instead of YYMMDD (default: True)
    -d DECIMAL, --decimal DECIMAL
                            set the number of decimal places for the money amount type (default: 2)
    -e ENCODING, --encoding ENCODING
                            set the input encoding ('cp850' for standard AEB file) (default: latin1)
    --use-float           export monetary amounts using binary floating point numbers as a fallback (default: str)
    -V, --verbose         show csb43 warnings (default: True)

    output arguments:
    converted_file        destination file ('-' for stdout)
    -f {csv,dbf,homebank,html,jira,json,latex,ods,ofx,ofx1,rst,tsv,xls,xlsx,yaml}, --format {csv,dbf,homebank,html,jira,json,latex,ods,ofx,ofx1,rst,tsv,xls,xlsx,yaml}
                            format of the output file (default: ofx)
    -E OUTPUT_ENCODING, --output-encoding OUTPUT_ENCODING
                            set the output encoding (default: utf-8)



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


*ODS*, *XLS* and *XLSX* files are generated as books, with the first sheet
containing the accounts information, and the subsequent sheets
containing the transactions of each one of the accounts.



From code
---------


Parse a *CSB43* file and print the equivalent *OFX* file

.. code-block:: python

    # OFX
    from csb43.ofx import converter as ofx_converter
    from csb43.aeb43 import read_batch

    with open("movimientos.csb", "rb") as fd:
        batch = read_batch(fd)

    # print to stdout
    print(ofx_converter.convert_from_aeb43(batch))


Parse a *CSB43* file and print the equivalent in a tabular or
dictionary-like file format

.. code-block:: python

    from csb43 import read_batch, formats

    with open("movimientos.csb", "rb") as fd:
        batch = read_batch(fd)

    # print 'yaml' format to stdout
    o = formats.convert_from_aeb43(batch, 'yaml')
    print(o.yaml)

    # write 'xlsx' format to file
    o = formats.convert_from_aeb43(batch, 'xlsx')
    with open("movimientos.xlsx", "wb") as f:
        f.write(o.xlsx)


Build an AEB43 with a custom context:

.. code-block:: python

    import dataclasses
    from csb43 import read_batch, get_current_context

    # custom context
    ctx = dataclasses.replace(get_current_context(), strict=True)
    with open("movimientos.csb", "rb") as fd:
        batch = read_batch(fd, context=context)

    # scoped context
    with get_current_context().scoped(strict=True):
        with open("movimientos.csb", "rb") as fd:
            batch = read_batch(fd)
