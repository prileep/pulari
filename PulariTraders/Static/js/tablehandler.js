function thGetRow(elem) {
    return elem.closest("tr");
}

function getInputFromRowById(row, inputId) {

    if (!row || !inputId) return null;

    // search inside the row for the element with given id
    return row.querySelector("#" + inputId);
}

function appendGivenRow(table, row) {

    const newRow = row.cloneNode(true);

    // clear inputs
    newRow.querySelectorAll("input").forEach(input => {
        input.value = "";
    });

    table.appendChild(newRow);
    return newRow;

}

function deleteRowsById(table, rowId) {

    if (!table) {
        console.error("Table not found:", tableId);
        return;
    }
    const rows = table.querySelectorAll(`#${rowId}`);
    rows.forEach(row => row.remove());
}