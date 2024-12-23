# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet


class CostHead(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cost_head_name: DF.Data
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_cost_head: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types
	pass
