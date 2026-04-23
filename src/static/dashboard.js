// Get and show the total balance

async function get_balance() {
    const res = await fetch("/api/get_balance");
    const data = await res.json();

    return data.balance;
}

async function show_balance() {
    const balance = await get_balance();
    document.getElementById("balance-text").innerText = balance + "€";
}


// Get and show teh name and surname of user

async function get_user_name_surname() {
    const res = await fetch("/api/get_user_name_surname");
    const data = await res.json();

    return data.name_surname;
}

async function show_name() {
    const name_surname = await get_user_name_surname();
    document.getElementById("user-name-surname").innerText = name_surname;
}

// Show data

window.onload = async function() {
    await show_name();
    await show_balance();

    setInterval(show_balance, 1000);
}




async function recharge() {
    const amount_tag = document.getElementById("recharge-amount");
    const amount = amount_tag.value;
    amount_tag.value = "";

    console.log(amount);

    if (amount <= 0) {
        alert("Error: the value isn't valid!");
    }

    const res = await fetch("/api/recharge", { 
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "amount": amount.toString()
        })
    });

    const result = await res.json();
}

async function withdraw() {
    const amount_tag = document.getElementById("withdraw-amount");
    const amount = amount_tag.value;
    amount_tag.value = "";

    console.log(amount);

    if (amount <= 0) {
        alert("Error: the value isn't valid!");
    }

    const res = await fetch("/api/withdraw", { 
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            "amount": amount.toString()
        })
    });

    const result = await res.json();
}