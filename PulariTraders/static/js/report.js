function printReport() {
    // Collect the parameter values cleanly from DOM inputs
    const reportName = document.getElementById("report_name")?.value || "";
    const fromDate = document.getElementById("tran_from_date")?.value || "";
    const toDate = document.getElementById("tran_to_date")?.value || "";
    const itemRid = document.getElementById("tran_item_rid")?.value || "0";
    const accountRid = document.getElementById("tran_account_rid")?.value || "0";
    const refType = document.getElementById("acctran_ref_type")?.value || "";

    // Build standard URL parameters query string securely
    const queryParams = new URLSearchParams({
        report_name: reportName,
        tran_from_date: fromDate,
        tran_to_date: toDate,
        tran_item_rid: itemRid,
        tran_account_rid: accountRid,
        acctran_ref_type: refType
    });

    // Request fresh data matching these variables via JSON endpoint
    fetch(`/report/generate_report/?${queryParams.toString()}`)
        .then(response => response.json())
        .then(data => {
            if (data.details) {
                // Cache data to localStorage so the raw print window can extract it immediately
                localStorage.setItem("print_report_payload", JSON.stringify(data.details));
                localStorage.setItem("print_report_metadata", JSON.stringify({
                    report_name: reportName,
                    from_date: fromDate,
                    to_date: toDate
                }));

                // Open the clean print layout template in a separate workspace tab
                window.open("/report/print_preview/", "_blank");
            } else {
                alert("No structural data found for the current query criteria.");
            }
        })
        .catch(error => {
            console.error("Report extraction processing failure:", error);
            alert("Could not process your printing query request at this time.");
        });
}