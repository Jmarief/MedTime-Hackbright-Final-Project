"""Crud Operations"""

from model import db, User, Medications, User_Medications, Reminders, connect_to_db

"""Database Functions"""

def create_user(fname, lname, email, phone_number, password):
    """Create a new user and return user"""

    user = User(fname=fname, lname=lname, phone_number=phone_number, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Find user by email"""

    return User.query.filter_by(email=email).all()

def login_user(email, password):
    """Return a user by email and password"""

    return User.guery.filter(user.email==email, User.password==password).first()


def create_medications(instructions, medication_allergies):
    """create and return medications"""

    medications = Medications(instructions=instructions, medication_allergies=medication_allergies)

    db.session.add(medications)
    db.session.commit()

    return medications


def create_user_medications(user_id, medication_id, dosage, frequency_per_day):
    """create and return user medications"""

    user_medications = User_Medications(user_id=user_id, medication_id=medication_id, 
                                        dosage=dosage, frequency_per_day=frequency_per_day)

    db.session.add(user_medications)
    db.session.commit()

    return user_medications


def create_reminders(user_medications_id, medication_id, dosage, scheduled_date, scheduled_time,
                     intake_alarm, refills):
    """Create and return reminders"""

    reminder = Reminders(user_medications_id=user_medications_id, medication_id=medication_id,
                         dosage=dosage, scheduled_date=scheduled_date, scheduled_time=scheduled_time,
                         intake_alarm=intake_alarm, refills=refills)

    db.session.add(reminder)
    db.session.commit()
    
    return reminder                

if __name__ == '__main__':
    from server import app
    connect_to_db(app)