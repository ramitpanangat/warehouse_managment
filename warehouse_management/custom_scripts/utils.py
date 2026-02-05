import frappe

def hide_standard_workspaces():
    keep_visible = ["L1 User", "L2 User", "Store Manager", "Admin"] 

    workspaces = frappe.get_all("Workspace", filters={"name": ["not in", keep_visible]})

    for ws in workspaces:
        frappe.db.set_value("Workspace", ws.name, "public", 0)
    
    frappe.db.commit()



def redirect_user(login_manager):
    user = login_manager.user
    roles = frappe.get_roles(user)
    
    if "Admin" in roles or "System Manager" in roles:
        frappe.local.response["home_page"] = "/app/admin-dashboard"
    elif "L1 User" in roles:
        frappe.local.response["home_page"] = "/app/level-1"
    elif "L2 User" in roles:
        frappe.local.response["home_page"] = "/app/level-2"
    elif "Store Manager" in roles:
        frappe.local.response["home_page"] = "/app/store-manager"