"""Models for MedTime Tracker and Reminder app"""

from flask_sqlalchemy import SQLAlcemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """Create a user object for each user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def check_password(self, input_password):
        return check_password(self.password, input_password)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>'"


class Medications(db.Model):
    """Create a list of medications the user will input"""

    __tablename__ = "medications"

    medication_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instructions = db.Column(db.String(200), nullable=True)
    medication_allergies = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Medications medication_id={self.medication_id} instructions={self.instructions} medication_allergies={self.medication_allergies}"

class User_Medications(db.Model):
    """Create user medications for medications, dosage and frequency"""

    __tablename__ = "user_medications"

    


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()