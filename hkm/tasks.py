from datetime import timedelta
import frappe


def mrn_close():
    past_date = frappe.utils.now() - timedelta(days=90)
    ninety_days_ago_str = past_date.strftime("%Y-%m-%d")
    for i in frappe.get_all(
        "Material Request",
        filters={
            "creation": [">", ninety_days_ago_str],
            "status": "Pending",
            "docstatus": ["!=", 2],  
        },
        pluck="name",
    ):
        doc = frappe.get_doc("Material Request", i)
        doc.cancel()
