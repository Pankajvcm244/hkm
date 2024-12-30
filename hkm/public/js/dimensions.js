$(document).on("app_ready", function () {
  $.each(["Purchase Invoice"], function (i, doctype) {
    frappe.ui.form.on(doctype, {
      cost_head: function (frm) {
        for (var i = 0; i < frm.doc.items.length; i++) {
          frappe.model.set_value(
            frm.doc.items[i].doctype,
            frm.doc.items[i].name,
            "cost_head",
            frm.doc.cost_head
          );
        }
      },
      cost_center: function (frm) {
        for (var i = 0; i < frm.doc.items.length; i++) {
          frappe.model.set_value(
            frm.doc.items[i].doctype,
            frm.doc.items[i].name,
            "cost_center",
            frm.doc.cost_center
          );
        }
      },
    });
  });
});
