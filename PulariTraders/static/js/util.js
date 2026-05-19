function numberToRupees(num) {
    num = parseFloat(num || 0).toFixed(2);

    let parts = num.split(".");
    let rupees = parseInt(parts[0]);
    let paise = parseInt(parts[1]);

    const ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
        "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
        "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];

    const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty",
        "Sixty", "Seventy", "Eighty", "Ninety"];

    function words(n) {
        if (n < 20) return ones[n];
        if (n < 100) return tens[Math.floor(n / 10)] + " " + ones[n % 10];
        if (n < 1000) return ones[Math.floor(n / 100)] + " Hundred " + words(n % 100);
        if (n < 100000) return words(Math.floor(n / 1000)) + " Thousand " + words(n % 1000);
        if (n < 10000000) return words(Math.floor(n / 100000)) + " Lakh " + words(n % 100000);
        return words(Math.floor(n / 10000000)) + " Crore " + words(n % 10000000);
    }

    let result = words(rupees) + " Rupees";

    if (paise > 0) {
        result += " and " + words(paise) + " Paise";
    }

    return result + " Only";
}

function formatNegative(value) {

    value = Number(value);

    if (value < 0) {
        return "(-)" + Math.abs(value);
    }

    return value.toString();
}

function showLoadingBar() {

    const loadingContainer = document.getElementById("loadingContainer");

    loadingContainer.style.visibility = "visible";
    loadingContainer.style.display = "block";
    loadingContainer.style.opacity = "0";

    setTimeout(() => {
        loadingContainer.style.transition = "opacity 0.3s ease";
        loadingContainer.style.opacity = "1";
    }, 10);
}

function hideLoadingBar() {

    const loadingContainer = document.getElementById("loadingContainer");

    loadingContainer.style.visibility = "hidden";
    loadingContainer.style.display = "none";
}

function formatIndianCurrency(amount) {

    return new Intl.NumberFormat('en-IN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);

}

function mergeCells(firstTd, columnCount) {

    if (!firstTd || columnCount < 2) return;

    // Set colspan
    firstTd.colSpan = columnCount;

    // Remove next sibling tds
    let nextTd = firstTd.nextElementSibling;

    for (let i = 1; i < columnCount && nextTd; i++) {

        const tdToRemove = nextTd;
        nextTd = nextTd.nextElementSibling;

        tdToRemove.remove();
    }
}