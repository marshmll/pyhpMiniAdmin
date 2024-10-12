let tables = [];

async function renderIndex() {
    tables = await fetch("http://localhost:3000/php/describe_tables.php")
        .then(async (res) => await res.json())
        .catch((err) => {
            throw new Error(err);
        })

    renderTableList(tables);
    renderTableView(Object.keys(tables)[0], Object.values(tables)[0]);
}

function renderTableList(tables) {
    const tablesList = document.querySelector(".tables__list");

    Object.keys(tables).forEach(tableName => {
        tablesList.innerHTML += `
        <li class="tables__item">
            <button id="${tableName}" title="${tableName}" class="tables__button">
                <span class="material-symbols-outlined">table</span>
                ${tableName.toUpperCase()}
            </button>
        </li>
        `;
    });

    const allButtons = document.querySelectorAll(".tables__button");

    allButtons[0].classList.add("tables__button--active");

    allButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();

            allButtons.forEach(button => button.classList.remove("tables__button--active"));
            button.classList.add("tables__button--active");
            renderTableView(button.id, tables[button.id]);
            console.log("Executing to " + button.id)
        })
    })
}

async function renderTableView(tableName, table) {
    document.querySelector(".table-title").textContent = `Tabela ${tableName}`;

    const data = await fetch(`http://127.0.0.1:8000/${tableName}/`)
        .then(async res => await res.json())
        .catch(err => { console.error(err) });

    let tableHead = `
        <thead>
            <tr>
    `;

    table.forEach(field => {
        tableHead += `<th scope="col">${field.Field}<br> ${field.Type.toUpperCase()}${field.Null == "NO" ? "*" : ""} ${field.Key}</th>`;
    })

    tableHead += `
            </tr>
        </thead>
    `;

    document.querySelector(".table__columns").innerHTML = tableHead;

    document.querySelector(".table__rows").innerHTML = "";

    if (data.length != 0) {
        let tableRows = "";

        console.log(data)

        data.forEach(row => {
            tableRows += "<tr>";

            table.forEach(field => {
                if (field.Key == "PRI")
                    tableRows += `<th scope="row">${row[field.Field]}</th>`;
                else
                    tableRows += `<td>${row[field.Field]}</td>`;
            });

            tableRows += "<tr>";

        });

        document.querySelector(".table__rows").innerHTML = tableRows;
    }
}

renderIndex();