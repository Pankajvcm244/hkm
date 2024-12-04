import frappe
from hkm.erpnext___custom.letterhead import letterhead_query
from hkm.erpnext___custom.extend.cost_center import set_cost_center
from hkm.erpnext___custom.doctype.freeze_transaction_settings.freeze_transaction_settings import (
    validate_transaction_against_frozen_date,
)


def on_update(self, method=None):
    set_cost_center(self, method=None)
    letterhead_query(self, method=None)
    validate_transaction_against_frozen_date(self, method=None)
    self.reload()
