<!--
SPDX-FileCopyrightText: 2024 wmj <wmj.py@gmx.com>

SPDX-License-Identifier: LGPL-3.0-or-later
-->

## Changelog

### 0.10.0

- BREAKING CHANGES!
- Dropped support for python < 3.8. If you need support for old versions, please do not upgrade.
- New subpackage `csb43.aeb43`: CSB43 reimplemented using field descriptors:
    - the original binary record is kept as the internal representation
    - consistent behaviour for field types (money, currency, int, string, etc...)
    - validation failures will raise ValidationException o ValidationWarning depending of their gravity
    - parsing of SEPA transfers and SEPA direct debits information stored in optional items in transactions.
- Subpackage `csb43.csb43` has been deprecated and it will be removed in a future version (and every package object that use it).
- Classes and functions using camel case have been deprecated and they will be removed in a future version.
- Moved package settings from `setup.py` to `pyproject.toml`
- Updated dependencies.

### 0.9.3

- Add support for Python 3.12 (thanks to Cédric Krier)

### 0.9.2

- Fixed setuptool's deprecation warning on python==3.10 (thanks to @mb)
- Fixed duplicated documentation of the same objects by sphinx (thanks to @mb)

### 0.9.1

- Added python_requires >= 3.6 (thanks to Cédric Krier)

### 0.9.0

- Dropped support for Python 2 (thanks to Sergi Almacellas)
- Added support for Python 3.8 and 3.9 (thanks to Sergi Almacellas)
- Added compatibility with tablib >= 1.0.0 (thanks to Sergi Almacellas)
- Type hinting

### 0.8.4

- Fixed tablib requirement (< 1.0.0)
- Fixed parsing of records with code 00 (thanks to Uttam Sharma)

### 0.8.2

- Do not fail with C locale (thanks to Cédric Krier)

### 0.8.1

- Fixed decimal values conversion in JSON and tabular formats (thanks to Harshad Modi).
- Fixed OFX validation (ORIGCURRENCY field).
- An error is raised when the currency code is not found.

### 0.8

- Text values are stored as string instead of bytes (thanks to Sergi Almacellas)
- Warnings are raised using the 'warnings' module.
- An encoding where control characters are different from ascii is not allowed. An exception will be raised.
- csb2format: added encoding as a new parameter.

### 0.7

- Defined installation targets: `yaml` and `formats` (thanks to Sergi Almacellas & Cédric Krier).
- Updated README file (thanks to Sergi Almacellas).
- Removed `simplejson` dependency.
- Dates stored as `date` instead of `datetime` (thanks to Sergi Almacellas).
- Monetary amounts are represented as `Decimal` instead to `float` in order to prevent representation and rounding issues. These fields are exported as a string by default, conversion to float is optional (thanks to Sergi Almacellas & Cédric Krier).
- Added temprary dependency to `openpyxl < 2.5.0` to prevent issue while trying to export to xlsx.

### 0.6

- Fixed usage of pycountry >= 16.10.23rc1 objects (thanks to Alex Barcelo).
- Package refactored to simplify the structure.

### 0.5

- Fixed conversion to binary formats in python 2.
- `tablib` backend supported in python 3.
- N43 warnings are silenced by default.

### 0.4

- OFX v 1.0.3 supported.
- OFX Tag inv401source renamed to inv401ksource.
- Unique transaction id when generating OFX file (thanks to Julien Moutte).

### 0.3.4

- Most Spanish N43 files will use LATIN-1 encoding not pure ASCII (thanks to Julien Moutte).
- Regular expression to check for account name is too limited (thanks to Julien Moutte).
- Reference1 can hold non numerical data in information mode 1 and 2 (thanks to Julien Moutte).
- Currency data as an inmutable list.

### 0.3.3

- Fixed deficiencies in OFX conversion (thanks to Andrea Santambrogio). Checked XML validation against OFX2_Protocol.xsd

### 0.3

- Compatible with Python 3 (except "tablib" dependencies)

### 0.2.3

- Fixed shebang header of csb2format


### 0.2.2

- csb2format adapted to pyinstaller
- Executable file for Windows

### 0.2.1

- Trivial changes

### 0.2

- Several bugfixes
- Bidirectional use of objects (file -> object, object -> file)
- Added conversion to spreadsheets, dict and tabular formats (thanks to tablib)
- Localization to Spanish
- Sphinx documentation

### 0.1

- Initial release


