
frappe.ready(function() {
    if (window.location.search.includes('redirect-to')) {
        const cleanUrl = window.location.origin + window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl);
        console.log("Logout redirect parameters cleared.");
    }
});