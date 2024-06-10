# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
Conversion from AEB43 to dict and tabular formats
"""
from __future__ import annotations
import json
import warnings
from decimal import Decimal
import datetime as dt
from collections import defaultdict

from deprecated.sphinx import deprecated

from .aeb43.batch import Batch
from .aeb43.account import Account
from .aeb43.transaction import Transaction
from .aeb43.fields.information_mode import InformationMode
from .csb43.csb_file import File as CFile
from .csb43.account import Account as CAccount
from .csb43.transaction import Transaction as TTransaction
from .i18n import tr as _
from .utils import messages as msg
from . import utils


class FormatWarning(UserWarning):
    "a warning related to conversion formats"


_ABSTRACT_HEADER = (
    msg.T_BANK_CODE,
    msg.T_BRANCH_CODE,
    msg.T_ACCOUNT_KEY,
    msg.T_ACCOUNT_NUMBER,
    msg.T_INFORMATION_MODE,
    msg.T_SHORT_NAME,
    msg.T_CURRENCY,
    msg.T_INITIAL_DATE,
    msg.T_FINAL_DATE,
    msg.T_INITIAL_BALANCE,
    msg.T_FINAL_BALANCE,
    msg.T_INCOME,
    msg.T_EXPENSES,
    msg.T_INCOME_ENTRIES,
    msg.T_EXPENSES_ENTRIES
)


_TRANSACTION_HEADER = (
    msg.T_BRANCH_CODE,
    msg.T_DOCUMENT_NUMBER,
    msg.T_SHARED_ITEM,
    msg.T_OWN_ITEM,
    msg.T_ITEM_1,
    msg.T_ITEM_2,
    msg.T_REFERENCE_1,
    msg.T_REFERENCE_2,
    msg.T_TRANSACTION_DATE,
    msg.T_VALUE_DATE,
    msg.T_AMOUNT,
    msg.T_ORIGINAL_CURRENCY,
    msg.T_ORIGINAL_AMOUNT
)


_TRANSACTION_HEADER_2 = (
    msg.T_BRANCH_CODE,
    msg.T_DOCUMENT_NUMBER,
    msg.T_SHARED_ITEM,
    msg.T_OWN_ITEM,
    msg.T_ITEM_1,
    msg.T_ITEM_2,
    msg.T_OPTIONAL_ITEMS,
    msg.T_REFERENCE_1,
    msg.T_REFERENCE_2,
    msg.T_TRANSACTION_DATE,
    msg.T_VALUE_DATE,
    msg.T_AMOUNT,
    msg.T_ORIGINAL_CURRENCY,
    msg.T_ORIGINAL_AMOUNT,
    _("SEPA"),
    msg.T_SCHEME_CODE,
    msg.T_CREDITOR_NAME,
    msg.T_CREDITOR_ID,
    msg.T_MANDATE_REFERENCE,
    msg.T_PURPOSE,
    msg.T_PURPOSE_CATEGORY,
    msg.T_REMITANCE_INFORMATION,
    msg.T_CREDITOR_REFERENCE,
    msg.T_DEBTOR_NAME,
    msg.T_ORIGINATOR_NAME,
    msg.T_ORIGINATOR_CODE,
    msg.T_ORIGINATOR_REFERENCE,
    msg.T_ORIGINATOR_REFERENCE_PARTY,
    msg.T_ADDITIONAL_INFO,
)


DECIMAL_SUPPORTED = (
    "ods",
    "xls",
    "xlsx",
    "csv",
    "tsv",
    "df",
    "html",
    "latex",
)

DATE_UNSUPPORTED = (
    "xls",
    "ods",
)


def _dump_date(value: dt.datetime | dt.date | None, fmt: str):
    if (fmt not in DATE_UNSUPPORTED) or (value is None):
        return value
    return utils.export_date(value)


def _abstract_row(acc: Account, fmt: str):
    return (
        acc.bank_code,
        acc.branch_code,
        acc.account_control_key,
        acc.account_number,
        int(acc.information_mode),
        acc.short_name,
        acc.currency.alpha_3,
        _dump_date(acc.initial_date, fmt),
        _dump_date(acc.final_date, fmt),
        acc.initial_balance,
        acc.summary.final_balance if acc.summary else None,
        acc.summary.income if acc.summary else None,
        acc.summary.expense if acc.summary else None,
        acc.summary.income_entries if acc.summary else None,
        acc.summary.expense_entries if acc.summary else None
    )


def _transaction_row(trn: Transaction, fmt, decimal_fallback):
    items = [x for x in (v.strip() for v in trn.iter_optional_items()) if x]
    item1 = items[0] if items else None
    item2 = items[1] if len(items) > 1 else None
    alt_items = "; ".join(items[2:])

    if trn.exchange:
        o_currency = utils.export_currency_code(trn.exchange.original_currency)
        o_amount = utils.export_decimal(trn.exchange.amount, fallback=decimal_fallback)
    else:
        o_currency = None
        o_amount = None

    if trn.sepa_debit:
        purpose = trn.sepa_debit.purpose
        purpose_category = trn.sepa_debit.purpose_category
        remitance_information = trn.sepa_debit.remitance_information
        sepa = _("direct debit")
    elif trn.sepa_transfer:
        purpose = trn.sepa_transfer.purpose
        purpose_category = trn.sepa_transfer.purpose_category
        remitance_information = trn.sepa_transfer.remitance_information
        sepa = _("transfer")
    else:
        purpose = None
        purpose_category = None
        remitance_information = None
        sepa = None

    return (
        trn.branch_code,
        trn.document_number,
        f"{trn.shared_item:02d}",
        f"{trn.own_item:03d}",
        item1,
        item2,
        alt_items,
        trn.reference1,
        trn.reference2,
        _dump_date(trn.transaction_date, fmt),
        _dump_date(trn.value_date, fmt),
        trn.amount,
        o_currency or '',
        o_amount or '',
        sepa,

        trn.sepa_debit.scheme_code if trn.sepa_debit else None,
        trn.sepa_debit.creditor_name if trn.sepa_debit else None,
        trn.sepa_debit.creditor_id if trn.sepa_debit else None,
        trn.sepa_debit.mandate_reference if trn.sepa_debit else None,
        purpose,
        purpose_category,
        remitance_information,
        trn.sepa_debit.creditor_reference if trn.sepa_debit else None,
        trn.sepa_debit.debtor_name if trn.sepa_debit else None,
        trn.sepa_transfer.originator_name if trn.sepa_transfer else None,
        trn.sepa_transfer.originator_code if trn.sepa_transfer else None,
        trn.sepa_transfer.originator_reference if trn.sepa_transfer else None,
        trn.sepa_transfer.originator_reference_party if trn.sepa_transfer else None,
        trn.sepa_transfer.additional_info if trn.sepa_transfer else None,
    )


try:
    import tablib
    #: formats supported by :mod:`tablib`
    if tablib.__version__.startswith("0."):
        # tablib < 1.0.0
        TABLIB_FORMATS = [f.title for f in tablib.formats.available]
    else:
        # tablib >= 1.0.0
        TABLIB_FORMATS = [f.title for f in tablib.formats.registry.formats()]
except ImportError:
    TABLIB_FORMATS = []
    warnings.warn(
        _("Package 'tablib' not found. Formats provided by 'tablib' will not be available."),
        FormatWarning
    )

#: dictionary formats
DICT_FORMATS = ['json']
try:
    import yaml
    DICT_FORMATS.append('yaml')
except ImportError:
    warnings.warn(
        _("Package 'yaml' not found. Hierarchical YAML format will not be available."),
        FormatWarning
    )

#: available formats
FORMATS = list(set(TABLIB_FORMATS + DICT_FORMATS))


def convert_from_aeb43(
    batch: Batch,
    expected_format: str,
    decimal_fallback: str | None = None
):
    '''
    Convert a batch file into a :mod:`tablib` data object or a \
    dictionary-like object

    Args:

        batch : Batch
            an AEB43 batch
        decimal_fallback
            decimal number fallback representation:

            - 'float': use type `float`
            - 'str': represent decimal as a string
            - `None`: use default fallback ('str')

    Returns :class:`tablib.Databook`, :class:`tablib.Dataset` or an object \
    with an attribute named as `expected_format`
    '''
    decimal_supported = expected_format in DECIMAL_SUPPORTED
    d_conversion: str | None = decimal_fallback or 'str'
    if decimal_supported:
        d_conversion = None

    if expected_format in DICT_FORMATS:
        return convert_aeb43_to_dict(batch, expected_format, decimal_fallback=d_conversion)
    return convert_aeb43_to_tabular(batch, expected_format, decimal_fallback=d_conversion)


# pylint: disable=too-few-public-methods
class _TablibSurrogate:
    "mimic behaviour found in tablib converters"

    def __init__(self, string, expected_format):
        setattr(self, expected_format, string)


def _yaml_as_float(dumper, obj):
    return dumper.represent_float(float(obj))


def _yaml_as_str(dumper, obj):
    return dumper.represent_str(str(obj))


def _yaml_enum_as_int(dumper, obj):
    return dumper.represent_int(obj.value)


def _dict_to_yaml(data: dict, decimal_fallback) -> _TablibSurrogate:
    representer = None
    if decimal_fallback == "float":
        representer = _yaml_as_float
    elif decimal_fallback == "str":
        representer = _yaml_as_str
    elif decimal_fallback:
        raise ValueError(f"fallback={repr(decimal_fallback)}")

    if representer:
        yaml.representer.SafeRepresenter.add_representer(Decimal, representer)

    yaml.representer.SafeRepresenter.add_representer(
        InformationMode,
        _yaml_enum_as_int
    )

    yaml.representer.SafeRepresenter.add_representer(
        utils.currency.CurrencyLite,
        utils.currency.yaml_currency_representer
    )

    return _TablibSurrogate(yaml.safe_dump(data), "yaml")


class CsbJsonEncoder(json.JSONEncoder):
    "a JSON encoder ready for currency and dates"
    def default(self, o):
        if isinstance(o, (dt.datetime, dt.date)):
            return str(o)
        if utils.currency.is_currency(o):
            return o.numeric
        return super().default(o)

def _dict_to_json(data: dict, decimal_fallback) -> _TablibSurrogate:
    class _Encoder(CsbJsonEncoder):
        def default(self, o):
            if not isinstance(o, Decimal):
                return super().default(o)
            if decimal_fallback == "float":
                return float(o)
            if decimal_fallback == "str":
                return str(o)
            if decimal_fallback:
                raise ValueError(f"fallback={repr(decimal_fallback)}")
            return super().default(o)

    return _TablibSurrogate(json.dumps(data, indent=1, cls=_Encoder), "json")


def convert_aeb43_to_dict(
    batch: Batch,
    expected_format: str = "json",
    decimal_fallback=None
) -> _TablibSurrogate:
    """
    Convert from `CSB43` to a dictionary format

    Args:
        batch : Batch
            an AEB43 `Batch`
        expected_format : str
            destination format
    """
    csb_dict = batch.to_dict()

    if expected_format == "yaml":
        return _dict_to_yaml(csb_dict, decimal_fallback)
    if expected_format == "json":
        return _dict_to_json(csb_dict, decimal_fallback)
    raise ValueError(_("unexpected format {format}").format(format=expected_format))


def convert_aeb43_to_tabular(
    batch: Batch,
    expected_format='ods',
    decimal_fallback=None
):
    '''
    Convert an AEB43 `batch` into a `tablib` data object

    Args:

        batch : Batch
            an AEB43 batch
        expected_format: str
            output format
        decimal_fallback: str | None
            fall-back representation for decimal objects

    Returns a `tablib.Databook` or `tablib.Dataset`
    '''
    datasets = []

    accounts_abstract = tablib.Dataset()

    accounts_abstract.title = _("Accounts")
    accounts_abstract.headers = _ABSTRACT_HEADER

    datasets.append(accounts_abstract)

    account_ids: dict[str, int] = defaultdict(lambda: 0)

    ac: Account
    for ac in (batch.accounts or []):
        accounts_abstract.append(_abstract_row(ac, expected_format))

        trn_list = tablib.Dataset()
        sheet_title = '-'.join((
            ac.bank_code,
            ac.branch_code,
            ac.account_control_key,
            ac.account_number
        ))
        account_ids[sheet_title] += 1
        if account_ids[sheet_title] > 1:
            sheet_title += f" ({account_ids[sheet_title]})"
        trn_list.title = sheet_title

        trn_list.headers = _TRANSACTION_HEADER_2

        trn: Transaction
        for trn in (ac.transactions or []):
            trn_list.append(_transaction_row(trn, expected_format, decimal_fallback))

        datasets.append(trn_list)

    book = tablib.Databook(datasets)

    if hasattr(book, expected_format):
        return book

    # Databook unsupported, falling back to single Dataset
    dataset = tablib.Dataset()

    dataset.title = _("Transactions")
    dataset.headers = _ABSTRACT_HEADER + _TRANSACTION_HEADER_2

    for ac in (batch.accounts or []):

        account_abstract = _abstract_row(ac, expected_format)

        for trn in (ac.transactions or []):
            dataset.append(
                account_abstract + _transaction_row(trn, expected_format, decimal_fallback)
            )

    return dataset


def __abstractRow(ac: CAccount):
    return (
        ac.bankCode,
        ac.branchCode,
        ac.get_account_key(),
        ac.accountNumber,
        ac.informationMode,
        ac.shortName,
        ac.currency.alpha_3,
        str(ac.initialDate),
        str(ac.finalDate),
        ac.initialBalance,
        ac.abstract.balance if ac.abstract else None,
        ac.abstract.income if ac.abstract else None,
        ac.abstract.expense if ac.abstract else None,
        ac.abstract.incomeEntries if ac.abstract else None,
        ac.abstract.expenseEntries if ac.abstract else None
    )


def __transactionRow(trn: TTransaction, decimal_fallback):

    name = ", ".join(x.item1.rstrip(' ') for x in trn.optionalItems)

    extdname = ", ".join(x.item2.rstrip(' ') for x in trn.optionalItems)

    if trn.exchange:
        o_currency = utils.export_currency_code(trn.exchange.sourceCurrency)
        o_amount = utils.export_decimal(trn.exchange.amount, fallback=decimal_fallback)
    else:
        o_currency = None
        o_amount = None

    return (
        trn.branchCode,
        trn.documentNumber,
        trn.sharedItem,
        trn.ownItem,
        name,
        extdname,
        trn.reference1,
        trn.reference2,
        utils.export_date(trn.transactionDate),
        utils.export_date(trn.valueDate),
        trn.amount,
        o_currency or '',
        o_amount or ''
    )


@deprecated(version="0.10.0", reason="use csb43.formats.convert_aeb43_to_dict")
def convertFromCsb2Dict(csb: CFile, expectedFormat='json', decimal_fallback=None):
    '''
    Convert from `CSB43` to a dictionary format

    :param csb: a csb file
    :type  csb: :class:`csb43.csb43.File`
    :param decimal_fallback: decimal number fallback representation

    :rtype: a object with an attribute named as `expectedFormat`

    :raises: :class:`csb43.utils.Csb43Exception` when the format is unknown \
    or unsupported

    >>> from csb43.csb43 import File
    >>> import csb43.formats as formats
    >>> f = File()
    >>> o = formats.convertFromCsb2Dict(f, 'yaml')
    >>> print(o.yaml)
    cuentas: []
    <BLANKLINE>


    >>> o = formats.convertFromCsb2Dict(f, 'json')
    >>> print(o.json)
    {
     "cuentas": []
    }

    '''
    csb_dict = csb.as_dict(decimal_fallback=decimal_fallback)

    if expectedFormat == 'yaml':
        return _TablibSurrogate(yaml.safe_dump(csb_dict), expectedFormat)
    if expectedFormat == 'json':
        return _TablibSurrogate(
            json.dumps(csb_dict, indent=1, sort_keys=True),
            expectedFormat
        )

    utils.raiseCsb43Exception(_("unexpected format %s") % expectedFormat, True)


@deprecated(version="0.10.0", reason="use csb43.formats.convert_aeb43_to_tabular")
def convertFromCsb2Tabular(csb: CFile, expectedFormat='ods', decimal_fallback=None):
    '''
    Convert a File file into an :mod:`tablib` data object

    :param csb: a csb file
    :type  csb: :class:`csb43.csb43.File`
    :param decimal_fallback: decimal number fallback representation

    :rtype: :class:`tablib.Databook` or :class:`tablib.Dataset`

    '''
    datasets = []

    accounts_abstract = tablib.Dataset()

    accounts_abstract.title = _("Accounts")
    accounts_abstract.headers = _ABSTRACT_HEADER

    datasets.append(accounts_abstract)

    for ac in csb.accounts:
        accounts_abstract.append(__abstractRow(ac))

        trn_list = tablib.Dataset()
        trn_list.title = '-'.join((
            ac.bankCode,
            ac.branchCode,
            ac.get_account_key(),
            ac.accountNumber
        ))

        trn_list.headers = _TRANSACTION_HEADER

        for trn in ac.transactions:
            trn_list.append(__transactionRow(trn, decimal_fallback))

        datasets.append(trn_list)

    book = tablib.Databook(datasets)

    if hasattr(book, expectedFormat):
        return book

    dataset = tablib.Dataset()

    dataset.title = _("Transactions")
    dataset.headers = _ABSTRACT_HEADER + _TRANSACTION_HEADER

    for ac in csb.accounts:

        account_abstract = __abstractRow(ac)

        for trn in ac.transactions:
            dataset.append(account_abstract + __transactionRow(trn, decimal_fallback))

    return dataset


@deprecated(version="0.10.0", reason="use csb43.formats.convert_from_aeb43")
def convertFromCsb(csb: CFile, expectedFormat, decimal_fallback=None):
    '''
    Convert a File file into an :mod:`tablib` data object or a \
    dictionary-like object

    :param csb: a csb file
    :type  csb: :class:`csb43.csb43.File`
    :param decimal_fallback: decimal number fallback representation:

    - 'float': use type `float`
    - 'str': represent decimal as a string
    - `None`: use default fallback ('str')

    :rtype: :class:`tablib.Databook`, :class:`tablib.Dataset` or a object \
    with an attribute named as `expectedFormat`
    '''
    decimal_supported = expectedFormat in DECIMAL_SUPPORTED
    d_conversion = decimal_fallback or 'str'
    if decimal_supported:
        d_conversion = None

    if expectedFormat in DICT_FORMATS:
        return convertFromCsb2Dict(csb, expectedFormat, decimal_fallback=d_conversion)
    return convertFromCsb2Tabular(csb, expectedFormat, decimal_fallback=d_conversion)
