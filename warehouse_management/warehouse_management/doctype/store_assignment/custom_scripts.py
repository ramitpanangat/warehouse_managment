import frappe


privileged_roles = ["Administrator", "Admin", "System Manager"]
def asset_request_permission_query(user):
	if not user: user = frappe.session.user
	user_roles = frappe.get_roles(user)
	if any(role in user_roles for role in privileged_roles):
		return ""

	assigned_warehouses = frappe.get_all("User Permission", filters={"user": user, "allow": "Warehouse"}, pluck="for_value")

	if not assigned_warehouses:
		return "1=0"

	warehouses_sql = "', '".join(assigned_warehouses)
	condition = f"`tabAsset Request`.warehouse IN ('{warehouses_sql}')"

	return condition

def get_item_by_assignment(user):
    if not user: user = frappe.session.user
    user_roles = frappe.get_roles(user)
    if any(role in user_roles for role in privileged_roles):
        return ""

    assignments = frappe.get_all("Store Assignment", 
        filters={"user": user}, 
        fields=["name"]
    )
    
    if not assignments:
        return "1=0"

    assigned_warehouses = frappe.get_all("Store Warehouse", # Child DocType name
        filters={"parent": assignments[0].name},
        pluck="warehouse"
    )

    if not assigned_warehouses:
        return "1=0"

    allowed_items = frappe.get_all("Bin",
        filters={"warehouse": ["in", assigned_warehouses], "actual_qty": [">", 0]},
        pluck="item_code"
    )

    if allowed_items:
        return f"`tabItem`.name in ({', '.join([frappe.db.escape(i) for i in allowed_items])})"
    
    return "1=0"