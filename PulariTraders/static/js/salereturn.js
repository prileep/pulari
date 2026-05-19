document.addEventListener("DOMContentLoaded", function () {



    const dataEl = document.getElementById("accounts-data");
    const accounts = JSON.parse(dataEl.textContent);
    const accountInput = document.getElementById("sr_acc_name");
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(accountInput, accounts, "acc_disp_name", function (acc) {

        selectAccount(acc);

    });

    const itemInput = document.getElementById("item_name");
    initSaleReturnItem(itemInput);

    let sr_net_amount = document.getElementById("sr_net_amount").value;
    document.getElementById("sr_net_amount_words").innerHTML = numberToRupees(sr_net_amount);
});

function selectAccount(acc) {
    document.getElementById("sr_acc_rid").value = acc ? acc.acc_rid : "";
    document.getElementById("sr_acc_name").value = acc ? acc.acc_disp_name : "";
    document.getElementById("accountAddress").value = acc ? acc.acc_address : "";
    document.getElementById('sr_acc_code').value = acc ? acc.acc_code : "";
    document.getElementById("accountPhone").value = acc ? acc.acc_phone : "";

    if (acc.acc_code == "CASHPARTY") {
        document.getElementById("sr_counter_sle").checked = true;
    } else {
        document.getElementById("sr_customer_sle").checked = true;
    }
}

const radios = document.querySelectorAll("input[name='saleReturn_type']");

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
    calculateSaleReturn()
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
    initSaleReturnItem(itemInput);

}

function initSaleReturnItem(itemInput) {
    const itemsData = document.getElementById("items-data");
    const items = JSON.parse(itemsData.textContent);
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(itemInput, items, "item_display_name", function (c) {
        itemInput.value = c.item_display_name;
        //srd_amount
        let row = thGetRow(itemInput);

        getInputFromRowById(row, "srd_amount").value = parseFloat(c.item_sale_price || 0).toFixed(2);
        getInputFromRowById(row, "item_stk").value = parseFloat(c.item_stk || 0).toFixed(2);

        getInputFromRowById(row, "srd_item_rid").value = c.item_rid;
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

function calculateSaleReturn() {

    let srd_qty = document.getElementsByName("srd_qty");
    let srd_amount = document.getElementsByName("srd_amount");
    let srd_total_amount = document.getElementsByName("srd_total_amount");
    let grandTotal = parseFloat(0);

    for (let i = 0; i < srd_qty.length; i++) {

        let quantity = parseFloat(srd_qty[i].value) || 0;
        let amount = parseFloat(srd_amount[i].value) || 0;

        let total = quantity * amount;

        if (srd_total_amount[i]) {
            srd_total_amount[i].value = total.toFixed(2);
        }
        grandTotal = (grandTotal + total);
    }

    let sr_amount = grandTotal;
    let sr_net_amount = Math.floor(grandTotal);
    let sr_discount = (sr_amount - sr_net_amount);

    document.getElementById("sr_amount").value = sr_amount.toFixed(2);
    document.getElementById("sr_net_amount").value = sr_net_amount.toFixed(2);
    document.getElementById("sr_discount").value = sr_discount.toFixed(2);
    document.getElementById("sr_net_amount_words").innerHTML = numberToRupees(sr_net_amount);
}

function adjustAmount() {
    let sr_net_amount = parseFloat(document.getElementById("sr_net_amount").value);
    let sr_amount = parseFloat(document.getElementById("sr_amount").value);
    let sr_discount = (sr_amount - sr_net_amount);

    document.getElementById("sr_amount").value = sr_amount.toFixed(2);
    document.getElementById("sr_net_amount").value = sr_net_amount.toFixed(2);
    document.getElementById("sr_discount").value = sr_discount.toFixed(2);

    document.getElementById("sr_net_amount_words").innerHTML = numberToRupees(sr_net_amount);
}

function refreshitem() {
    let slNos = document.getElementsByName("slno");
    for (let i = 0; i < slNos.length; i++) {
        slNos[i].value = i + 1;
    }

}

function selectAccount(acc) {
    document.getElementById("sr_acc_rid").value = acc ? acc.acc_rid : "";
    document.getElementById("sr_acc_name").value = acc ? acc.acc_disp_name : "";
    document.getElementById("accountAddress").value = acc ? acc.acc_address : "";
    document.getElementById('sr_acc_code').value = acc ? acc.acc_code : "";
    document.getElementById("accountPhone").value = acc ? acc.acc_phone : "";

    if (acc.acc_code == "CASHPARTY") {
        document.getElementById("sr_counter_sle").checked = true;
    } else {
        document.getElementById("sr_customer_sle").checked = true;
    }
}

function setSaleType(type) {

    //Account Sale
    if (type == 0) {
        selectAccount(null);
    } else {
        const dataEl = document.getElementById("accounts-data");
        const accounts = JSON.parse(dataEl.textContent);

        const acc = accounts.find(
            acc => acc.acc_code === "CASHPARTY"
        );
        selectAccount(acc);
    }
}