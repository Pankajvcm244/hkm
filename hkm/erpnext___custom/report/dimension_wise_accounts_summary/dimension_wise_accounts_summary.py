# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe


import calendar
from datetime import datetime
import frappe
from frappe import _, cstr
from frappe.auth import date_diff
from frappe.utils.data import add_to_date


def test():
    print("test")
    filters = {
        "dimension": "Cost Head",
        "from_date": "2024-08-01",
        "to_date": "2024-10-31",
    }
    DimensionWiseAccountsSummary(filters).get_data()


def execute(filters=None):
    colums, data = DimensionWiseAccountsSummary(filters).get_data()
    frappe.errprint(colums)
    frappe.errprint(data)
    return colums, data


class DimensionWiseAccountsSummary(object):
    def __init__(self, filters):
        self.filters = frappe._dict(filters)
        self.dimension_meta = frappe.get_meta(filters.get("dimension"))
        self.get_heads()
        self.validate_filters()
        self.get_month_year_dates_range()
        self.set_columns()
        self.data = frappe._dict()
        self.load_data()
        self.get_data()

    def get_data(self):
        final_data = []
        # for d in self.heads.values():
        # for m in self.months:
        #     if d.get(m.key):
        #         d[m.key] = d[m.key]["net"]
        # for index, fund_row in enumerate(d.fund_accounts.values()):
        #     final_data_row = frappe._dict()
        #     if index == 0:
        #         final_data_row.donation_account = d.donation_account
        #     else:
        #         final_data_row.donation_account = ""
        #     final_data_row.update(fund_row)
        #     final_data.append(final_data_row)
        #     for m in self.months:
        #         total_row[m.key] += fund_row.get(m.key, 0)
        #         total_row["total"] += fund_row.get(m.key, 0)
        # final_data.append(total_row)
        return self.columns, list(self.heads.values())

    def load_data(self):
        self.get_monthwise_gl_entries()
        self.accumulate_values_into_parents()

    def get_monthwise_gl_entries(self):
        data = {}
        dimension = frappe.scrub(self.filters.get("dimension"))
        for m in self.months:
            for d in frappe.db.sql(
                f"""
                SELECT {dimension},root_type, SUM(debit) as sum_debit, SUM(credit) as sum_credit  
                FROM `tabGL Entry`
                JOIN `tabAccount` tac
                    ON tac.name = `tabGL Entry`.account
                WHERE tac.report_type = 'Profit and Loss'
                AND is_cancelled = 0
                AND posting_date BETWEEN '{m.start_date}' AND '{m.end_date}'
                GROUP BY {dimension}, root_type  
                """,
                as_dict=True,
            ):
                head = d.get(dimension)
                month_key_inc = m.key + "_inc"
                month_key_exp = m.key + "_exp"
                if head not in data:
                    data.setdefault(head, {})
                if month_key_inc not in data[head]:
                    data[head].setdefault(month_key_inc, 0)
                if month_key_exp not in data[head]:
                    data[head].setdefault(month_key_exp, 0)
                if d.root_type == "Income":
                    data[head][month_key_inc] += (d.sum_credit or 0) - (
                        d.sum_debit or 0
                    )
                if d.root_type == "Expense":
                    data[head][month_key_exp] += (d.sum_debit or 0) - (
                        d.sum_credit or 0
                    )
        for h in self.heads:
            if h in data:
                self.heads[h].update(data[h])

    def accumulate_values_into_parents(self):
        """accumulate children's values in parent heads"""
        parent_key = "parent_" + frappe.scrub(self.dimension_meta.name)

        for head, data in reversed(list(self.heads.items())):
            if data.get(parent_key):
                for month in self.months:
                    month_key_inc = month.key + "_inc"
                    month_key_exp = month.key + "_exp"

                    if month_key_inc not in self.heads[data[parent_key]]:
                        self.heads[data[parent_key]][month_key_inc] = 0
                    self.heads[data[parent_key]][month_key_inc] += data.get(
                        month_key_inc, 0
                    )

                    if month_key_exp not in self.heads[data[parent_key]]:
                        self.heads[data[parent_key]][month_key_exp] = 0
                    self.heads[data[parent_key]][month_key_exp] += data.get(
                        month_key_exp, 0
                    )

    def get_heads(self):
        condition = ""
        if self.dimension_meta.has_field("disabled"):
            condition = " and disabled = 0"
        if self.dimension_meta.is_tree:
            actual_heads = frappe.db.sql(
                f"""
                select name, parent_{frappe.scrub(self.dimension_meta.name)}, lft, rgt,is_group
                from `tab{self.dimension_meta.name}`
                where 1 {condition} order by lft""",
                as_dict=True,
            )
            # print(self.attach_indent_to_heads(actual_heads))
            self.heads = self.attach_indent_to_heads(actual_heads)
            # print(self.heads)
        else:
            self.heads = {}
            for d in frappe.db.sql(
                f"""
                select name from `tab{self.dimension_meta.name}`
                where 1 {condition}""",
                as_dict=True,
            ):
                self.heads[d.name] = d

        # print(self.heads)

    def attach_indent_to_heads(self, actual_heads, depth=20):
        parent_children_map = {}
        heads_by_name = {}
        for d in actual_heads:
            heads_by_name[d.name] = d
            parent_children_map.setdefault(
                d.get("parent_" + frappe.scrub(self.dimension_meta.name), None), []
            ).append(d)

        refactored_heads = []

        def add_to_list(parent, level):
            if level < depth:
                children = parent_children_map.get(parent) or []
                for child in children:
                    child.indent = level
                    refactored_heads.append(child)
                    add_to_list(child.name, level + 1)

        add_to_list(None, 0)
        heads = {}
        for r in refactored_heads:
            heads[r.name] = r

        return heads

    def set_columns(self):
        self.columns = [
            {
                "fieldname": "name",
                "label": _("Dimension"),
                "fieldtype": "Data",
                "width": 300,
            },
            # {
            #     "fieldname": "currency",
            #     "label": _("Currency"),
            #     "fieldtype": "Link",
            #     "options": "Currency",
            #     "hidden": 1,
            # },
        ]
        for m in self.months:
            self.columns.extend(
                [
                    {
                        "fieldname": m.key + "_inc",
                        "label": m.label + " (Income)",
                        "fieldtype": "Currency",
                        "options": "Currency",
                        "precision": 0,
                        "width": 150,
                    },
                    {
                        "fieldname": m.key + "_exp",
                        "label": m.label + " (Expense)",
                        "fieldtype": "Currency",
                        "options": "Currency",
                        "precision": 0,
                        "width": 150,
                    },
                ]
            )

    def validate_filters(self):
        if not self.filters.get("from_date") and self.filters.get("to_date"):
            frappe.throw(_("From and To Dates are required."))
        elif date_diff(self.filters.to_date, self.filters.from_date) < 0:
            frappe.throw(_("To Date cannot be before From Date."))

    def get_month_year_dates_range(self):
        start = datetime.strptime(self.filters.get("from_date"), "%Y-%m-%d")
        end = datetime.strptime(self.filters.get("to_date"), "%Y-%m-%d")

        current = start
        date_ranges = []

        while current <= end:
            # Start date of the current month
            month_start = current.strftime("%Y-%m-%d")
            # Total days in the month
            days = calendar.monthrange(current.year, current.month)[1]
            last_day = datetime(year=current.year, month=current.month, day=days)
            month_end = min(end, last_day).strftime("%Y-%m-%d")
            unique_key = current.strftime("%Y%m")

            # Format the output
            formatted_range = frappe._dict(
                key=unique_key,
                label=current.strftime("%B - %y"),
                start_date=month_start,
                end_date=month_end,
            )
            date_ranges.append(formatted_range)

            current = add_to_date(last_day, days=1)

        self.months = date_ranges
