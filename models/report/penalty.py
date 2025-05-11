from models import db

class Penalty(db.Model):
    __tablename__ = 'penalty'
    id = db.Column(db.Integer, primary_key=True)
    penalty_type = db.Column(db.Enum('BAN', 'MUTE', 'WARNING', name='penalty_type_enum'), nullable=False)
    period_minutes = db.Column(db.Integer, nullable=False)
