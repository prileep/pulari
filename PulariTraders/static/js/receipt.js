document.addEventListener("DOMContentLoaded", function () {

    const dataEl = document.getElementById("accounts-data");
    const accounts = dataEl ? JSON.parse(dataEl.textContent) : [];

    const accountInput = document.getElementById("rcpt_account_name");

    if (accountInput) {

        inputAutocomplete(
            accountInput,
            accounts,
            "acc_disp_name",
            function (acc) {
                selectReceiptAccount(acc);
            }
        );
    }
});


function selectReceiptAccount(acc) {

    const rcpt_acc_rid = document.getElementById("rcpt_acc_rid");
    const rcpt_account_name = document.getElementById("rcpt_account_name");
    const rcpt_account_code = document.getElementById("rcpt_account_code");

    if (!acc) {
        rcpt_acc_rid.value = "";
        rcpt_account_name.value = "";
        rcpt_account_code.value = "";
        showAccountBalanceSheet();
        return;
    }

    rcpt_acc_rid.value = acc.acc_rid;
    rcpt_account_name.value = acc.acc_disp_name;
    rcpt_account_code.value = acc.acc_code;

    showAccountBalanceSheet();
}

function showAccountBalanceSheet() {
    const accountRid = document.getElementById("rcpt_acc_rid").value;
    const table = document.getElementById("receiptAccountBalanceSheetTable");
    const dueAmtInput = document.getElementById("rcpt_account_due_amt");

    if (!accountRid || !table) {
        clearBalanceSheetRows(table);
        if (dueAmtInput) dueAmtInput.value = "";
        return;
    }

    const url = `/receipt/api/customer-balance-sheet/?rid=${accountRid}`;

    fetch(url, {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            clearBalanceSheetRows(table);

            // 1. Add the Opening Balance row first if data exists
            if (data && data.length > 0) {
                const openingBalanceVal = parseFloat(data[0].open_balance || 0).toFixed(0); //

                const openRow = document.createElement("tr");
                openRow.classList.add("data-row", "rowUnderline");

                // Removed the "Opening Balance" label string from the second <td> column cell
                openRow.innerHTML = `
                    <td></td>
                    <td style="text-align: left;"></td>
                    <td></td>
                    <td style="text-align: right;"></td>
                    <td></td>
                    <td style="text-align: right;"></td>
                    <td></td>
                    <td style="text-align: right; font-weight: bold;">
                        ${formatIndianCurrency(openingBalanceVal)}
                    </td>
                    <td></td>
                `;
                table.appendChild(openRow);

                referenceNode = openRow.nextSibling;
            } else {
                if (dueAmtInput) dueAmtInput.value = "0";
            }

            // 2. Dynamically append new rows to table body in sequence
            data.forEach((item, index) => {
                const row = document.createElement("tr");
                row.classList.add("data-row", "rowUnderline");

                const debitAmount = parseFloat(item.dr_amt || 0); //
                const creditAmount = parseFloat(item.cr_amt || 0); //

                const displayDebit = debitAmount > 0 ? formatIndianCurrency(debitAmount.toFixed(0)) : '';
                const displayCredit = creditAmount > 0 ? formatIndianCurrency(creditAmount.toFixed(0)) : '';
                const displayBalance = formatIndianCurrency(parseFloat(item.balance || 0).toFixed(0)); //

                row.innerHTML = `
                    <td></td>
                    <td style="text-align: left;">
                        <small class="text-muted d-block">${formatDate(item.acctran_date)}</small> ${item.acc_notes || ''} </td>
                    <td></td>
                    <td style="text-align: right; vertical-align: bottom;">${displayDebit}</td>
                    <td></td>
                    <td style="text-align: right; vertical-align: bottom;">${displayCredit}</td>
                    <td></td>
                    <td style="text-align: right; vertical-align: bottom; font-weight: bold;">${displayBalance}</td>
                    <td></td>
                `;

                table.appendChild(row);
                if (index === data.length - 1) {
                    dueAmtInput.value = item.balance;
                }
            });
        })
        .catch(error => {
            console.error("Error fetching ledger balance data:", error);
        });
}

// Utility function to drop rows safely without mutating fixed structural markup headers
function clearBalanceSheetRows(table) {
    if (!table) return;
    const dataRows = table.querySelectorAll(".data-row");
    dataRows.forEach(row => row.remove());
}