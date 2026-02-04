// Copyright (c) 2026, Ramit Panangat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Request', {
    onload: function (frm) {
        set_warehouse_filter(frm, frappe.session.user);
    },
    requester: function (frm) {
        console.log("hello")
        console.log(frm)
        set_warehouse_filter(frm, frm.doc.requester);
        frm.set_value('warehouse', '');
    },
    warehouse: function (frm) {
        frm.set_query('item', 'items', function () {
            return {
                query: "warehouse_management.warehouse_management.doctype.asset_request.custom_script.get_items_from_bin",
                filters: {
                    "warehouse": frm.doc.warehouse
                }
            };
        });
    }
});

function set_warehouse_filter(frm, user) {
    frm.set_query('warehouse', function () {
        return {
            query: "warehouse_management.warehouse_management.doctype.asset_request.custom_script.get_assigned_warehouses",
            filters: {
                "user": user
            }
        };
    });
}
