# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries, make_autoname

AUBANK = "AU Small Finance Bank"


class HKMPaymentRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from hkm.hkm_integration.doctype.hkm_payment_request_detail.hkm_payment_request_detail import HKMPaymentRequestDetail

        amended_from: DF.Link | None
        bank_account: DF.Link
        batch_number: DF.Data | None
        company: DF.Link
        items: DF.Table[HKMPaymentRequestDetail]
        request_id: DF.Data | None
    # end: auto-generated types

    def autoname(self):
        abbrevation = frappe.db.get_value("Company", self.company, "abbr")
        prefix = f"B{abbrevation}"
        self.name = prefix + getseries(prefix, 6)

    def validate(self):
        if (
            frappe.db.get_value("Bank Account", self.bank_account, "company")
            != self.company
        ):
            frappe.throw("Bank Account doesn't belong to the company.")
        return


@frappe.whitelist()
def upload_payment(payment_request):
    payment_request_doc = frappe.get_doc("HKM Payment Request", payment_request)
    bank = frappe.db.get_value("Bank Account", payment_request_doc.bank_account, "bank")
    bank_config_found = False
    if bank == AUBANK:
        if not frappe.db.exists(
            "AU Bank Account", {"bank_account": payment_request_doc.bank_account}
        ):
            frappe.throw("The AU Bank doesn't have the configuration set in ERP.")
        bank_config_found = True
        au_bank_doc = frappe.get_doc(
            "AU Bank Account", {"bank_account": payment_request_doc.bank_account}
        )
        au_bank_doc.payout(payment_request_doc)

    if not bank_config_found:
        frappe.throw("No Bank Config available.")


@frappe.whitelist()
def get_status(payment_request):
    payment_request_doc = frappe.get_doc("HKM Payment Request", payment_request)
    bank = frappe.db.get_value("Bank Account", payment_request_doc.bank_account, "bank")
    bank_config_found = False
    if bank == AUBANK:
        if not frappe.db.exists(
            "AU Bank Account", {"bank_account": payment_request_doc.bank_account}
        ):
            frappe.throw("The AU Bank doesn't have the configuration set in ERP.")
        bank_config_found = True
        au_bank_doc = frappe.get_doc(
            "AU Bank Account", {"bank_account": payment_request_doc.bank_account}
        )
        au_bank_doc.payment_enquiry(payment_request_doc)

    if not bank_config_found:
        frappe.throw("No Bank Config available.")


@frappe.whitelist()
def make_payment_request_from_pi(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc

    def set_missing_values(source, target):
        party_bank_account = (
            frappe.db.get_value(
                "Bank Account", {"party_type": "Supplier", "party": source.party}
            )
            or ""
        )
        target.append(
            "items",
            {
                "document_type": source.doctype,
                "document_name": source.name,
                "amount": source.grand_total,
                "supplier": source.supplier,
            },
        )

    doclist = get_mapped_doc(
        "Purchase Invoice",
        source_name,
        {
            "Purchase Invoice": {
                "doctype": "HKM Payment Request",
            }
        },
        target_doc,
        set_missing_values,
    )

    return doclist
