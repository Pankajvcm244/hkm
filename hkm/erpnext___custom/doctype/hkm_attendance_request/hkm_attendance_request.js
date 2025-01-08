// Copyright (c) 2025, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on("HKM Attendance Request", {
	refresh(frm) {
     
	},
    department(frm) {
        frm.set_query("employee", (doc) => {
            return {
                filters: {
                    department: doc.department,
                    status :"Active"
                }
            }
        })
    },

    employee(frm) {
        // apps/hkm/hkm/erpnext___custom/doctype/hkm_attendance_request/opening_leave_balance.py
        frappe.call({
            method: "hkm.erpnext___custom.doctype.hkm_attendance_request.opening_leave_balance.leave_balance",
            args: {
                employee_id : frm.doc.employee
            },
            freeze: true,
            async: true,
            callback: function (r) {
              if (r.message) {
                console.log(r.message);
              
                frm.set_df_property("leave_balance", "options", `
                    <div style="text-align: center;">
                        <h5>
                            ${r.message.month} 
                            EL: ${r.message.el_opening_balance} 
                            CL: ${r.message.cl_opening_balance} 
                            COFF: ${r.message.coff_opening_balance}
                        </h5>
                    </div>
                `);
                
                // Refresh the field to update the UI
                frm.refresh_field("leave_balance");
              } else {
                frm.set_df_property("leave_balance", "options", `
                    <div style="text-align: center;">
                        <h5>No leave balance data found for the selected employee.</h5>
                    </div>
                `);
                frm.refresh_field("leave_balance");
              }
            },
          });
    }
});
