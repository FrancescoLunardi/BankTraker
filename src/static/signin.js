async function signin() {
    let name = document.getElementById("name").value;
    let surname = document.getElementById("surname").value;
    let password = document.getElementById("password").value;

    if (name == "" || surname == "" || password == "") {
        alert("Error! Enter data...");
        return;
    }

    const res = await fetch("signin", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "name": name, 
            "surname": surname, 
            "password": password
        })
    });
    
    const result = await res.json();
    console.log("Data recived: ", result.res);

    if (result.res == "succes") {
        window.location.href = "/login_page"
    } else {
        alert("Error! " + result.res)
    }
}