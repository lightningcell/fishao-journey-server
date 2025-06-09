from models import db, BaseEntity
from enums.enum_registration_type import RegistrationType

class Task(BaseEntity):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    fishing_mission_quantity = db.Column(db.Integer, nullable=False)
    is_shine_fishing_log = db.Column(db.Boolean, nullable=False)
    star_rate = db.Column(db.Integer, nullable=False)
    fish_length = db.Column(db.Integer, nullable=False)
    area_registration_type = db.Column(db.Enum(RegistrationType), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    area = db.relationship('Area', back_populates='tasks')
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship('Fish', back_populates='tasks')
    npc_id = db.Column(db.Integer, db.ForeignKey('npc.id'))
    npc = db.relationship('NPC', back_populates='tasks')

    # One-to-many relationship with TaskCompletion
    task_completions = db.relationship('TaskCompletion', back_populates='task', lazy='dynamic')
    # One-to-many relationship with TaskAward
    task_awards = db.relationship('TaskAward', back_populates='task', lazy='dynamic')
