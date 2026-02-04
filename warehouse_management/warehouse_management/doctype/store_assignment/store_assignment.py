# Copyright (c) 2026, Ramit Panangat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StoreAssignment(Document):
	def validate(self):
		if self.is_new():
			existing_assignment = frappe.db.exists("Store Assignment", {"user": self.user})
			
			if existing_assignment:
				frappe.throw(
					msg="A Store Assignment already exists for <b>{0}</b>. Please find the existing record <b>({1})</b> and add the new warehouse to the list there instead of creating a new one.".format(
						frappe.db.get_value("User", self.user, "full_name"), 
						existing_assignment
					),
					title="Duplicate Assignment"
				)

	def autoname(self):
		full_name = frappe.db.get_value("User", self.user, "full_name")
		self.name = full_name if full_name else self.user

	def on_update(self):
		current_warehouses = [d.warehouse for d in self.warehouse if d.warehouse]
		existing_permissions = frappe.get_all("User Permission", filters={"user": self.user, "allow": "Warehouse"}, pluck="for_value")
		
		for w in current_warehouses:
			if w not in existing_permissions:
				user_permission = frappe.new_doc("User Permission")		
				user_permission.user = self.user
				user_permission.allow = "Warehouse"
				user_permission.for_value = w
				user_permission.apply_to_all_doctypes = 1
				user_permission.insert(ignore_permissions=True)

		for x in existing_permissions:
			if x not in current_warehouses:
				frappe.db.delete("User Permission", {"user": self.user, "allow": "Warehouse", "for_value": x})
	
	def on_trash(self):
		frappe.db.delete("User Permission", {"user": self.user, "allow": "Warehouse"})