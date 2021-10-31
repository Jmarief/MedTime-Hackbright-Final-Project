"""Models for MedTime Tracker and Reminder app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta

db = SQLAlchemy()

class User(db.Model):
    """Create a user object for each user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def check_password(self, input_password):
        return check_password(self.password, input_password)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Medications(db.Model):
    """Create a list of medications the user will input"""

    __tablename__ = "medications"

    medication_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instructions = db.Column(db.String(200), nullable=True)
    medication_allergies = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Medications medication_id={self.medication_id}, instructions={self.instructions}, medication_allergies={self.medication_allergies}>"


class User_Medications(db.Model):
    """Create user medications for medications, dosage and frequency"""

    __tablename__ = "user_medications"

    user_medications_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.medication_id'))
    dosage = db.Column(db.Integer, nullable=False)
    frequency_per_day = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', backref='user_medications')
    medications = db.relationship('Medications', backref='user_medications')
    
    def __repr__(self):
        return f"<User_Medications user_medications_id={self.user_medication_id}, dosage={self.dosage}, frequency_per_day={self.frequency_per_day}>"


class Reminders(db.Model):
    """Various reminders for medications and refills"""

    __tablename__ = "reminders"

    reminders_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_medications_id = db.Column(db.Integer, db.ForeignKey('user_medications.user_medications_id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.medication_id'))
    scheduled_date = db.Column(db.DateTime)
    scheduled_time = db.Column(db.DateTime(timezone=True))
    intake_alarm = db.Column(db.DateTime)
    refills = db.Column(db.Integer, nullable=True)

    user_medications = db.relationship('User_Medications', backref='reminders')
    medications = db.relationship('Medications', backref='reminders')

    def __repr__(self):
        return f"<Reminders reminders_id{self.reminders_id} dosage={self.dosage} frequency_per_day={self.frequency_per_day} scheduled_date={self.scheduled_date} scheduled_time={self.scheduled_time} refills={self.refills}>"


"""NEED TO DO - Pharmacy Information Table"""

def connect_to_db(flask_app, db_uri='postgresql:///medtime', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

if __name__ == '__main__':
    from server import app
    connect_to_db(app)