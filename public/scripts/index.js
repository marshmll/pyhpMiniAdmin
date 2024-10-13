const modal = document.querySelector(".modal");
const modalContainer = document.querySelector(".modal__container");
const modalForm = document.querySelector(".modal__form");

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
        tableHead += `<th scope="col">${field.Field}<br> ${field.Type.toUpperCase()} ${field.Null == "NO" ? "NOT NULL" : ""} ${field.Key}</th>`;
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

function renderInsertModal(tableName, table) {
    modal.classList.remove("modal--hidden");
    modalForm.innerHTML = `<h2 class="modal__title">Inserir em ${tableName}</h2>`;

    table.forEach(field => {
        let maxLength = null;
        let inputType;

        if (field.Type == "int")
            inputType = "number";
        else if (field.Type.includes("varchar")) {
            inputType = "text";
            maxLength = field.Type.replace("varchar", "");
            maxLength = maxLength.replace("(", "");
            maxLength = maxLength.replace(")", "");
        }
        else if (field.Type == "date")
            inputType = "date";
        else if (field.Type == "datetime")
            inputType = "datetime-local";

        if (field.Field != "id") {
            modalForm.innerHTML += `
                <div class="modal__item">
                    <label class="modal__label" for="${field.Field}">${field.Field} ${field.Type}</label>
                    <input class="modal__input" type="${inputType}" name="${field.Field}" id="${field.Field}" ${field.Null == "NO" ? "required" : ""} ${maxLength ? `maxlength="${maxLength}"` : ""}>
                </div>
            `;
        }
    });

    modalForm.innerHTML += `<input class="modal__submit" type="submit" value="Inserir">`;

}

async function insertIntoDatabase(formData) {
    const jsonBody = Object.fromEntries(formData.entries());

    const tableName = document.querySelector(".tables__button--active").id;

    const res = await fetch(`http://127.0.0.1:8000/${tableName}/`,
        {
            method: "POST",
            headers: new Headers({
                "Content-Type": "application/json",
            }),
            body: JSON.stringify(jsonBody)
        })
        .then(async res => {
            const json = await res.json();

            if (res.status != 200) {
                alert("Ocorreu um erro na inserção do registro: " + json.detail);
                return;
            }

            modal.classList.add("modal--hidden");
            renderTableView(tableName, tables[tableName]);
        })
        .catch(err => console.error(err));
}

document.getElementById("insert").addEventListener("click", (e) => {
    e.preventDefault();

    let tableName = document.querySelector(".tables__button--active").id;

    renderInsertModal(tableName, tables[tableName]);
});

document.querySelector(".modal__close").addEventListener("click", () => {
    modal.classList.add("modal--hidden");
})

modalForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    insertIntoDatabase(formData);
})

renderIndex();