import { jsonToHTMLTable } from "./jsonToHTMLTable.js";

CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "text/x-mysql",
    lineNumbers: true,
    theme: "default",
});

async function checkAuthentication() {
    const res = await fetch("http://localhost:3000/php/check_auth.php");

    if (res.status === 401)
        window.location.replace("http://localhost:3000/login.html");
}

const form = document.querySelector(".form");
const output = document.querySelector(".output");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const body = Object.fromEntries(formData.entries());

    if (body.query.length === 0) return;

    let res = await fetch("http://localhost:3000/php/query.php", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            accept: "application:json",
        },
        body: JSON.stringify(body),
    }).then(res => res.json());

    output.innerHTML = jsonToHTMLTable(res);
});

checkAuthentication();