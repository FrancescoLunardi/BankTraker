# Librarys --------------------------------------------------------------------------------------------------------------

# Standard librarys
from flask import Flask, render_template, request, jsonify, session, redirect

# Project librarys
import functions


# Create app and settings -----------------------------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "session"

# Route of PEAGES -------------------------------------------------------------------------------------------------------

# First page (for select "Signin" or "login")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/signin_page")
def signin_page():
    return render_template("signin.html")

@app.route("/dashboard_page")
def dashboard_page():
    if session.get("user_id") != None:
        return render_template("dashboard.html")
    return redirect("/login_page")

# API -------------------------------------------------------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():
    # Get user data
    data = request.json
    user_name = data["name"]
    user_surname = data["surname"]
    user_password = data["password"]
    
    # Debug utput
    print(f"Sys-$ -- Log-in / Data recived: [ name: {user_name}, surname: {user_surname}, password: {user_password} ]")
    
    # Check if the user existe and if the password is correct
    res = functions.check_user_data(user_name, user_surname, user_password)
    
    # Debug output
    print(f"Sys-$ -- Log-in / Res: [ {res} ]")
    
    # Id data is all correct, set the user session
    if res != None:
        session["user_id"] = res
    
    return {"success": True if res != None else False}


@app.route("/signin", methods=["POST"])
def signin():
    # Get user data
    data = request.json
    user_name = data["name"]
    user_surname = data["surname"]
    user_password = data["password"]
    
    # Debug output
    print(f"Sys-$ -- Sign-in / Data recived: [ name: {user_name}, surname: {user_surname}, password: {user_password} ]")
    
    # Add the user (incluse checking of data)
    res = functions.add_user(user_name, user_surname, user_password)
    
    # Debug output
    print(f"Sys-$ -- Sign-in / Res: [ {res} ]")
    
    return {"res": res}


@app.route("/api/get_user_name_surname")
def api_get_user_name_surname():
    return jsonify(
        {"name_surname": functions.get_user_name_surname(id=session.get("user_id"))}
    )

@app.route("/api/get_balance")
def api_get_balance():
    return jsonify(
        {"balance": functions.get_user_balance(id=session.get("user_id"))}
    )

    
@app.route("/api/recharge", methods=["POST"])
def api_recharge():
    # Get omount to recharge
    data = request.json
    amount = float(data["amount"])
    
    # Take the user id
    user = session.get("user_id")
    
    # Debug output
    print(f"Sys-$ -- Dashboard / Recharge: User_id [ {user} ], Amount: [ {amount} ]")
    
    # Recharge 
    res = functions.recharge(user, amount)
    
    # Debug output
    print(f"Sys-$ -- Dashboard / User_id: [ {user} ] // Res: [ {res} ]")
    
    return jsonify({"res": res})


@app.route("/api/withdraw", methods=["POST"])
def api_withdraw():
    # Get amount to withdrawed
    data = request.json
    amount = float(data["amount"])
    
    # Take the suer id
    user = session.get("user_id")
    
    # Debug output
    print(f"Sys-$ -- Dashboard / Withdraw: User_id [ {user} ], Amount: [ {amount} ]")
    
    # Withdraw
    res = functions.withdraw(user, amount)
    
    # Debug output
    print(f"Sys-$ -- Dashboard / User_id: [ {user} ] // Res: [ {res} ]")

    return jsonify({"res": res})


# Run
# host="0.0.0.0", port=5000, 
app.run(host="0.0.0.0", port=5000, debug=True)