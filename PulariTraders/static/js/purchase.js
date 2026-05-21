document.addEventListener("DOMContentLoaded", function () {

    const addressInput = document.getElementById("accountAddress");
    const phoneInput = document.getElementById("accountPhone");

    const dataEl = document.getElementById("accounts-data");
    const accounts = JSON.parse(dataEl.textContent);
    const accountInput = document.getElementById("ph_acc_name");
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(accountInput, accounts, "acc_disp_name", function (c) {
        document.getElementById("ph_acc_rid").value = c.acc_rid;
        addressInput.value = c.acc_address;
        phoneInput.value = c.acc_phone;
        document.getElementById('ph_acc_code').value = c.acc_code;
    });

    const itemInput = document.getElementById("item_name");
    initPurchaseItem(itemInput);

    let ph_net_amount = document.getElementById("ph_net_amount").value;
    document.getElementById("ph_net_amount_words").innerHTML = numberToRupees(ph_net_amount);
});

const radios = document.querySelectorAll("input[name='purchase_type']");

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
    calculatePurchase()
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
    initPurchaseItem(itemInput);

}

function initPurchaseItem(itemInput) {
    const itemsData = document.getElementById("items-data");
    const items = JSON.parse(itemsData.textContent);
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(itemInput, items, "item_display_name", function (c) {
        itemInput.value = c.item_display_name;

        let row = thGetRow(itemInput);

        getInputFromRowById(row, "pd_amount").value = parseFloat(c.item_sale_price || 0).toFixed(2);
        getInputFromRowById(row, "item_stk").value = parseFloat(c.item_stk || 0).toFixed(2);

        getInputFromRowById(row, "pd_item_rid").value = c.item_rid;
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

function calculatePurchase() {

    let pd_qty = document.getElementsByName("pd_qty");
    let pd_amount = document.getElementsByName("pd_amount");
    let pd_total_amount = document.getElementsByName("pd_total_amount");
    let grandTotal = parseFloat(0);

    for (let i = 0; i < pd_qty.length; i++) {

        let quantity = parseFloat(pd_qty[i].value) || 0;
        let amount = parseFloat(pd_amount[i].value) || 0;

        let total = quantity * amount;

        if (pd_total_amount[i]) {
            pd_total_amount[i].value = total.toFixed(2);
        }
        grandTotal = (grandTotal + total);
    }

    let ph_amount = grandTotal;
    let ph_net_amount = Math.floor(grandTotal);
    let ph_discount = (ph_amount - ph_net_amount);

    document.getElementById("ph_amount").value = ph_amount.toFixed(2);
    document.getElementById("ph_net_amount").value = ph_net_amount.toFixed(2);
    document.getElementById("ph_discount").value = ph_discount.toFixed(2);
    document.getElementById("ph_net_amount_words").innerHTML = numberToRupees(ph_net_amount);
}

function adjustAmount() {
    let ph_net_amount = parseFloat(document.getElementById("ph_net_amount").value);
    let ph_amount = parseFloat(document.getElementById("ph_amount").value);
    let ph_discount = (ph_amount - ph_net_amount);

    document.getElementById("ph_amount").value = ph_amount.toFixed(2);
    document.getElementById("ph_net_amount").value = ph_net_amount.toFixed(2);
    document.getElementById("ph_discount").value = ph_discount.toFixed(2);

    document.getElementById("ph_net_amount_words").innerHTML = numberToRupees(ph_net_amount);
}

function refreshitem() {
    let slNos = document.getElementsByName("slno");
    for (let i = 0; i < slNos.length; i++) {
        slNos[i].value = i + 1;
    }

}

function openPrintPurchase(rid) {

    const url = `/purchase/print/${rid}/`;

    const win = window.open(
        url,
        '_blank',
        'width=900,height=700'
    );

    win.onload = function () {
        win.focus();
        win.print();
    };
}