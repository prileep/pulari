function getParams() {
    const acctran_ref_type = document.getElementById("acctran_ref_type")?.value || "";
    const tranStatus = document.getElementById("tran_status")?.value || "";
    const fromDate = document.getElementById("tran_from_date")?.value || "";
    const toDate = document.getElementById("tran_to_date")?.value || "";
    const tran_account_rid = document.getElementById("tran_account_rid")?.value || "";
    const tran_account = document.getElementById("tran_account")?.value || "";
    const refno = document.getElementById("tran_refno")?.value || "";
    const notes = document.getElementById("tran_notes")?.value || "";
    const amountFrom = document.getElementById("tran_amount_from")?.value || "";
    const amountTo = document.getElementById("tran_amount_to")?.value || "";


    const params = new URLSearchParams({
        acctran_ref_type: acctran_ref_type,
        status: tranStatus,
        from_date: fromDate,
        to_date: toDate,
        account_rid: tran_account_rid,
        account: tran_account,
        refno: refno,
        notes: notes,
        amount_from: amountFrom,
        amount_to: amountTo
    });
    return params;
}

function printTransactions() {

    const params = getParams();
    const tran_account_rid = document.getElementById("tran_account_rid")?.value || "0";

    let printUrl =
        `/transactionbrowser/${tran_account_rid == "0" ? "print" : "printbyaccount"
        }/?${params.toString()}`;

    window.open(printUrl, "_blank");
}

document.addEventListener("DOMContentLoaded", function () {
    const dataEl = document.getElementById("accounts-data");
    const accounts = dataEl ? JSON.parse(dataEl.textContent) : [];
    const accountInput = document.getElementById("tran_account");

    const tblTransactionBrowserItems = document.getElementById("tblTransactionBrowserItems");
    const rowClone = document.getElementById("rowTransactionBrowserItems").cloneNode(true);

    if (accountInput) {
        inputAutocomplete(accountInput, accounts, "acc_disp_name", function (c) {
            selectTranAccount(c);
        });
    }

    const searchBtn = document.getElementById("transactionSearchBtn");

    if (!searchBtn) return;

    searchBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const tbl = document.getElementById("tblTransactionBrowserItems");
        tbl.style.visibility = 'hidden';
        tbl.style.display = 'none';

        deleteRowsById(tblTransactionBrowserItems, 'rowTransactionBrowserItems');

        const params = getParams();

        showLoadingBar();
        document.getElementById('spnErrorInfo').innerHTML = "";

        fetch(`/transactionbrowser/transaction-search/?${params}`)
            .then(r => {
                hideLoadingBar();
                if (!r.ok) {
                    throw new Error(`HTTP ${r.status}`);
                }

                return r.json();
            })
            .then(data => {

                if (data.transactions && data.transactions.length > 0) {

                    let i = 0;
                    tbl.style.visibility = "visible";
                    let balance = 0;
                    let totCashIn = 0;
                    let totCashOut = 0;

                    data.transactions.forEach(item => {

                        totCashIn += item.cr_amt;
                        totCashOut += item.dr_amt;

                        if (i == 0) {
                            newRow = appendGivenRow(tbl, rowClone);
                            getInputFromRowById(newRow, 'tdCashOut').style.color = "Grey";
                            getInputFromRowById(newRow, 'tdBalance').innerHTML = formatIndianCurrency(item.open_balance);
                        }

                        newRow = appendGivenRow(tbl, rowClone);
                        getInputFromRowById(newRow, 'tdSl').innerHTML = ++i;

                        getInputFromRowById(newRow, 'tdDate').innerHTML = item.acctran_date;
                        getInputFromRowById(newRow, 'tdAccount').innerHTML = item.acc_name;

                        getInputFromRowById(newRow, 'tdType').innerHTML = item.acctran_ref_type;
                        getInputFromRowById(newRow, 'tdType').href = `/${item.acctran_ref_type.toLowerCase()}/${item.acctran_ref_rid}/`;

                        const bullet = '\u2022';
                        getInputFromRowById(newRow, 'tdNotes').innerHTML = item.acc_notes.replaceAll(` ${bullet} `, ` ${bullet} <wbr> `);
                        getInputFromRowById(newRow, 'tdNotes').style.whiteSpace = "nowrap";
                        getInputFromRowById(newRow, 'tdCashIn').innerHTML = item.cr_amt == 0 ? "-" : formatIndianCurrency(item.cr_amt);
                        getInputFromRowById(newRow, 'tdCashOut').innerHTML = item.dr_amt == 0 ? "-" : formatIndianCurrency(item.dr_amt);
                        getInputFromRowById(newRow, 'tdBalance').innerHTML = formatIndianCurrency(item.balance);

                        if (i == data.transactions.length) {
                            newRow = appendGivenRow(tbl, rowClone);
                            newRow.style.color = "Grey";
                            getInputFromRowById(newRow, 'tdNotes').style.textAlign = "right";
                            newRow.style.fontStyle = "italic";
                            getInputFromRowById(newRow, 'tdNotes').innerHTML = "Opening";
                            getInputFromRowById(newRow, 'tdCashIn').innerHTML = "(-)Cash In";
                            getInputFromRowById(newRow, 'tdCashOut').innerHTML = "Cash Out";
                            getInputFromRowById(newRow, 'tdBalance').innerHTML = "Closing";

                            newRow = appendGivenRow(tbl, rowClone);

                            getInputFromRowById(newRow, 'tdNotes').style.textAlign = "right";
                            getInputFromRowById(newRow, 'tdNotes').innerHTML = formatIndianCurrency(item.open_balance);
                            getInputFromRowById(newRow, 'tdCashIn').innerHTML = formatIndianCurrency(totCashIn);
                            getInputFromRowById(newRow, 'tdCashOut').innerHTML = formatIndianCurrency(totCashOut);
                            getInputFromRowById(newRow, 'tdBalance').innerHTML = formatIndianCurrency(item.balance);
                        }

                    });
                    tbl.style.visibility = 'visible';
                    tbl.style.display = 'block';

                } else {
                    document.getElementById('spnErrorInfo').innerHTML = "No matching records found!";
                }
            })
            .catch(error => {
                console.error("Search error:", error);
            });
    });
});

function selectTranAccount(acc) {
    const account = document.getElementById("tran_account");
    const accountRid = document.getElementById("tran_account_rid");
    const address = document.getElementById("tran_address");
    const phone = document.getElementById("tran_phone");

    if (!acc) {
        if (account) account.value = "";
        if (accountRid) accountRid.value = "";
        if (address) address.value = "";
        if (phone) phone.value = "";
        return;
    }

    if (account) account.value = acc.acc_disp_name;
    if (accountRid) accountRid.value = acc.acc_rid;
    if (address) address.value = acc.acc_address;
    if (phone) phone.value = acc.acc_phone;
}