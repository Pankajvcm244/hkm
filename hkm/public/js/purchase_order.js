frappe.ui.form.on("Purchase Order", {
  company: function (frm) {
    frm.set_query("department", () => {
      return {
        filters: {
          company: frm.doc.company,
        },
      };
    });
  },
  onload: function (frm) {
    frm.add_custom_button(__("Resend Approval Request"), function () {
      frappe.prompt(
        {
          label: "Method",
          fieldname: "method",
          fieldtype: "Select",
          options: "WhatsApp\nEmail",
        },
        (values) => {
          console.log(values.method);
          frappe.call({
            method:
              "hkm.erpnext___custom.overrides.purchase_order.HKMPurchaseOrder.resend_approver_request",
            args: {
              docname: frm.doc.name,
              method: values.method,
            },
            callback: (r) => {
              var doc = frappe.model.sync(r.message);
            },
          });
        }
      );
      // resend_approver_request
    });
  },
});

frappe.ui.form.on("Purchase Order Item", {
  // The child table is defined in a DoctType called "Dynamic Link"
  item_code(frm, cdt, cdn) {
    // "links" is the name of the table field in ToDo, "_add" is the event

    let row = frappe.get_doc(cdt, cdn);
    if (row.item_code) {
      frappe.db.get_doc("Item", row.item_code).then((doc) => {
        if (doc.is_fixed_asset == 1) {
          row.item_type = "Asset";
        } else if (doc.is_stock_item == 1) {
          row.item_type = "Stock";
        } else {
          row.item_type = "Non-Stock";
        }
        frm.refresh_field("items");
      });
    }
  },
});
