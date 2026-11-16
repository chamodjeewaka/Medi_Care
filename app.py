from functools import wraps
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.secret_key = "my_clinic_secret_key_123"

db = SQL("sqlite:///data.db")


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def loginn_user():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?",username)

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            flash("Invalid username or password", "error")
            return redirect("/login")

        session.clear()

        # Save logged-in user's ID
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/home")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET","POST"])
def register_user():

    if request.method == "POST":

        #Form inputs
        name = request.form.get("name")
        age = request.form.get("age")
        height = request.form.get("height")
        weight = request.form.get("weight")
        email = request.form.get("email")
        phone = request.form.get("phone")
        user_name = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        # Check username and email
        errors = []

        if db.execute("SELECT username FROM users WHERE username = ?",user_name):
            errors.append("Username already exists")

        if db.execute(
            "SELECT email FROM patients WHERE email = ?",email):
            errors.append("Email already exists")

        if errors:
            for error in errors:
                flash(error, "error")

            return redirect("/register")

        #Checking the password
        if password != repassword:
            flash("Passwords do not match", "error")
            return redirect("/register")
        # Hash password
        password_hash = generate_password_hash(password)

        #Insert to database
        db.execute("INSERT INTO patients(name,age,height,weight,email,phone_number) VALUES (?,?,?,?,?,?)",name,age,height,weight,email,phone)
        patient_id = db.execute("SELECT id FROM patients")[::-1][0]["id"]
        db.execute("INSERT INTO users(username,password,patient_id) VALUES (?,?,?)",user_name,password_hash,patient_id)
        flash("Successfully Registered!", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/home")
def home():
    #Checking user already logged
    if "user_id" not in session:
            flash("Please login first", "error")
            return redirect("/login")

    username = session['username']
    patient_details = db.execute("SELECT * FROM patients WHERE id = (SELECT patient_id FROM users WHERE username = ?)",username)
    return render_template("home.html",patient_details=patient_details)



@app.route("/home/doctors")
def doctors():

    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect("/login")

    doctors = db.execute("SELECT * FROM doctors ORDER BY name ASC")

    return render_template("view_doctors.html",doctors=doctors)



@app.route("/login_doctor",methods=["GET","POST"])
def doctor_login():
    if request.method == "POST":

            username = request.form.get("username")
            password = request.form.get("password")

            rows = db.execute("SELECT * FROM users WHERE username = ? AND doctor_id IS NOT NULL",username)

            if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
                flash("Invalid username or password", "error")
                return redirect("/login_doctor")

            session.clear()

            # Save logged-in user's ID
            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["username"]
            session["doctor_id"] = rows[0]["doctor_id"]

            return redirect("/doctor_dashboard")
    return render_template("doctor_login.html")



@app.route("/doctor_dashboard")
def doctor_dashboard():

    if "user_id" not in session:
            flash("Please login first", "error")
            return redirect("/login_doctor")

    doctor_id = session.get("doctor_id")
    doctor = db.execute("SELECT * FROM doctors WHERE id = ?", doctor_id)
    print(doctor_id)
    if len(doctor) != 1:
        session.clear()
        flash("Doctor account not found", "error")
        return redirect("/login_doctor")

    return render_template("doctor_dash.html",doctor=doctor[0])


from datetime import datetime
from zoneinfo import ZoneInfo

@app.route("/patient_consult", methods=["GET", "POST"])
def patient_consult():

    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect("/login_doctor")

    # Display the form
    if request.method == "GET":
        return render_template("patient_consult.html")

    # Get form data
    description = request.form.get("description")
    doctor_id = session.get("doctor_id")
    patient_id = request.form.get("patient_id")

    medicines = request.form.getlist("medicine[]")
    dosages = request.form.getlist("dosage[]")
    frequencies = request.form.getlist("frequency[]")
    durations = request.form.getlist("duration[]")
    quantities = request.form.getlist("quantity[]")

    # Check whether medicine fields have matching lengths
    if not (len(medicines) == len(dosages) == len(frequencies) == len(durations) == len(quantities)):
        flash("Invalid medicine details", "error")
        return redirect("/patient_consult")

    # Get current date and time
    now = datetime.now(ZoneInfo("Asia/Colombo"))
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # 1. Create checking record and get its ID
    checking_id = db.execute("""
        INSERT INTO checkings
        (doctor_id, patient_id, description, date, time)
        VALUES (?, ?, ?, ?, ?)
    """, doctor_id, patient_id, description, date, time)

    # 2. Insert all medicines using the same checking_id
    for medicine, dosage, frequency, duration, quantity in zip(
        medicines, dosages, frequencies, durations, quantities
    ):
        db.execute("""
            INSERT INTO prescriptions
            (checking_id, medicine, dosage, frequency, duration, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, checking_id, medicine, dosage, frequency, duration, quantity)


    return redirect("/doctor_dashboard")



@app.route("/patient_search", methods=["POST"])
def patient_search():

    data = request.get_json()

    identifier = data.get("identifier")

    patient = db.execute("""
        SELECT * FROM patients
        WHERE email = ? OR phone_number = ?
    """, identifier, identifier)

    if len(patient) != 1:
        return {
            "success": False,
            "message": "Patient not found"
        }, 404

    patient = patient[0]

    return {
        "success": True,
        "patient": {
            "id": patient["id"],
            "name": patient["name"],
            "email": patient["email"],
            "phone": patient["phone_number"],
            "age": patient["age"],
            "height": patient["height"],
            "weight": patient["weight"]
        }
    }




@app.route("/doctor_patient_history")
def doctor_patient_history():

    if "user_id" not in session or not session.get("doctor_id"):
        flash("Please login as a doctor first", "error")
        return redirect("/login_doctor")

    doctor_id = session.get("doctor_id")

    # Get logged-in doctor's name
    doctors = db.execute("""
        SELECT *
        FROM doctors
        WHERE id = ?
    """, doctor_id)

    if len(doctors) != 1:
        flash("Doctor not found", "error")
        return redirect("/login_doctor")

    doctor = doctors[0]

    # Get patients consulted by this doctor
    patients = db.execute("""
        SELECT
            patients.id,
            patients.name,
            patients.age,
            patients.height,
            patients.weight,
            patients.email,
            patients.phone_number,
            MAX(checkings.date) AS last_consultation
        FROM patients
        JOIN checkings
            ON patients.id = checkings.patient_id
        WHERE checkings.doctor_id = ?
        GROUP BY patients.id
        ORDER BY MAX(checkings.date) DESC
    """, doctor_id)

    return render_template(
        "doctor_patient_history.html",
        doctor=doctor,
        patients=patients
    )



@app.route("/patient_history/<int:patient_id>")
def patient_history(patient_id):

    # Check whether user is logged in
    if "user_id" not in session:
        flash("Please login first", "error")
        return redirect("/login")

    # Identify whether logged-in user is a doctor or patient
    doctor_id = session.get("doctor_id")

    if doctor_id:

        # Doctor can view patients consulted by that doctor
        access = db.execute("""
            SELECT id
            FROM checkings
            WHERE patient_id = ? AND doctor_id = ?
        """, patient_id, doctor_id)

        if not access:
            flash("You are not authorized to view this history", "error")
            return redirect("/doctor_dashboard")

    else:

        # Get logged-in patient's ID from users table
        users = db.execute("""
            SELECT patient_id
            FROM users
            WHERE id = ?
        """, session["user_id"])

        if len(users) != 1 or users[0]["patient_id"] != patient_id:
            flash("You are not authorized to view this history", "error")
            return redirect("/home")

    # Get patient details
    patients = db.execute("""
        SELECT *
        FROM patients
        WHERE id = ?
    """, patient_id)

    if len(patients) != 1:
        flash("Patient not found", "error")

        if doctor_id:
            return redirect("/doctor_dashboard")

        return redirect("/home")

    patient = patients[0]

    # Get consultation history
    checkings = db.execute("""
        SELECT
            checkings.id,
            checkings.date,
            checkings.time,
            checkings.description,
            doctors.name AS doctor_name,
            doctors.specialized_area,
            doctors.slmcno,
            doctors.phone_number AS doctor_phone,
            doctors.email AS doctor_email
        FROM checkings
        JOIN doctors ON checkings.doctor_id = doctors.id
        WHERE checkings.patient_id = ?
        ORDER BY checkings.date DESC, checkings.time DESC
    """, patient_id)

    # Get prescriptions for each consultation
    for checking in checkings:

        checking["medicines"] = db.execute("""
            SELECT
                medicine,
                dosage,
                frequency,
                duration,
                quantity
            FROM prescriptions
            WHERE checking_id = ?
        """, checking["id"])

    return render_template("past_history.html",patient=patient,checkings=checkings,is_doctor=bool(doctor_id))
