# Copyright (c) 2024, Narahari Dasa and contributors
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

		employee: DF.Link | None
		leave_from_date: DF.Date | None
		leave_type: DF.Literal["EL", "CL", "Coff"]
		leave_upto_date: DF.Date | None
		number_of_leaves: DF.Float
	# end: auto-generated types
	
	def validate(self):
		from_date = datetime.strptime(self.leave_from_date, "%Y-%m-%d").date()
		to_date = datetime.strptime(self.leave_upto_date, "%Y-%m-%d").date()
		if to_date < from_date:
			frappe.throw("Invalid date range")
		if not check_is_valid_date(self.leave_from_date) or not check_is_valid_date(self.leave_upto_date):
			frappe.throw("Invalid date range")
		if self.number_of_leaves == 0 or not self.number_of_leaves:
			frappe.throw("Number of leaves cannot be zero")
		check_number_of_leaves(self.leave_from_date, self.leave_upto_date, self.number_of_leaves)	
		
      
    

def check_is_valid_date(value):
    value = datetime.strptime(value, "%Y-%m-%d").date()
    past_date = date.today() - timedelta(days=31)
    future_date = date.today() + timedelta(days=31)
    return past_date <= value <= future_date


def check_number_of_leaves(from_date, to_date , leaves):
	from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
	to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
	number_of_leaves = (to_date - from_date).days + 1
	range_value = number_of_leaves * 1
	if leaves > range_value:
		return frappe.throw("Number of leaves is invalid")
	leaves = float(leaves)
	fractional_part = leaves % 1
	if fractional_part not in [0, 0.5]:
		return frappe.throw("Number of leaves is invalid")

	  
