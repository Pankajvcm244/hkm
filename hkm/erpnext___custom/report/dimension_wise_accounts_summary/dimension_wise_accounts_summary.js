// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.query_reports["Dimension-wise Accounts Summary"] = {
  filters: [
    {
      fieldname: "dimension",
      label: __("Select Dimension"),
      fieldtype: "Select",
      default: "Cost Center",
      options: get_accounting_dimension_options(),
      reqd: 1,
    },
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      default: erpnext.utils.get_fiscal_year(
        frappe.datetime.get_today(),
        true
      )[1],
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      default: erpnext.utils.get_fiscal_year(
        frappe.datetime.get_today(),
        true
      )[2],
      reqd: 1,
    },
  ],
  tree: true,
  name_field: "name",
  parent_field: "parent_cost_head",
  initial_depth: 1,
};

function get_accounting_dimension_options() {
  let options = ["Cost Center", "Project"];
  frappe.db
    .get_list("Accounting Dimension", { fields: ["document_type"] })
    .then((res) => {
      res.forEach((dimension) => {
        options.push(dimension.document_type);
      });
    });
  return options;
}
