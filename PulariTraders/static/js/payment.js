document.addEventListener("DOMContentLoaded", function () {

    const dataEl = document.getElementById("accounts-data");
    const accounts = dataEl ? JSON.parse(dataEl.textContent) : [];

    const accountInput = document.getElementById("pay_account_name");

    if (accountInput) {

        inputAutocomplete(
            accountInput,
            accounts,
            "acc_disp_name",
            function (acc) {
                selectPaymentAccount(acc);
            }
        );
    }
});


function selectPaymentAccount(acc) {

    const pay_acc_rid = document.getElementById("pay_acc_rid");
    const pay_account_name = document.getElementById("pay_account_name");
    const pay_account_code = document.getElementById("pay_account_code");
    const pay_account_due_amt = document.getElementById("pay_account_due_amt");

    if (!acc) {
        pay_acc_rid.value = "";
        pay_account_name.value = "";
        pay_account_code.value = "";
        absShowAccountBalanceSheet(pay_acc_rid.value, pay_account_due_amt);
        return;
    }

    pay_acc_rid.value = acc.acc_rid;
    pay_account_name.value = acc.acc_disp_name;
    pay_account_code.value = acc.acc_code;

    absShowAccountBalanceSheet(pay_acc_rid.value, pay_account_due_amt);

}