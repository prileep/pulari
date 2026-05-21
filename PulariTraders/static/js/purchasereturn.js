document.addEventListener("DOMContentLoaded", function () {

    const addressInput = document.getElementById("accountAddress");
    const phoneInput = document.getElementById("accountPhone");

    const dataEl = document.getElementById("accounts-data");
    const accounts = JSON.parse(dataEl.textContent);
    const accountInput = document.getElementById("pr_acc_name");
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(accountInput, accounts, "acc_disp_name", function (c) {
        document.getElementById("pr_acc_rid").value = c.acc_rid;
        addressInput.value = c.acc_address;
        phoneInput.value = c.acc_phone;
        document.getElementById('pr_acc_code').value = c.acc_code;
    });

    const itemInput = document.getElementById("item_name");
    initPurchaseReturnItem(itemInput);

    let pr_net_amount = document.getElementById("pr_net_amount").value;
    document.getElementById("pr_net_amount_words").innerHTML = numberToRupees(pr_net_amount);
});

const radios = document.querySelectorAll("input[name='purchaseReturn_type']");

function setReadonlyState(isReadonly) {

    const fields = [accountInput, addressInput, phoneInput];

    fields.forEach(field => {
        if (!field) return;

        field.readOnly = isReadonly;

        if (isReadonly) {
            field.classList.add("readonly-style");
            field.style.pointerEvents = "none"; // disable autocomplete clicks
        } else {
            field.classList.remove("readonly-style");
            field.style.pointerEvents = "auto";
        }
    });
}

function handleQtyChange(el) {

    cloneItemRow(el);
    calculatePurchaseReturn();
}

function cloneItemRow(el) {
    const row = el.closest("tr");
    const container = row.parentElement;

    if (row !== container.lastElementChild) return;

    const clone = row.cloneNode(true);

    // clear inputs
    clone.querySelectorAll("input").forEach(input => {
        input.value = "";
    });

    container.appendChild(clone);

    // ✅ get element inside cloned row
    const itemInput = clone.querySelector("#item_name");
    initPurchaseReturnItem(itemInput);

}

function initPurchaseReturnItem(itemInput) {
    const itemsData = document.getElementById("items-data");
    const items = JSON.parse(itemsData.textContent);
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(itemInput, items, "item_display_name", function (c) {
        itemInput.value = c.item_display_name;
        //prd_amount
        let row = thGetRow(itemInput);

        getInputFromRowById(row, "prd_amount").value = parseFloat(c.item_sale_price || 0).toFixed(2);
        getInputFromRowById(row, "item_stk").value = parseFloat(c.item_stk || 0).toFixed(2);

        getInputFromRowById(row, "prd_item_rid").value = c.item_rid;
    });
    refreshitem();
}

document.addEventListener("blur", function (e) {
    if (e.target.matches('input[type="number"]')) {
        let val = e.target.value.trim();

        // 👉 keep empty as empty
        if (val === "") return;

        let num = parseFloat(val);

        // 👉 if invalid or zero → 0.00
        if (isNaN(num) || num === 0) {
            e.target.value = "0.00";
        } else {
            e.target.value = num.toFixed(2);
        }
    }
}, true);

function calculatePurchaseReturn() {

    let prd_qty = document.getElementsByName("prd_qty");
    let prd_amount = document.getElementsByName("prd_amount");
    let prd_total_amount = document.getElementsByName("prd_total_amount");
    let grandTotal = parseFloat(0);

    for (let i = 0; i < prd_qty.length; i++) {

        let quantity = parseFloat(prd_qty[i].value) || 0;
        let amount = parseFloat(prd_amount[i].value) || 0;

        let total = quantity * amount;

        if (prd_total_amount[i]) {
            prd_total_amount[i].value = total.toFixed(2);
        }
        grandTotal = (grandTotal + total);
    }

    let pr_amount = grandTotal;
    let pr_net_amount = Math.floor(grandTotal);
    let pr_discount = (pr_amount - pr_net_amount);

    document.getElementById("pr_amount").value = pr_amount.toFixed(2);
    document.getElementById("pr_net_amount").value = pr_net_amount.toFixed(2);
    document.getElementById("pr_discount").value = pr_discount.toFixed(2);
    document.getElementById("pr_net_amount_words").innerHTML = numberToRupees(pr_net_amount);
}

function adjustAmount() {
    let pr_net_amount = parseFloat(document.getElementById("pr_net_amount").value);
    let pr_amount = parseFloat(document.getElementById("pr_amount").value);
    let pr_discount = (pr_amount - pr_net_amount);

    document.getElementById("pr_amount").value = pr_amount.toFixed(2);
    document.getElementById("pr_net_amount").value = pr_net_amount.toFixed(2);
    document.getElementById("pr_discount").value = pr_discount.toFixed(2);

    document.getElementById("pr_net_amount_words").innerHTML = numberToRupees(pr_net_amount);
}

function refreshitem() {
    let slNos = document.getElementsByName("slno");
    for (let i = 0; i < slNos.length; i++) {
        slNos[i].value = i + 1;
    }

}