from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)
from hkm.erpnext___custom.doctype.hkm_budget.hkm_budget import (
    validate_expense_against_budget,
)
import frappe


def validate(doc, method=None):
    args = doc.as_dict()
    validate_expense_against_budget(args)
    return
