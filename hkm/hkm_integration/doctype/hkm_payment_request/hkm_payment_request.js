// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on("HKM Payment Request", {
  refresh: function (frm) {
    frm.set_query("bank_account", function () {
      return {
        filters: {
          is_company_account: 1,
          company: frm.doc.company,
        },
      };
    });
    frm.set_query("supplier_bank_account", "items", function (frm, cdt, cdn) {
      const row = locals[cdt][cdn];
      return {
        filters: {
          party_type: "Supplier",
          party: row.supplier,
          disabled: 0,
        },
      };
    });
    if (frm.doc.docstatus == 1) {
      frm.add_custom_button(
        "Upload to Bank",
        function () {
          frappe.call({
            method:
              "hkm.hkm_integration.doctype.hkm_payment_request.hkm_payment_request.upload_payment",
            freeze: 1,
            freeze_message: "Uploading to Bank",
            args: {
              payment_request: frm.doc.name,
            },
            callback: function (r) {
              if (r.message) {
                frappe.msgprint(r.message);
              }
              frm.reload_doc();
            },
          });
        },
        "Bank Operations"
      );
      frm.add_custom_button(
        "Get Status",
        function () {
          frappe.call({
            method:
              "hkm.hkm_integration.doctype.hkm_payment_request.hkm_payment_request.get_status",
            freeze: 1,
            freeze_message: "Fetching Status",
            args: {
              payment_request: frm.doc.name,
            },
            callback: function (r) {
              if (r.message) {
                frappe.msgprint(r.message);
              }
              frm.reload_doc();
            },
          });
        },
        "Bank Operations"
      );
    }

    // if (
    //   frm.doc.document_type &&
    //   ["Purchase Invoice", "Purchase Order"].includes(frm.doc.document_type)
    // ) {
    //   frm.set_query("document_name", "items", function (frm, cdt, cdn) {
    //     const row = locals[cdt][cdn];
    //     return {
    //       filters: {
    //         party_type: "Supplier",
    //         party: row.supplier,
    //         docstatus: 1,
    //       },
    //     };
    //   });
    // }

    // if (frm.doc.docstatus == 0) {
    //   frm.add_custom_button(
    //     __("Purchase Invoice"),
    //     function () {
    //       //   frm.trigger("get_from_purchase_invoice");
    //       erpnext.utils.map_current_doc({
    //         method:
    //           "hkm.hkm_integration.doctype.hkm_payment_request.hkm_payment_request.make_payment_request_from_pi",
    //         source_doctype: "Purchase Invoice",
    //         target: frm,
    //         date_field: "posting_date",
    //         setters: {
    //           // supplier: frm.doc.supplier || undefined,
    //           company: frm.doc.company,
    //           supplier: frm.doc.supplier,
    //         },
    //         get_query_filters: {
    //           docstatus: 1,
    //         },
    //       });
    //     },
    //     __("Get Payments from")
    //   );

    //   frm.add_custom_button(
    //     __("Purchase Order"),
    //     function () {
    //       frm.trigger("get_from_purchase_order");
    //     },
    //     __("Get Payments from")
    //   );

    //   frm.trigger("remove_button");
    // }
  },
  get_from_purchase_invoice: function (frm) {
    // frm.trigger("remove_row_if_empty");
    erpnext.utils.map_current_doc({
      method:
        "hkm.hkm_integration.doctype.hkm_payment_request.hkm_payment_request.make_payment_request_from_pi",
      source_doctype: "Purchase Invoice",
      target: frm,
      setters: {
        party_type: "Supplier",
        party: frm.doc.supplier || "",
      },
      get_query_filters: {
        docstatus: 1,
        // status: ["=", "Initiated"],
      },
    });
  },
});

frappe.ui.form.on("HKM Payment Request Detail", {
  supplier: async function (frm, cdt, cdn) {
    var d = frappe.get_doc(cdt, cdn);
    r = await frappe.db.get_value(
      "Bank Account",
      (filters = { party_type: "Supplier", party: d.supplier, disabled: 0 }),
      (pluck = "name")
    );
    if (r.message.name) {
      frappe.model.set_value(cdt, cdn, "supplier_bank_account", r.message.name);
    }
  },
  supplier_bank_account: async function (frm, cdt, cdn) {
    var d = frappe.get_doc(cdt, cdn);
    var bank_doc = await frappe.db.get_doc(
      "Bank Account",
      d.supplier_bank_account
    );
    frappe.model.set_value(
      cdt,
      cdn,
      "bank_account_name",
      bank_doc.account_name
    );
    frappe.model.set_value(
      cdt,
      cdn,
      "bank_account_number",
      bank_doc.bank_account_no
    );
    frappe.model.set_value(cdt, cdn, "ifsc_code", bank_doc.branch_code);
    refresh_field("items");
  },
});
