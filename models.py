from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="Student")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class StudentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    g1 = db.Column(db.Float)
    g2 = db.Column(db.Float)
    studytime = db.Column(db.Integer)
    failures = db.Column(db.Integer)
    absences = db.Column(db.Integer)
    predicted_grade = db.Column(db.Float)
    risk_level = db.Column(db.String(10))
    course = db.Column(db.String(50))
    semester = db.Column(db.String(20))