document.addEventListener("DOMContentLoaded", function () {



    const dataEl = document.getElementById("accounts-data");
    const accounts = JSON.parse(dataEl.textContent);
    const accountInput = document.getElementById("br_acc_name");
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(accountInput, accounts, "acc_disp_name", function (acc) {

        selectAccount(acc);

    });

    const itemInput = document.getElementById("item_name");
    initBillReturnItem(itemInput);

    let br_net_amount = document.getElementById("br_net_amount").value;
    document.getElementById("br_net_amount_words").innerHTML = numberToRupees(br_net_amount);
});

function selectAccount(acc) {
    document.getElementById("br_acc_rid").value = acc ? acc.acc_rid : "";
    document.getElementById("br_acc_name").value = acc ? acc.acc_disp_name : "";
    document.getElementById("accountAddress").value = acc ? acc.acc_address : "";
    document.getElementById('br_acc_code').value = acc ? acc.acc_code : "";
    document.getElementById("accountPhone").value = acc ? acc.acc_phone : "";

    if (acc.acc_code == "CASHPARTY") {
        document.getElementById("br_counter_sle").checked = true;
    } else {
        document.getElementById("br_customer_sle").checked = true;
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
    calculateBillReturn();
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
    initBillReturnItem(itemInput);

}

function initBillReturnItem(itemInput) {
    const itemsData = document.getElementById("items-data");
    const items = JSON.parse(itemsData.textContent);
    // 🔥 Initialize autocomplete with callback
    inputAutocomplete(itemInput, items, "item_display_name", function (c) {
        itemInput.value = c.item_display_name;
        //brd_amount
        let row = thGetRow(itemInput);

        getInputFromRowById(row, "brd_amount").placeholder = parseFloat(c.item_sale_price || 0).toFixed(2);
        getInputFromRowById(row, "item_stk").value = parseFloat(c.item_stk || 0).toFixed(2);

        getInputFromRowById(row, "brd_item_rid").value = c.item_rid;
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

function calculateBillReturn() {

    let brd_qty = document.getElementsByName("brd_qty");
    let brd_amount = document.getElementsByName("brd_amount");
    let brd_total_amount = document.getElementsByName("brd_total_amount");
    let grandTotal = parseFloat(0);

    for (let i = 0; i < brd_qty.length; i++) {

        let quantity = parseFloat(brd_qty[i].value) || 0;
        let amount = parseFloat(brd_amount[i].value) || 0;

        let total = quantity * amount;

        if (brd_total_amount[i]) {
            brd_total_amount[i].value = total.toFixed(2);
        }
        grandTotal = (grandTotal + total);
    }

    let br_amount = grandTotal;
    let br_net_amount = Math.floor(grandTotal);
    let br_discount = (br_amount - br_net_amount);

    document.getElementById("br_amount").value = br_amount.toFixed(2);
    document.getElementById("br_net_amount").value = br_net_amount.toFixed(2);
    document.getElementById("br_discount").value = br_discount.toFixed(2);
    document.getElementById("br_net_amount_words").innerHTML = numberToRupees(br_net_amount);
}

function adjustAmount() {
    let br_net_amount = parseFloat(document.getElementById("br_net_amount").value);
    let br_amount = parseFloat(document.getElementById("br_amount").value);
    let br_discount = (br_amount - br_net_amount);

    document.getElementById("br_amount").value = br_amount.toFixed(2);
    document.getElementById("br_net_amount").value = br_net_amount.toFixed(2);
    document.getElementById("br_discount").value = br_discount.toFixed(2);

    document.getElementById("br_net_amount_words").innerHTML = numberToRupees(br_net_amount);
}

function refreshitem() {
    let slNos = document.getElementsByName("slno");
    for (let i = 0; i < slNos.length; i++) {
        slNos[i].value = i + 1;
    }

}

function selectAccount(acc) {
    document.getElementById("br_acc_rid").value = acc ? acc.acc_rid : "";
    document.getElementById("br_acc_name").value = acc ? acc.acc_disp_name : "";
    document.getElementById("accountAddress").value = acc ? acc.acc_address : "";
    document.getElementById('br_acc_code').value = acc ? acc.acc_code : "";
    document.getElementById("accountPhone").value = acc ? acc.acc_phone : "";

    if (acc.acc_code == "CASHPARTY") {
        document.getElementById("br_counter_sle").checked = true;
    } else {
        document.getElementById("br_customer_sle").checked = true;
    }
}

function setBillType(type) {

    //Account Bill
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