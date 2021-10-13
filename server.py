"""Server for MedTime app"""

from flask import Flask
render_template
redirect
flash
session
request
from model import db, connect_to_db
from datetime import datetime 
from datetime import timedelta

import model


@app.route("/") 
def homepage():
    """Homepage"""

    return render_template("homepage.html")

@app.route("/register")
def register():
    """Registration form"""

    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def registration_form():
    """New user registration"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone_number")

    new_user = User(fname=fname, lname=lname, email=email, password=password, phone_number=phone_number)
    user = User.query.filter_by(fname=fname, lname=lname, email=email, password=password).first()

    if user is not None:
        flash(f"User {user.fname} {user.lname} has already registered!")

        else:
            db.session.add(new_user)

        db.session.commit()
        flash(f"User {new_user.fname} {new_user.lname} account has been registered!")

        session["new_user_id"] = new_user.user_id

        return redirect("/")


@app.route("/login", methods=["POST"])
def user_login():
    """User login"""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User email address is not registered")

        return redirect("/register")

    elif user.password != password:
        flash("Incorrect password, please try again")

        return redirect("/login")

    session["user_id"] = user.user_id
    flash("Welcome, you have logged in successfully")
    return redirect("/users", user_id=user.user_id)


@app.route("/medications", methods["POST"])
def submission():
    """User medications"""

    user = session["user_id"]

    medications_id = request.form.get("medications_id")
    user_medications_id = request.form.get("user_medications_id")
    dosage = request.form.get("dosage")
    frequency_per_day = request.form.get("frequency_per_day")

    new_medication = Medications(user_id=user, medications_id=medications_id, 
                                user_medications_id=user_medications_id, dosage=dosage, frequency_per_day=frequency_per_day )

    db.session.add(new_medication)
    db.session.commit() 

    for new_time in frequency_per_day:
        scheduled_time = datetime.strptime(new_time, "%H:%M:%S")
        new_frequency = Reminders(user=user_id, scheduled_time=scheduled_time, new_medications=new_medication.medications.id)

        db.session.add(new_frequency)
        db.session.commit()
    
    flash("Medication has been added")
    return redirecr("/")

//NEED TO FIX - Complete medication plan
@app.route("/medication_plan", methods=["GET"])
def user_meds():
"""User medications that they are currently taking"""


def reminders(user_id)
"""User reminders for taking medications"""

    current_date = datetime.now()
    med_hour = current_date + timedelta(hours=1)
    med_hour = med_hour.time()
    current_date = current_date.time()

    for medications in medication_plan:
        user_medications = Reminders.query.filter_by(medications_id=medications.medications_id).all()
            if current_date <= reminders.timestamp and reminders.timestamp <= med_hour:
                message = "REMINDER {first_name": time to take {user_medication_id}."
                flash(message)
                return message




if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)