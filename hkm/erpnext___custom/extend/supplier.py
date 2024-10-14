import frappe
from frappe.contacts.doctype.address.address import get_address_display
from frappe.utils import time_diff_in_hours, time_diff_in_seconds, date_diff, flt
from frappe.model.workflow import apply_workflow
from frappe.utils.background_jobs import enqueue
from frappe import _


item_supplier_admin = "Item Manager"


def creation_from_gstin(self, method):
    if (
        self.is_new()
        and not self.get("gstin")
        and not item_supplier_admin in frappe.get_roles(frappe.session.user)
    ):
        frappe.throw(
            "You are not allowed to create a Supplier without GSTIN. Raise through Supplier Creation Request."
        )
    return
