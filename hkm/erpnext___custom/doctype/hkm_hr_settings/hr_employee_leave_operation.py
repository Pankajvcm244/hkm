from hkm.erpnext___custom.doctype.extra_utils.sheet import get_data_from_google_sheets
import frappe


@frappe.whitelist(methods=["POST"])
def process():
    operations_doc = frappe.get_single("HKM HR Settings")
    if not operations_doc.google_sheets_link:
        frappe.throw("There is no link avaialble.")
    rows = get_data_from_google_sheets(operations_doc.google_sheets_link)
    headers = rows[0]
    
    if (
        not [
           "Employee ID",
           "EL Opening Balance",
           "CL Opening Balance",
           "Coff Opening Balance",
           "Month"  
        ]
        == headers
    ):
        frappe.throw("Google Sheets File is Corrupt. Headers are not matching.")
    month = rows[1][4]  
    if not month:
        frappe.throw("Please put the month in the sheet.")
    operations_doc.month = month
    operations_doc.save(ignore_permissions=True)      
    
    frappe.db.sql(
        f"""
        DELETE FROM `tabHKM Leaves`'
        """
    )
    frappe.db.commit()
    for raw in rows[1:]:
        create_hkm_leave_entries(raw)
        

def create_hkm_leave_entries(raw):        
    employee_id = raw[0]
    if not employee_id:
        return
    employee = frappe.get_doc({
        "doctype": "HKM Leaves",
        "employee": employee_id,
        "el_opening_balance": raw[1],
        "cl_opening_balance": raw[2],
        "coff_opening_balance" : raw[3],
        
    }).insert(ignore_permissions=True)
    
    
    return