# Copyright (c) 2026, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AssetRequest(Document):
	def on_submit(self):
		if self.workflow_state == "Approved":
			self.create_stock_entry()

	def on_cancel(self):
		self.workflow_state = "Rejected"
		self.reverse_stock_reduction()
		self.db_set("workflow_state", "Rejected")

	def create_stock_entry(self):
		se = frappe.new_doc("Stock Entry")
		se.purpose = "Material Issue"
		se.stock_entry_type = "Material Issue"
		se.company = frappe.db.get_default("company")
		se.from_warehouse = self.warehouse
		
		# Add the item from the Asset Request
		for item in self.items:
			se.append("items", {
				"item_code": item.item,
				"qty": item.quantity,
				"uom": "Nos",
				"s_warehouse": self.warehouse,
				"basic_rate": frappe.db.get_value("Item", item.item, "valuation_rate") or 0
			})
		
		se.insert()
		se.submit()
	
	def reverse_stock_reduction(self):
		reversal = frappe.new_doc("Stock Entry")
		reversal.purpose = "Material Receipt"
		reversal.stock_entry_type = "Material Receipt"
		reversal.company = frappe.db.get_default("company")

		for item in self.items:
			reversal.append("items", {
				"item_code": item.item,
				"qty": item.quantity,
				"uom": "Nos",
				"t_warehouse": self.warehouse,
				"basic_rate": frappe.db.get_value("Item", item.item, "valuation_rate") or 0
			})

		reversal.insert()
		reversal.submit()