document.addEventListener("DOMContentLoaded", function () {



    const dataEl = document.getElementById("accounts-data");
    const accounts = JSON.parse(dataEl.textContent);
    const accountInput = document.getElementById("bh_acc_name");
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(accountInput, accounts, "acc_disp_name", function (acc) {

        selectAccount(acc);

    });

    const itemInput = document.getElementById("item_name");
    initBillItem(itemInput);

    let bh_net_amount = document.getElementById("bh_net_amount").value;
    document.getElementById("bh_net_amount_words").innerHTML = numberToRupees(bh_net_amount);
});

function selectAccount(acc) {
    document.getElementById("bh_acc_rid").value = acc ? acc.acc_rid : "";
    document.getElementById("bh_acc_name").value = acc ? acc.acc_disp_name : "";
    document.getElementById("accountAddress").value = acc ? acc.acc_address : "";
    document.getElementById('bh_acc_code').value = acc ? acc.acc_code : "";
    document.getElementById("accountPhone").value = acc ? acc.acc_phone : "";

    if (acc.acc_code == "CASHPARTY") {
        document.getElementById("bh_counter_sle").checked = true;
    } else {
        document.getElementById("bh_customer_sle").checked = true;
    }
}

const radios = document.querySelectorAll("input[name='bill_type']");

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
    calculateBill()
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
    initBillItem(itemInput);

}

function initBillItem(itemInput) {
    const itemsData = document.getElementById("items-data");
    const items = JSON.parse(itemsData.textContent);
    // 🔥 Initialize autocomplete with callback

    inputAutocomplete(itemInput, items, "item_display_name", function (c) {
        itemInput.value = c.item_display_name;
        //bd_amount
        let row = thGetRow(itemInput);

        getInputFromRowById(row, "bd_amount").value = parseFloat(c.item_sale_price || 0).toFixed(2);
        getInputFromRowById(row, "item_stk").value = parseFloat(c.item_stk || 0).toFixed(2);

        getInputFromRowById(row, "bd_item_rid").value = c.item_rid;
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

function calculateBill() {

    let bd_qty = document.getElementsByName("bd_qty");
    let bd_amount = document.getElementsByName("bd_amount");
    let bd_total_amount = document.getElementsByName("bd_total_amount");
    let grandTotal = parseFloat(0);

    for (let i = 0; i < bd_qty.length; i++) {

        let quantity = parseFloat(bd_qty[i].value) || 0;
        let amount = parseFloat(bd_amount[i].value) || 0;

        let total = quantity * amount;

        if (bd_total_amount[i]) {
            bd_total_amount[i].value = total.toFixed(2);
        }
        grandTotal = (grandTotal + total);
    }

    let bh_amount = grandTotal;
    let bh_net_amount = Math.floor(grandTotal);
    let bh_discount = (bh_amount - bh_net_amount);

    document.getElementById("bh_amount").value = bh_amount.toFixed(2);
    document.getElementById("bh_net_amount").value = bh_net_amount.toFixed(2);
    document.getElementById("bh_discount").value = bh_discount.toFixed(2);
    document.getElementById("bh_net_amount_words").innerHTML = numberToRupees(bh_net_amount);
}

function adjustAmount() {
    let bh_net_amount = parseFloat(document.getElementById("bh_net_amount").value);
    let bh_amount = parseFloat(document.getElementById("bh_amount").value);
    let bh_discount = (bh_amount - bh_net_amount);

    document.getElementById("bh_amount").value = bh_amount.toFixed(2);
    document.getElementById("bh_net_amount").value = bh_net_amount.toFixed(2);
    document.getElementById("bh_discount").value = bh_discount.toFixed(2);

    document.getElementById("bh_net_amount_words").innerHTML = numberToRupees(bh_net_amount);
}

function refreshitem() {
    let slNos = document.getElementsByName("slno");
    for (let i = 0; i < slNos.length; i++) {
        slNos[i].value = i + 1;
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

function openPrintBill(rid) {

    const url = `/bill/print/${rid}/`;

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