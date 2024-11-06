# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe


from hkm.erpnext___custom.doctype.hkm_budget.hkm_budget import (
    get_additional_expenses_amount,
    get_dimension_condition,
    get_payment_entries_amount,
    get_unpaid_and_uninvoiced_purchase_orders_amount,
    get_unpaid_purchase_invoices_amount,
)
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)
import frappe


def execute(filters=None):
    columns = get_columns(filters)

    data = []

    for budget in frappe.get_all(
        "HKM Budget",
        filters={"docstatus": 1, "fiscal_year": filters.get("fiscal_year")},
        fields=["*"],
    ):
        args = budget
        default_dimensions = [
            {
                "fieldname": "project",
                "document_type": "Project",
            },
            {
                "fieldname": "cost_center",
                "document_type": "Cost Center",
            },
        ]

        for dimension in default_dimensions + get_accounting_dimensions(as_list=False):
            if budget.get(dimension.get("fieldname")):
                args.budget_against_field = dimension.get("fieldname")
                args.budget_against_doctype = dimension.get("document_type")
                args.is_tree = frappe.get_cached_value(
                    "DocType", args.budget_against_doctype, "is_tree"
                )
                break

        args.fiscal_year = budget.fiscal_year

        args.yr_start_date, args.yr_end_date = frappe.get_cached_value(
            "Fiscal Year", budget.fiscal_year, ["year_start_date", "year_end_date"]
        )
        args.dimension_condition = get_dimension_condition(args)
        unpaid_invoices_amount = get_unpaid_purchase_invoices_amount(args)
        unpaid_and_uninvoiced_po_amt = get_unpaid_and_uninvoiced_purchase_orders_amount(
            args
        )
        payment_entries_amount = get_payment_entries_amount(args)

        additional_expenses = get_additional_expenses_amount(args)

        used = (
            unpaid_invoices_amount
            + unpaid_and_uninvoiced_po_amt
            + payment_entries_amount
            + additional_expenses
        )

        data.append(
            frappe._dict(
                budget=budget.name,
                allowed=budget.amount,
                payment_entries_amount=payment_entries_amount,
                unpaid_invoices_amount=unpaid_invoices_amount,
                unpaid_and_uninvoiced_po_amt=unpaid_and_uninvoiced_po_amt,
                additional_expenses=additional_expenses,
                used=used,
                variance=budget.amount - used,
            )
        )

    return columns, data


def get_columns(filters):
    columns = [
        {
            "label": "Budget",
            "fieldname": "budget",
            "fieldtype": "Link",
            "options": "HKM Budget",
            "width": 200,
        },
        {
            "label": "Allowed",
            "fieldname": "allowed",
            "fieldtype": "Currency",
            "width": 150,
        },
        {
            "label": "Paid (Payment Entry)",
            "fieldname": "payment_entries_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Unpaid (Purchase Invoice)",
            "fieldname": "unpaid_invoices_amount",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": "Unpaid & Uninvoiced (Purchase Order)",
            "fieldname": "unpaid_and_uninvoiced_po_amt",
            "fieldtype": "Currency",
            "width": 250,
        },
        {
            "label": "Additional (Stock & JE)",
            "fieldname": "additional_expenses",
            "fieldtype": "Currency",
            "width": 200,
        },
        {"label": "Used", "fieldname": "used", "fieldtype": "Currency", "width": 150},
        {
            "label": "Variance",
            "fieldname": "variance",
            "fieldtype": "Currency",
            "width": 170,
        },
    ]
    return columns
