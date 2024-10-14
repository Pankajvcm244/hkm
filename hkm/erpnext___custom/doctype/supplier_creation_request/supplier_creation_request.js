// Copyright (c) 2022, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplier Creation Request", {
  refresh: function (frm) {
    if (frm.doc.status == "Pending") {
      frm.add_custom_button(__("Create Supplier"), function () {
        frappe.call({
          method:
            "hkm.erpnext___custom.doctype.supplier_creation_request.supplier_creation_request.quickly_create_supplier",
          args: { request: frm.doc.name },
          callback: function (r) {
            if (r.message) {
              frappe.msgprint(r.message);
            }
            frm.reload_doc();
          },
        });
      });
      frm.add_custom_button(__("Reject"), function () {
        frm.set_value("status", "Rejected");
        frm.save();
      });
    }
  },
});
