let currentFocus = -1;
let suggestionItems = [];

function inputAutocomplete(input, json, displayField, onSelect) {

    const box = document.getElementById("suggestionBox");

    function closeSuggestions() {
        box.innerHTML = "";
        box.style.display = "none";
        currentFocus = -1;
        suggestionItems = [];
    }

    function selectAutoComplete(c) {
        input.value = c[displayField];

        closeSuggestions();

        if (typeof onSelect === "function") {
            onSelect(c);
        }
    }

    function highlight() {

        if (suggestionItems.length === 0) return;

        suggestionItems.forEach(item =>
            item.classList.remove("active")
        );

        if (currentFocus >= suggestionItems.length) {
            currentFocus = suggestionItems.length - 1;
        }

        if (currentFocus < 0) {
            currentFocus = 0;
        }

        suggestionItems[currentFocus].classList.add("active");
    }

    // =========================
    // SEARCH
    // =========================
    input.addEventListener("input", function () {

        let filter = this.value.toLowerCase().trim();

        box.innerHTML = "";

        currentFocus = -1;
        suggestionItems = [];

        if (!filter) {
            closeSuggestions();
            return;
        }

        // POSITION
        const rect = input.getBoundingClientRect();

        box.style.position = "absolute";
        box.style.top = (rect.bottom + window.scrollY) + "px";
        box.style.left = (rect.left + window.scrollX) + "px";
        box.style.width = rect.width + "px";
        box.style.minWidth = rect.width + "px";
        box.style.boxSizing = "border-box";

        json.forEach(c => {

            let disp = (c[displayField] || "").toLowerCase();

            if (disp.includes(filter)) {

                let div = document.createElement("div");

                div.classList.add("suggestion-item");

                let original = c[displayField];
                let lower = original.toLowerCase();

                let start = lower.indexOf(filter);

                if (start !== -1) {

                    let end = start + filter.length;

                    div.innerHTML =
                        original.substring(0, start) +
                        "<b>" +
                        original.substring(start, end) +
                        "</b>" +
                        original.substring(end);

                } else {

                    div.textContent = original;
                }

                div.onclick = function () {
                    selectAutoComplete(c);
                };

                box.appendChild(div);

                suggestionItems.push(div);
            }
        });

        box.style.display =
            suggestionItems.length ? "block" : "none";

        // FIRST ITEM ACTIVE
        if (suggestionItems.length > 0) {

            currentFocus = 0;

            highlight();
        }
    });

    // =========================
    // KEYBOARD NAVIGATION
    // =========================
    input.addEventListener("keydown", function (e) {

        if (suggestionItems.length === 0) return;

        // DOWN
        if (e.key === "ArrowDown") {

            e.preventDefault();

            if (currentFocus < suggestionItems.length - 1) {
                currentFocus++;
            }

            highlight();
        }

        // UP
        if (e.key === "ArrowUp") {

            e.preventDefault();

            if (currentFocus > 0) {
                currentFocus--;
            }

            highlight();
        }

        // ENTER
        if (e.key === "Enter") {

            e.preventDefault();

            if (
                currentFocus > -1 &&
                suggestionItems[currentFocus]
            ) {
                suggestionItems[currentFocus].click();
            }
        }
    });

    // =========================
    // CLICK OUTSIDE
    // =========================
    document.addEventListener("mousedown", function (e) {

        if (
            !input.contains(e.target) &&
            !box.contains(e.target)
        ) {
            closeSuggestions();
        }

    }, true);
}