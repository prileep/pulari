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
    const dueAmtInput = document.getElementById("rcpt_account_due_amt");

    if (!acc) {
        rcpt_acc_rid.value = "";
        rcpt_account_name.value = "";
        rcpt_account_code.value = "";
        absShowAccountBalanceSheet(rcpt_acc_rid.value, dueAmtInput);
        return;
    }

    rcpt_acc_rid.value = acc.acc_rid;
    rcpt_account_name.value = acc.acc_disp_name;
    rcpt_account_code.value = acc.acc_code;

    absShowAccountBalanceSheet(rcpt_acc_rid.value, dueAmtInput);
}