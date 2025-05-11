from models import db
from enums.enum_registration_type import RegistrationType

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    fishing_mission_quantity = db.Column(db.Integer, nullable=False)
    is_shine_fishing_log = db.Column(db.Boolean, nullable=False)
    star_rate = db.Column(db.Integer, nullable=False)
    fish_length = db.Column(db.Integer, nullable=False)
    area_registration_type = db.Column(db.Enum(RegistrationType), nullable=False)

    # One-to-many relationship with TaskCompletion
    task_completions = db.relationship('TaskCompletion', back_populates='task', lazy='dynamic')
    # One-to-many relationship with TaskAward
    task_awards = db.relationship('TaskAward', back_populates='task', lazy='dynamic')
