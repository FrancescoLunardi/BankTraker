async function login() {
    let name = document.getElementById("name").value;
    let surname = document.getElementById("surname").value;
    let password = document.getElementById("password").value;

    if (name == "" || surname == "" || password == "") {
        alert("Error! Enter data...");
        return;
    }
    
    const res = await fetch("login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "name": name, 
            "surname": surname, 
            "password": password
        })
    });
    
    const result = await res.json();
    console.log("Data recived: ", result);

    if (result.success) {
        window.location.href = "/dashboard_page";
    } else {
        alert("Unvalid data");
    }
}