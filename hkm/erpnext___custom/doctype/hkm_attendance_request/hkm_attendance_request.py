# Copyright (c) 2025, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe
from datetime import datetime, timedelta, date

import time
from frappe.model.document import Document
from frappe.utils import getdate
import frappe


class HKMAttendanceRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        employee: DF.Link
        leave_from_date: DF.Date
        leave_type: DF.Literal["EL", "CL", "Coff"]
        leave_upto_date: DF.Date
        number_of_leaves: DF.Float
    # end: auto-generated types
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        employee: DF.Link
        leave_from_date: DF.Date
        leave_type: DF.Literal["EL", "CL", "Coff"]
        leave_upto_date: DF.Date
        number_of_leaves: DF.Float

    def validate(self):
        if not self.leave_from_date < self.leave_upto_date:
            frappe.throw("Invalid date range")
        if not check_is_valid_date(self.leave_from_date) or not check_is_valid_date(
            self.leave_upto_date
        ):
            frappe.throw("Invalid date range")
        
        check_duplicate_leave_applications(
            self.employee, self.leave_from_date, self.leave_upto_date
        )
    
        if self.number_of_leaves == 0 or not self.number_of_leaves:
            frappe.throw("Number of leaves cannot be zero")
        check_number_of_leaves(
            self.leave_from_date, self.leave_upto_date, self.number_of_leaves
        )


def check_duplicate_leave_applications(employee, leave_from_date, leave_upto_date):
    from_date = datetime.strptime(leave_from_date, "%Y-%m-%d")
    upto_date = datetime.strptime(leave_upto_date, "%Y-%m-%d")
    query = frappe.db.sql(
    f"""
    SELECT employee , leave_from_date, leave_upto_date
    FROM `tabHKM Attendance Request`
    WHERE employee = '{employee}'
    AND (
        -- Condition 1: New range starts within an existing range
        (leave_from_date <= '{from_date}' AND leave_upto_date >= '{from_date}')
        
        -- Condition 2: New range ends within an existing range
        OR (leave_from_date <= '{upto_date}' AND leave_upto_date >= '{upto_date}')
        
        -- Condition 3: Existing range is fully contained in the new range
        OR (leave_from_date >= '{from_date}' AND leave_upto_date <= '{upto_date}')
        
        -- Condition 4: New range is fully contained in the existing range
        OR (leave_from_date <= '{from_date}' AND leave_upto_date >= '{upto_date}')
        
        -- Condition 5: Exact match of ranges
        OR (leave_from_date = '{from_date}' AND leave_upto_date = '{upto_date}')
    )
    """,
    as_dict=1,
)
    if query:
        frappe.throw("Duplicate leave application: The requested dates overlap with an existing leave application.")



def check_is_valid_date(value):
    value = datetime.strptime(value, "%Y-%m-%d").date()
    past_date = date.today() - timedelta(days=31)
    future_date = date.today() + timedelta(days=31)
    return past_date <= value <= future_date


def check_number_of_leaves(from_date, to_date, leaves):
	from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
	to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
	number_of_leaves = (to_date - from_date).days + 1  # Calculate total days including both from_date and to_date
    
	if leaves == number_of_leaves:
		return
    # Check if leaves exceed the calculated number of days
	if leaves > number_of_leaves:
		frappe.throw("Number of leaves is invalid")
    
    # Check if the number of leaves has a valid fractional part
	leaves = float(leaves)
	fractional_part = leaves % 1
	if fractional_part not in [0, 0.5]:
		frappe.throw("Number of leaves is invalid")
        

	if leaves != (number_of_leaves - 0.5):
		frappe.throw("Number of leaves is invalid")
