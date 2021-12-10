"""Server for MedTime app"""

from datetime import datetime
from datetime import timedelta

from flask import Flask, render_template, redirect, flash, session, request
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Medications, User_Medications, Reminders

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """Homepage"""

    medications = User_Medications.query.filter_by(user_id=1).all()

    if "current_user" in session:
        current_user = session["current_user"]
        return render_template('homepage.html', current_user="current_user")
    else:
        return render_template('homepage.html', current_user=None, medications=medications)


@app.route("/signup", methods=["GET"])
def signup_form():
    """User sign up form"""

    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_request():
    """New user signup"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")

    new_user = User(fname=fname, lname=lname, email=email,
                    password=password, phone_number=phone_number)
    user = User.query.filter_by(fname=fname, lname=lname, email=email, password=password).first()

    if user is not None:
        flash(f"User {user.fname} {user.lname} has already registered!")
        return redirect("/")

    else:
        db.session.add(new_user)

    db.session.commit()
    flash(f"User {new_user.fname} {new_user.lname} account has been registered!")

    session["new_user_id"] = new_user.user_id

    return redirect("/")


@app.route("/register", methods=["GET"])
def register():
    """User sign up form"""

    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def registration_form():
    """User registration for medications"""

    loggedin_user_id = session.get("user_id")

    if loggedin_user_id:
        user = User.query.filter_by(user_id=loggedin_user_id).first()

        if user:
            flash(f"Welcome {user.fname} you are logged in")
        else:
            flash("You are currently not logged in")

    return redirect("medication_directory")


@app.route("/login")
def login():
    if "new_user_id" in session:
        user_id = session["new_user_id"]
        user_name = User.query.filter_by(user_id=user_id).first().fname
        del session["new_user_id"]

    else:
        user_name = "User"

    return render_template("login.html", user=user_name)


@app.route("/login", methods=["POST"])
def user_login():
    """User login"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User email address is not registered")

        return redirect("/")

    elif user.password != password:
        flash("Incorrect password, please try again")

        return redirect("/")
    print(user.user_id)
    session["user_id"] = user.user_id
    flash("Welcome, you have logged in successfully")
    return redirect("/medication_directory")


@app.route('/logout', methods=['GET'])
def logout():
    """User log out"""

    session.clear()
    flash("You have been logged out")

    return redirect("/")


@app.route("/medications", methods=["POST"])
def submission():
    """User medications"""

    user_id = session["user_id"]

    medications_id = request.form.get("medications_id")
    user_medications_id = request.form.get("user_medications_id")
    dosage = request.form.get("dosage")
    frequency_per_day = request.form.get("frequency_per_day")

    new_medication = Medications(user_id=user_id, medications_id=medications_id,
                                 user_medications_id=user_medications_id, dosage=dosage,
                                 frequency_per_day=frequency_per_day)

    db.session.add(new_medication)
    db.session.commit()

    for new_time in frequency_per_day:
        scheduled_time = datetime.strptime(new_time, "%H:%M:%S")
        new_frequency = Reminders(
            user=user_id, scheduled_time=scheduled_time, new_medications=new_medication.medications.id
        )
        db.session.add(new_frequency)
        db.session.commit()

    flash("Medication has been added")
    return redirect("medication_directory")


@app.route("/medication_directory", methods=["GET"])
def user_meds():
    """User medications that they are currently taking"""

    user_id = session["user_id"]

    all_meds = User_Medications.query.filter_by(user_id=user_id).all()
    user = User.query.filter_by(user_id=user_id).first()

    medications_dict = dict()

    for medication in user.user_medications:
        medications_dict[medication.medication.medication_id] = medication.reminders

    return render_template("medication_directory.html", user=user, medications=medications_dict)


def reminders(user_id):
    """User reminders for taking medications"""

    current_date = datetime.now()
    med_hour = current_date + timedelta(hours=1)
    med_hour = med_hour.time()
    current_date = current_date.time()

    for medications in medication_plan:
        user_medications = Reminders.query.filter_by(
            medications_id=medications.medications_id).all()
        if current_date <= reminders.timestamp and reminders.timestamp <= med_hour:
            message = "REMINDER {first_name}: it's time to take {user_medication_id}."
            flash(message)
            return message


if __name__ == '__main__':
    connect_to_db(app)

    app.run(host='0.0.0.0', debug=True)