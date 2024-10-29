const modal = document.querySelector(".modal");
const modalContainer = document.querySelector(".modal__container");
const modalForm = document.querySelector(".modal__form");
let tables = [];
let data = [];

// Fetch and render the initial list of tables and data
async function renderIndex() {
    try {
        tables = await fetchTables();
        renderTableList(tables);
        const firstTable = Object.keys(tables)[0];
        renderTableView(firstTable, tables[firstTable]);
    } catch (err) {
        console.error("Error fetching tables:", err);
    }
}

// Fetch table descriptions
async function fetchTables() {
    try {
        const response = await fetch("http://localhost:3000/php/describe_tables.php");

        if (response.status === 401)
            window.location.replace("http://localhost:3000/login.html");

        return await response.json();
    } catch (err) {
        throw new Error("Failed to fetch table descriptions");
    }
}

// Render the list of tables
function renderTableList(tables) {
    const tablesList = document.querySelector(".tables__list");
    tablesList.innerHTML = Object.keys(tables).map(createTableButton).join("");

    const allButtons = document.querySelectorAll(".tables__button");
    setActiveTableButton(allButtons[0]);

    allButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            setActiveTableButton(button);
            renderTableView(button.id, tables[button.id]);
        });
    });
}

// Create a table button for each table
function createTableButton(tableName) {
    return `
        <li class="tables__item">
            <button id="${tableName}" title="${tableName}" class="tables__button">
                <span class="material-symbols-outlined">table</span>
                ${tableName.toUpperCase()}
            </button>
        </li>
    `;
}

// Set the active table button
function setActiveTableButton(activeButton) {
    document.querySelectorAll(".tables__button").forEach(button => {
        button.classList.remove("tables__button--active");
    });
    activeButton.classList.add("tables__button--active");
}

// Get the currently active table name
function getActiveTableName() {
    return document.querySelector(".tables__button--active").id;
}

// Render the table view with fields and data
async function renderTableView(tableName, table) {
    document.querySelector(".table-title").textContent = `Tabela ${tableName}`;
    data = await fetchTableData(tableName);

    if (data) {
        renderTableHead(table);
        renderTableBody(data, table);
    }
}

// Fetch table data
async function fetchTableData(tableName) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/${tableName}/`);
        return await response.json();
    } catch (err) {
        console.error(`Error fetching data for ${tableName}:`, err);
        return [];
    }
}

// Render table head with columns
function renderTableHead(table) {
    const tableHead = table.map(createTableHeaderCell).join("");
    document.querySelector(".table__columns").innerHTML = `<thead><tr>${tableHead}</tr></thead>`;
}

// Create table header cell
function createTableHeaderCell(field) {
    return `
        <th scope="col">
            ${field.Field}<br> ${field.Type.toUpperCase()} ${field.Null === "NO" ? "NOT NULL" : ""} ${field.Key}
        </th>
    `;
}

// Render table body with data rows
function renderTableBody(data, table) {
    const pkFields = table.filter(field => field.Key === "PRI").map(pk => pk.Field);
    const tableRows = data.map(row => createTableRow(row, table, pkFields)).join("");
    document.querySelector(".table__rows").innerHTML = tableRows;

    addTableRowEventListeners();
}

// Create a table row
function createTableRow(row, table, pkFields) {
    const rowId = pkFields.map(pk => row[pk]).join("-");
    const cells = table.map(field => createTableCell(row, field)).join("");
    return `<tr id="${rowId}">${cells}</tr>`;
}

// Create table cell
function createTableCell(row, field) {
    const content = field.Key === "PRI" ? `<th scope="row">${row[field.Field]}</th>` : `<td>${row[field.Field]}</td>`;
    return content;
}

// Add click event listeners to each row
function addTableRowEventListeners() {
    const allTableRows = document.querySelectorAll(".table tbody tr");
    document.querySelector(".head__right").classList.add("head__right--disabled");

    allTableRows.forEach(row => {
        row.addEventListener("click", () => {
            document.querySelectorAll(".table tbody tr").forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");
            document.querySelector(".head__right").classList.remove("head__right--disabled");
        });
    });
}

// Create modal input fields
function createModalInput(field, value = "", allowEditPks = false, showIdField = false) {
    if (field.Field === "id" && !showIdField) return '';  // Skip 'id' field, if necessary

    const inputType = getInputType(field.Type);
    const maxLength = field.Type.includes("varchar") ? field.Type.match(/\d+/)[0] : null;

    return `
        <div class="modal__item">
            <label class="modal__label" for="${field.Field}">${field.Field} ${field.Type} ${field.Key}</label>
            <input class="modal__input" type="${inputType}" value="${value}" name="${field.Field}" id="${field.Field}" ${field.Null === "NO" ? "required" : ""} ${maxLength ? `maxlength="${maxLength}"` : ""} ${!allowEditPks && field.Key === "PRI" ? "readonly" : ""}>
        </div>
    `;
}

// Get appropriate input type for a field
function getInputType(fieldType) {
    if (fieldType.includes("int")) return "number";
    if (fieldType.includes("varchar")) return "text";
    if (fieldType === "date") return "date";
    if (fieldType === "datetime") return "datetime-local";
    return "text";
}

// Render the insert modal
function renderInsertModal(tableName, table) {
    modalForm.onsubmit = handleInsertSubmit;
    modal.classList.remove("modal--hidden");
    modalForm.innerHTML = `<h2 class="modal__title">Inserir em ${tableName}</h2>` +
        table.map(field => createModalInput(field, "", true)).join("") +
        `<input class="modal__submit" type="submit" value="Inserir">`;
}

// Render the update modal
async function renderUpdateModal(tableName, table) {
    const rowData = await getDataFromSelectedRow();
    modalForm.onsubmit = handleUpdateSubmit;

    modal.classList.remove("modal--hidden");
    modalForm.innerHTML = `<h2 class="modal__title">Atualizar registro em ${tableName}</h2>` +
        table.map(field => createModalInput(field, rowData[field.Field], false, true)).join("") +
        `<input class="modal__submit" type="submit" value="Atualizar">`;
}

// Handle insert form submission
async function handleInsertSubmit(event) {
    event.preventDefault();
    const formData = new FormData(modalForm);
    await insertIntoDatabase(Object.fromEntries(formData.entries()));
}

// Handle update form submission
async function handleUpdateSubmit(event) {
    event.preventDefault();
    const formData = new FormData(modalForm);
    await updateFromDatabase(Object.fromEntries(formData.entries()));
}

// Insert data into the database
async function insertIntoDatabase(jsonBody) {
    const tableName = getActiveTableName();
    try {
        const res = await fetch(`http://127.0.0.1:8000/${tableName}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonBody)
        });

        const json = await res.json();
        if (res.status !== 200) {
            alert(`Ocorreu um erro na inserção do registro: ${json.detail}`);
        } else {
            closeModal();
            renderTableView(tableName, tables[tableName]);
        }
    } catch (err) {
        console.error("Insert error:", err);
    }
}

// Update data in the database
async function updateFromDatabase(jsonBody) {
    const tableName = getActiveTableName();
    try {
        const res = await fetch(`http://127.0.0.1:8000/${tableName}/`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonBody)
        });

        const json = await res.json();
        if (res.status !== 200) {
            alert(`Ocorreu um erro na atualização do registro: ${json.detail}`);
        } else {
            closeModal();
            renderTableView(tableName, tables[tableName]);
        }
    } catch (err) {
        console.error("Update error:", err);
    }
}

// Delete data from the database
async function deleteFromDatabase(pks, values) {
    const tableName = getActiveTableName();
    const formData = new FormData();
    pks.forEach((pk, i) => formData.append(pk, values[i]));
    const queryString = new URLSearchParams(formData).toString();

    if (confirm(`Deletar registro da tabela ${tableName}?`)) {
        try {
            const res = await fetch(`http://127.0.0.1:8000/${tableName}/?${queryString}`, {
                method: "DELETE"
            });

            const json = await res.json();
            if (res.status !== 200) {
                alert(`Ocorreu um erro na exclusão do registro: ${json.detail}`);
            } else {
                closeModal();
                renderTableView(tableName, tables[tableName]);
            }
        } catch (err) {
            console.error("Delete error:", err);
        }
    }
}

// Get primary key values from the selected row
function getPksFromSelectedRow() {
    const tableName = getActiveTableName();
    const pkFields = tables[tableName].filter(field => field.Key === "PRI").map(pk => pk.Field);
    const values = document.querySelector(".table tbody .selected").id.split("-");
    return { pkFields, values };
}

// Get data of the selected row
async function getDataFromSelectedRow() {
    const { pkFields, values } = getPksFromSelectedRow();
    const tableName = getActiveTableName();

    data = await fetchTableData(tableName);
    return data.find(row => pkFields.every((pk, i) => row[pk].toString() === values[i]));
}

// Close the modal
function closeModal() {
    modal.classList.add("modal--hidden");
}

// Event listeners
document.getElementById("insert").addEventListener("click", (e) => {
    e.preventDefault();
    const tableName = getActiveTableName();
    renderInsertModal(tableName, tables[tableName]);
});

document.getElementById("update").addEventListener("click", (e) => {
    e.preventDefault();
    if (!document.querySelector(".head__right").classList.contains("head__right--disabled")) {
        const tableName = getActiveTableName();
        renderUpdateModal(tableName, tables[tableName]);
    }
});

document.getElementById("delete").addEventListener("click", (e) => {
    e.preventDefault();
    if (!document.querySelector(".head__right").classList.contains("head__right--disabled")) {
        const { pkFields, values } = getPksFromSelectedRow();
        deleteFromDatabase(pkFields, values);
    }
});

document.querySelector(".modal__close").addEventListener("click", closeModal);

// Initialize the application
renderIndex();
