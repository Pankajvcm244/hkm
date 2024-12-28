# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class HKMGeneralSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		item_code_default_series: DF.Data | None
		material_request_expiry: DF.Int
		one_time_restrictions_enabled: DF.Check
		one_time_vendor_limit: DF.Currency
		po_approval_on_whatsapp: DF.Check
		po_whatsapp_template: DF.Data | None
		pp_group: DF.Link | None
		purchase_order_expiry: DF.Int
	# end: auto-generated types
	pass
