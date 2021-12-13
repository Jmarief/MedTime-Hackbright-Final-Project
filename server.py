"""Server for MedTime app"""

from datetime import datetime
from datetime import timedelta

from flask import Flask, render_template, redirect, flash, session, request
from flask_toastr import Toastr
from jinja2 import StrictUndefined

import model
from model import connect_to_db, db, User, Medications, User_Medications, Reminders

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

toastr = Toastr(app)
toastr.init_app(app)


@app.route("/")
def homepage():
    """Homepage"""

    medications = User_Medications.query.filter_by(user_id=1).all()

    if "current_user" in session:
        current_user = session["current_user"]
        return render_template('homepage.html', current_user="current_user")
    else:
        return render_template('homepage.html', current_user=None, medications=medications)


@app.route("/register", methods=["GET"])
def register():
    """User sign up form"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():
    """New user signup"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('password-confirmation')
    phone_number = request.form.get('phone_number')

    if (not fname or not lname or not email or not password or not password_confirmation or not phone_number) or (
            password != password_confirmation):
        flash('Form input was incorrect or incomplete', 'error')
    else:
        new_user = User(fname=fname, lname=lname, email=email,
                        password=password, phone_number=phone_number)
        user = User.query.filter_by(fname=fname, lname=lname, email=email, password=password).first()

        if user is not None:
            flash(f"{user.fname} {user.lname} has already registered! You may login <a href='/login' "
                  f"title='Login'>here</a>.", 'error')

            return redirect("/")

        else:
            db.session.add(new_user)

        db.session.commit()
        flash(f"Account has been registered for {new_user.fname} {new_user.lname}!")

        session['user_id'] = new_user.user_id

    return render_template("register.html")


# @app.route("/register", methods=["GET"])
# def register():
#    """User sign up form"""

#    return render_template("registration.html")


# @app.route("/register", methods=["POST"])
# def registration_form():
#    """User registration for medications"""

#    loggedin_user_id = session.get("user_id")

#    if loggedin_user_id:
#        user = User.query.filter_by(user_id=loggedin_user_id).first()

#        if user:
#            flash(f"Welcome {user.fname} you are logged in")
#        else:
#            flash("You are currently not logged in")

#    return redirect("medication_directory")

# region Medication Actions
@app.route('/create-medication', methods=['POST'])
def create_medication():
    user_id = session['user_id']
    medication_name = request.form.get('medication_name')
    instructions = request.form.get('instructions')
    medication_allergies = request.form.get('medication_allergies')

    new_med = Medications(medication_name=medication_name, instructions=instructions,
                          medication_allergies=medication_allergies)

    db.session.add(new_med)
    db.session.commit()

    return redirect('/my-meds')


# endregion

# region User_Medication Actions
@app.route('/create-user-medication', methods=["POST"])
def create_user_medication():
    user_id = session['user_id']
    medication_id = request.form.get('medication_id')
    dosage = request.form.get('dosage')
    uom = request.form.get('uom')
    frequency_per_day = request.form.get('frequency_per_day')

    new_med = User_Medications(user_id=user_id, medication_id=medication_id,
                               dosage=dosage, uom=uom, frequency_per_day=frequency_per_day)

    db.session.add(new_med)
    db.session.commit()

    return redirect('/my-meds')


# endregion

@app.route('/update-user-medication', methods=["POST"])
def update_user_medication():
    user_id = session['user_id']
    user_medications_id = request.form.get('user_medications_id')
    medication_id = request.form.get('medication_id')
    dosage = request.form.get('dosage')
    uom = request.form.get('dosage_uom')
    frequency_per_day = request.form.get('frequency_per_day')

    user_medication = User_Medications.query.filter_by(user_medications_id=user_medications_id).first()

    user_medication.medication_id = medication_id
    user_medication.dosage = dosage
    user_medication.uom = uom
    user_medication.frequency_per_day = frequency_per_day

    db.session.commit()

    return redirect('/my-meds')


@app.route('/delete_user_medication', methods=["POST"])
def delete_user_medication():
    user_medications_id = request.form.get('user_medications_id')

    if user_medications_id is not None:
        User_Medications.query.filter_by(user_medications_id=user_medications_id).delete()
        db.session.commit()

        return redirect('/')


# endregion


@app.route('/my-meds', methods=["GET"])
def my_meds():
    if 'user_id' in session:
        user_id = session['user_id']

        user_medications = User_Medications.query.join(Medications).filter(User_Medications.user_id == user_id)
        all_meds = Medications.query.order_by('medication_name')

        return render_template("my-meds.html", user_medications=user_medications, all_meds=all_meds, UoMs=model.UoM)
    else:
        return redirect('/')


@app.route('/manage-profile', methods=["GET"])
def manage():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(user_id=user_id).first()

        return render_template("profile.html", user=user)
    else:
        return redirect('/')


@app.route('/manage-profile', methods=['POST'])
def update_profile():
    if 'user_id' in session:
        if (not request.form['fname'] or not request.form['lname'] or not request.form['email'] or not request.form[
            'password'] or not request.form['password-confirmation'] or not request.form['phone_number']) or (
                request.form['password'] != request.form['password-confirmation']):
            flash('Form input was incorrect or incomplete', 'error')
            return render_template('profile.html', user=request.form)
        else:
            user_id = session['user_id']
            user = User.query.filter_by(user_id=user_id).first()

            user.fname = request.form['fname']
            user.lname = request.form['lname']
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
            user.password = request.form['password']

            db.session.commit()

            flash('Your profile was successfully updated', 'success')
            return render_template('profile.html', user=user)
    else:
        return redirect('/')


@app.route("/login")
def login():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = User.query.filter_by(user_id=user_id).first().fname
        del session['user_id']

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
        flash('User email address is not registered', 'error')
        return redirect("/login")

    elif user.password != password:
        flash('Incorrect password, please try again', 'error')
        return redirect("/login")

    print(user.user_id)
    session["user_id"] = user.user_id

    flash("Welcome, you have logged in successfully")

    return render_template('homepage.html')


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
