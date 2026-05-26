document.getElementById("reportForm").addEventListener("submit", function (event) {
    const reportNameSelect = document.getElementById("report_name");

    // Check if a report name has been selected
    if (!reportNameSelect || !reportNameSelect.value) {
        // Stop the form from submitting and opening a blank tab
        event.preventDefault();
        alert("Please select a Report Name before generating the report.");

        if (reportNameSelect) {
            reportNameSelect.focus();
        }
    }
    // If validation passes, no event.preventDefault() is called, 
    // and the native submission runs automatically.
});

// If you are calling it manually from a utility function, 
// make sure to perform the same validation check before submitting.
function printReport() {
    const reportNameSelect = document.getElementById("report_name");

    if (!reportNameSelect || !reportNameSelect.value) {
        alert("Please select a Report Name before generating the report.");
        if (reportNameSelect) reportNameSelect.focus();
        return; // Halt execution
    }

    document.getElementById("reportForm").submit();
}

document.addEventListener("DOMContentLoaded", function () {
    const dataEl = document.getElementById("accounts-data");
    const accounts = dataEl ? JSON.parse(dataEl.textContent) : [];
    const accountInput = document.getElementById("tran_account");

    if (accountInput) {
        inputAutocomplete(accountInput, accounts, "acc_disp_name", function (c) {
            accountInput.value = c.acc_disp_name;
            document.getElementById("tran_account_rid").value = c.acc_rid;
        });
    }

    const itemsData = document.getElementById("items-data");
    const items = itemsData ? JSON.parse(itemsData.textContent) : [];
    const itemInput = document.getElementById("tran_item");

    if (itemInput) {
        inputAutocomplete(itemInput, items, "item_display_name", function (c) {
            itemInput.value = c.item_display_name;
            document.getElementById("tran_item_rid").value = c.item_rid;
        });
    }
});