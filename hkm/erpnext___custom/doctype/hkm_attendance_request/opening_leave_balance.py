


import frappe

@frappe.whitelist()
def leave_balance(employee_id):
    doc = frappe.get_all(
        "HKM Leaves",
        filters = {
            "employee": employee_id
        },
        pluck = "name"
        
    )
    
    # if not doc:
    #     frappe.throw("No Leave Balance Found")    
    if len(doc) > 1:
        frappe.throw("Multiple Leave Balance Found")
    if not doc:
        return
    leave_balance = frappe.get_doc("HKM Leaves", doc[0])
    return {
        "el_opening_balance": doc.el_opening_balance,
        "cl_opening_balance": doc.cl_opening_balance,
        "coff_opening_balance": doc.coff_opening_balance
    }
    