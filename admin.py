from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

db = SQL("sqlite:///data.db")

def add_doctors():
    doctor_accounts = [
        {
            "id": 1,
            "username": "brucewayne",
            "password": "123456789"
        },
        {
            "id": 5,
            "username": "kaveeshanethmini",
            "password": "123456789"
        }

    ]

    for doctor in doctor_accounts:

        password_hash = generate_password_hash(doctor["password"])

        db.execute("INSERT INTO users(username,password,doctor_id) VALUES (?,?,?)",doctor["username"],password_hash,doctor["id"])

add_doctors()
