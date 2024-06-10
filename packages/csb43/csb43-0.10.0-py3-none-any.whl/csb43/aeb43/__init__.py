# SPDX-FileCopyrightText: 2024 <wmj.py@gmx.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
Parsing and validation utilites for the Spanish standard norm 43 by the
"Consejo Superior Bancario" (CSB) / "Asociación Española de Banca" (AEB)
for storing bank account transactions.

[es] Herramientas para leer y validar datos almacenados siguiendo la norma 43
del Consejo Superior Bancario (CSB) / Asociación Española de Banca (CSB).


References
----------

.. [n43_2012] Información normalizada de cuenta corriente SEPA (2012), Serie normas y procedimientos bancarios nº 43. Confederación Española de Cajas de Ahorros. Asociación Española de Banca.

.. code-block:: bibtex

    @techreport{n43_2012,
        author = {Varios},
        institution = {Confederación Española de Cajas de Ahorros},
        month = 6,
        number = {Serie normas y procedimientos bancarios nº 43},
        publisher = {Asociación Española de Banca},
        title = {{Información normalizada de cuenta corriente (SEPA)}},
        year = {2012}
    }
"""

from .batch import Batch, read_batch, EndOfFile
from .account import Account
from .transaction import Transaction
from .item import Item
from .exchange import Exchange
from .sepa_debit import SepaDebit
from .sepa_transfer import SepaTransfer
from .closing_account import ClosingAccount
from .record.context import get_current_context

__all__ = [
    "Batch",
    "read_batch",
    "EndOfFile",
    "Account",
    "ClosingAccount",
    "Transaction",
    "Item",
    "Exchange",
    "SepaDebit",
    "SepaTransfer",
    "get_current_context",
]
