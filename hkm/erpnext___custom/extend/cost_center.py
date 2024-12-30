from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)


relevant_documents = [
    "Material Request",
    "Purchase Order",
    "Purchase Invoice",
    "Sales Invoice",
    "Stock Entry",
    "Purchase Receipt",
]

import frappe


def set_dimensions(doc, method=None):
    if doc.doctype in relevant_documents:
        dimensions = get_accounting_dimensions()
        dimensions.extend(["cost_center", "project"])
        for dim in dimensions:
            if doc.get(dim):
                for item in doc.items:
                    if not item.get(dim):
                        item.update({dim: doc.get(dim)})
                if doc.get("taxes"):
                    for tc in doc.taxes:
                        if not tc.get(dim):
                            tc.update({dim: doc.get(dim)})
