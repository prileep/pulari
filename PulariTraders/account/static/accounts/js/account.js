document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("accountForm");

    form.addEventListener("submit", function (e) {

        let name = document.querySelector("input[name='acc_name']").value.trim();
        let place = document.querySelector("input[name='acc_place']").value.trim();

        let customer = document.getElementById("acc_is_customer").value;
        let supplier = document.getElementById("acc_is_supplier").value;
        let staff = document.getElementById("acc_is_staff").value;

        // NAME CHECK
        if (name === "") {
            alert("Enter Account Name");
            e.preventDefault();
            return;
        }

        // PLACE CHECK
        if (place === "") {
            alert("Enter Place");
            e.preventDefault();
            return;
        }

        // SELECT CHECK
        if (customer === "" || supplier === "" || staff === "") {
            alert("Please select Customer, Supplier, Staff");
            e.preventDefault();
            return;
        }

    });

});