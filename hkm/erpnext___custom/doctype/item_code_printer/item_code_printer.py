# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ItemCodePrinter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link | None
		date: DF.Date | None
		item_code: DF.Data | None
		price_list: DF.Link | None
		quantity: DF.Int
		quantity_date: DF.Int
	# end: auto-generated types
	pass
