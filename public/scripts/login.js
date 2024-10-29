const form = document.querySelector(".form");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formURLEncoded = new URLSearchParams(formData).toString();

    let res = await fetch("http://localhost:3000/php/login.php", {
        method: "POST",
        headers: {
            accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formURLEncoded
    }).then(async res => {
        let json = await res.json();

        if (res.status === 200)
            window.location.pathname = "/";
        else
            alert(`Erro: ${json.detail}`);
    });

    console.log(res);
});