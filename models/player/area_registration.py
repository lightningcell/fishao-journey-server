from models import db
from datetime import datetime

class AreaRegistration(db.Model):
    __tablename__ = 'area_registration'
    id = db.Column(db.Integer, primary_key=True)
    registration_type = db.Column(db.Enum('TypeA', 'TypeB', name='registration_type_enum'))
    duration_seconds = db.Column(db.Integer)
    end_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship("Player", back_populates="area_registrations")
