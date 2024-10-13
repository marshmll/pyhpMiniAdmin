const modal = document.querySelector(".modal");
const modalContainer = document.querySelector(".modal__container");
const modalForm = document.querySelector(".modal__form");
let tables = [];

// Fetches and renders the list of tables and the first table's data view.
async function renderIndex() {
    try {
        tables = await fetchTables();
        renderTableList(tables);
        renderTableView(Object.keys(tables)[0], Object.values(tables)[0]);
    } catch (err) {
        console.error("Error fetching tables:", err);
    }
}

// Fetches table descriptions from the backend.
async function fetchTables() {
    try {
        const response = await fetch("http://localhost:3000/php/describe_tables.php");
        return await response.json();
    } catch (err) {
        throw new Error("Failed to fetch table descriptions");
    }
}

// Renders the list of tables.
function renderTableList(tables) {
    const tablesList = document.querySelector(".tables__list");
    tablesList.innerHTML = "";

    Object.keys(tables).forEach(tableName => {
        tablesList.innerHTML += createTableButton(tableName);
    });

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

// Creates a table button.
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

// Sets the active button style and updates the view.
function setActiveTableButton(activeButton) {
    document.querySelectorAll(".tables__button").forEach(button => {
        button.classList.remove("tables__button--active");
    });
    activeButton.classList.add("tables__button--active");
}

// Renders the view of the selected table with its fields and data.
async function renderTableView(tableName, table) {
    document.querySelector(".table-title").textContent = `Tabela ${tableName}`;
    const data = await fetchTableData(tableName);

    if (data) {
        renderTableHead(table);
        renderTableBody(data, table);
    }
}

// Fetches data for the selected table.
async function fetchTableData(tableName) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/${tableName}/`);
        return await response.json();
    } catch (err) {
        console.error(`Error fetching data for ${tableName}:`, err);
        return [];
    }
}

// Renders the table head with columns.
function renderTableHead(table) {
    const tableHead = table.map(field => `
        <th scope="col">
            ${field.Field}<br> ${field.Type.toUpperCase()} ${field.Null == "NO" ? "NOT NULL" : ""} ${field.Key}
        </th>
    `).join("");

    document.querySelector(".table__columns").innerHTML = `<thead><tr>${tableHead}</tr></thead>`;
}

// Renders the table body with rows of data.
function renderTableBody(data, table) {
    const tableRows = data.map(row => {
        return `<tr>${table.map(field => createTableCell(row, field)).join("")}</tr>`;
    }).join("");

    document.querySelector(".table__rows").innerHTML = tableRows;
}

// Creates a table cell for each field in the row.
function createTableCell(row, field) {
    const cellContent = field.Key === "PRI" ? `<th scope="row">${row[field.Field]}</th>` : `<td>${row[field.Field]}</td>`;
    return cellContent;
}

// Renders the insert modal for a table.
function renderInsertModal(tableName, table) {
    modal.classList.remove("modal--hidden");
    modalForm.innerHTML = `<h2 class="modal__title">Inserir em ${tableName}</h2>`;

    modalForm.innerHTML += table.map(field => createModalInput(field)).join("");
    modalForm.innerHTML += `<input class="modal__submit" type="submit" value="Inserir">`;
}

// Creates input fields for the modal based on table schema.
function createModalInput(field) {
    if (field.Field === "id") return '';  // Skip 'id' field

    const inputType = getInputType(field.Type);
    const maxLength = field.Type.includes("varchar") ? field.Type.match(/\d+/)[0] : null;

    return `
        <div class="modal__item">
            <label class="modal__label" for="${field.Field}">${field.Field} ${field.Type}</label>
            <input class="modal__input" type="${inputType}" name="${field.Field}" id="${field.Field}" ${field.Null === "NO" ? "required" : ""} ${maxLength ? `maxlength="${maxLength}"` : ""}>
        </div>
    `;
}

// Determines the input type based on the field type.
function getInputType(fieldType) {
    if (fieldType.includes("int")) return "number";
    if (fieldType.includes("varchar")) return "text";
    if (fieldType === "date") return "date";
    if (fieldType === "datetime") return "datetime-local";
    return "text";
}

// Handles form submission and inserts data into the database.
async function insertIntoDatabase(formData) {
    const jsonBody = Object.fromEntries(formData.entries());
    const tableName = document.querySelector(".tables__button--active").id;

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

// Closes the modal.
function closeModal() {
    modal.classList.add("modal--hidden");
}

// Event listeners
document.getElementById("insert").addEventListener("click", (e) => {
    e.preventDefault();
    const tableName = document.querySelector(".tables__button--active").id;
    renderInsertModal(tableName, tables[tableName]);
});

document.querySelector(".modal__close").addEventListener("click", closeModal);

modalForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    insertIntoDatabase(formData);
});

renderIndex();
