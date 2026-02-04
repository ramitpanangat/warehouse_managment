import frappe

@frappe.whitelist()
def get_assigned_warehouses(doctype, txt, searchfield, start, page_len, filters):
    user = filters.get("user")
    user_roles = frappe.get_roles(user)
    privileged_roles = ["Administrator", "Admin", "System Manager"]

    if any(role in user_roles for role in privileged_roles):
        all_warehouses = frappe.get_all("Warehouse", 
            filters=[["name", "like", f"%{txt}%"]], 
            pluck="name"
        )
        return [[w] for w in all_warehouses]

    assigned_warehouses = frappe.get_all("User Permission", 
        filters={
            "user": user, 
            "allow": "Warehouse"
        }, 
        pluck="for_value"
    )

    if not assigned_warehouses:
        return []

    result = [[w] for w in assigned_warehouses if txt.lower() in w.lower()]
    return result


@frappe.whitelist()
def get_items_from_bin(doctype, txt, searchfield, start, page_len, filters):
    warehouse = filters.get("warehouse")
    
    if not warehouse:
        return []
        
    bins = frappe.get_all("Bin",
        filters={
            "warehouse": warehouse,
            "actual_qty": [">", 0],
            "item_code": ["like", f"%{txt}%"]
        },
        fields=["item_code", "actual_qty", "stock_uom"],
        start=start,
        page_length=page_len,
        as_list=True
    )

    return bins