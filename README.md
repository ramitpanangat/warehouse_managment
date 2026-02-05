This is a professional `README.md` structure for your GitHub repository or submission folder. It is designed to impress an interviewer by highlighting your architectural choices and the logic behind your Frappe/ERPNext implementation.

---

# Multi-Store Asset & Order Management System

A custom Frappe application designed for **Brocode Solutions Machine Test**. This system extends ERPNext core inventory functionality to provide a role-based, multi-warehouse asset request lifecycle with strict data isolation.

## 🚀 Overview

The system enables employees to request assets from specific warehouses, managed by Store Managers who are assigned to one or more locations. The core focus is a **"Zero-Noise"** UI where users see only the data and actions relevant to their assigned stores and roles.

---

## 🏗️ Architecture Decisions

### Core Inventory Integration

Instead of creating custom stock tables, this app extends the **ERPNext Core**:

* **Bin & Stock Ledger:** All asset requests query the `Bin` table directly for real-time availability.
* **Stock Entry:** Upon approval, the system automates the creation of a `Material Issue` Stock Entry, ensuring the Stock Ledger remains the "Single Source of Truth."

### Data Structure

* **Store Assignment:** A custom DocType using a **Child Table** to map one User to multiple Warehouses. This supports "Group Store Managers" who oversee several locations.
* **Asset Request:** Uses a Child Table for items to support bulk requests in a single document.

---

## 🔐 Role & Permission Handling

### Server-Side Data Isolation

To ensure strict security, I implemented **Permission Query Hooks** in `hooks.py`.

* **The Logic:** Even if a user bypasses the UI, the database query is intercepted to append a `WHERE` clause, restricting visibility to items and requests linked only to the user's assigned warehouses.

### Dynamic UI Filtering

* **Warehouse Dropdown:** Users only see warehouses assigned to them in the **Store Assignment**.
* **Item Selection:** The `item_code` field in the Asset Request child table is filtered via `set_query` to only show items that have an `actual_qty > 0` in the selected warehouse.

---

## 📊 Dashboard Logic (Role-Based)

The app utilizes **Frappe Workspaces** restricted by roles to provide a tailored experience. All default ERPNext modules are disabled for these roles to ensure a focused environment.

### 1. Admin Executive (The "Control Tower")

* **Status Number Cards:** Separate cards for *Draft, Pending, Approved, Rejected, and Cancelled* states.
* **Workflow Pie Chart:** Visual distribution of requests by their current workflow state.
* **Global Quick List:** Real-time feed of all requests across the organization.

### 2. Store Manager / L1 / L2

* **Action-Oriented Cards:** Users only see cards relevant to their workflow step (e.g., L2 sees "Pending Verification," Manager sees "Pending Approval").
* **Contextual Lists:** Quick Lists are pre-filtered to show only the tasks assigned to the logged-in user's warehouse.
* **Universal Shortcuts:** Quick-access buttons for *Asset Request, Item,* and *Store Assignment*.

---

## 🛠️ Stock Flow Logic

* **Automated Issuance:** I utilized Python's `frappe.get_doc` and `append` methods to map the Asset Request child table directly into a `Stock Entry`. This eliminates manual entry errors and ensures valuation rates are pulled correctly from the Item Master.
* **Reversal Logic:** If a request is cancelled after approval, the system is designed to trigger a `Material Receipt` to return assets to the correct warehouse.

---

## ⚙️ Setup & Installation

### Prerequisites

* Bench / Frappe Environment (v14 or v15)
* ERPNext installed on the site

### Installation

1. **Fetch the app:**
```bash
bench get-app [your-repo-url]

```


2. **Install on site:**
```bash
bench --site [your-site-name] install-app asset_management

```


3. **Migrate database:**
```bash
bench migrate

```



### Post-Install Setup

1. Assign the custom roles (**Store Manager, L1, L2, Admin Executive**) to your test users.
2. Create **Store Assignments** for each user to link them to their respective warehouses.
3. Access the custom **Workspaces** via the `/app` route.

---

## 📝 Technical Trade-offs & Assumptions

* **Assumption:** The Admin handles the initial `Material Receipt` of stock into warehouses using standard ERPNext tools.
* **Trade-off:** Prioritized **Backend Permission Logic** and **Data Integrity** over custom HTML/CSS UI styling to meet the prototype track's functional requirements.
* **Auditability:** Added custom logging to track request transitions, fulfilling requirements for debugging and system transparency.
