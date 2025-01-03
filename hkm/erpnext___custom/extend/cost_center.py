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
        company_abbr = frappe.get_cached_value("Company", doc.company, "abbr")
        default_cost_center = "Main - " + company_abbr
        dimensions = get_accounting_dimensions()
        dimensions.extend(["cost_center", "project"])
        for dim in dimensions:
            if doc.get(dim):
                for item in doc.items:
                    if (not item.get(dim)) or (
                        dim == "cost_center" and item.get(dim) == default_cost_center
                    ):
                        item.update({dim: doc.get(dim)})
                if doc.get("taxes"):
                    for tc in doc.taxes:
                        if (not tc.get(dim)) or (
                            dim == "cost_center" and tc.get(dim) == default_cost_center
                        ):
                            tc.update({dim: doc.get(dim)})
