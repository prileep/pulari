document.addEventListener("DOMContentLoaded", function () {

    const dataEl = document.getElementById("accounts-data");
    const accounts = dataEl ? JSON.parse(dataEl.textContent) : [];

    const accountInput = document.getElementById("disc_account_name");

    if (accountInput) {

        inputAutocomplete(
            accountInput,
            accounts,
            "acc_disp_name",
            function (acc) {
                selectDiscountAccount(acc);
            }
        );
    }
});


function selectDiscountAccount(acc) {

    const disc_acc_rid = document.getElementById("disc_acc_rid");
    const disc_account_name = document.getElementById("disc_account_name");
    const disc_account_code = document.getElementById("disc_account_code");

    if (!acc) {
        disc_acc_rid.value = "";
        disc_account_name.value = "";
        disc_account_code.value = "";

        absShowAccountBalanceSheet(disc_acc_rid.value, disc_account_due_amt);
        return;
    }

    disc_acc_rid.value = acc.acc_rid;
    disc_account_name.value = acc.acc_disp_name;
    disc_account_code.value = acc.acc_code;

    absShowAccountBalanceSheet(disc_acc_rid.value, disc_account_due_amt);
}