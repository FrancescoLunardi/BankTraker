# Library -------------------------------------------------------------------------------------------------------

# Standart librarys
import re, datetime

# Project Lybrarys
import database

# FUNCTIONS -----------------------------------------------------------------------------------------------------

# If the user data are correct return the user id
def check_user_data(name, surname, password):
    conn = database.get_conn()
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT id FROM users WHERE name == "{name}" AND surname == "{surname}" AND password == "{password}";
    """)
    
    ris = cur.fetchone()
    conn.close()
    
    return int(ris[0]) if ris != None else None

# Get a new id for a new user
def get_new_id():
    conn = database.get_conn()
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT MAX(id) FROM users
    """)
    
    row = cur.fetchone()
    
    # If there aren't users start from id 0
    return row[0] + 1 if row != None else 0

# Get a string with name and surname by id
def get_user_name_surname(id):
    conn = database.get_conn()
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT name, surname FROM users where id = {id}
    """)
    
    res = cur.fetchone()
    
    return res[0] + " " + res[1]


def get_user_balance(id):
    conn = database.get_conn()
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT balance FROM users where id = {id}
    """)
    
    return cur.fetchone()[0]

# Check if the password respect the rules
def check_password(password):
    if len(password) < 8:
        return "Error: The password is too short!"
    if (not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password)):
        return "Error: The pasword uncontain letters and numbers!"
    
    return "succes"
    

def add_user(name, surname, password):
    conn = database.get_conn()
    cur = conn.cursor()
    
    # Check if already existe a user with the same name and surname
    cur.execute(f"""
        SELECT * FROM users WHERE name == "{name}" AND surname == "{surname}"
    """)
    
    if cur.fetchone()[0] != None:
        return "e: there is already a user with the same name and surname"
    
    # Check if password is valid
    pass_check = check_password(password)
    if pass_check != "succes":
        return pass_check
    
    # Add the new user on database
    cur.execute(f"""
        INSERT INTO users VALUES ({get_new_id()}, "{name}", "{surname}", "{password}", 0)
    """)
    conn.commit()
    conn.close()
    
    return "succes"

# Get a new id for chronology item
def new_chronology_id(user_id):
    conn = database.get_conn()
    cur = conn.cursor()
    
    cur.execute(f"""
        SELECT MAX(id) FROM chronology WHERE user_id = {user_id} 
    """)
    last_id = cur.fetchone()[0]
    
    # If there aren't other items start from 0
    return (last_id + 1) if last_id != None else 0
    
    
def recharge(user_id, amount):
    conn = database.get_conn()
    cur = conn.cursor()
    
    # Get total balance
    cur.execute(f"""
        SELECT balance FROM users WHERE id = {user_id}
    """)
    balance = cur.fetchone()[0]
    
    # Add the new item on chronology
    cur.execute(f"""
        INSERT INTO chronology VALUES (
            {user_id}, {new_chronology_id(user_id)}, {amount}, {balance + amount}, "recharge", "{datetime.datetime.now(None)}"
        );
    """)
    
    # Update the user balance
    cur.execute(f"""    
        UPDATE users SET balance = {balance + amount} WHERE id = {user_id}
    """)
    
    conn.commit()
    
    return f"{amount}€ added!"
    
def withdraw(user_id, amount):
    conn = database.get_conn()
    cur = conn.cursor()
    
    # Get total balance
    cur.execute(f"""
        SELECT balance FROM users WHERE id = {user_id}
    """)
    balance = cur.fetchone()[0]
    
    # Check if the amount is greater than total balance
    if amount > balance:
        return "e: amount is biggest than total balance"
    
    # Add the new item on chronology
    cur.execute(f"""
        INSERT INTO chronology VALUES (
            {user_id}, {new_chronology_id(user_id)}, {amount}, {balance - amount}, "withdraw", "{datetime.datetime.now(None)}"
        )
    """)
    
    # Update the user balance
    cur.execute(f"""    
        UPDATE users SET balance = {balance - amount} WHERE id = {user_id}
    """)
    
    conn.commit()
    
    return "succes"