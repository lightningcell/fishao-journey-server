from models import db
from enums.enum_penalty_type import PenaltyType

class Penalty(db.Model):
    __tablename__ = 'penalty'
    id = db.Column(db.Integer, primary_key=True)
    penalty_type = db.Column(db.Enum(PenaltyType), nullable=False)
    period_minutes = db.Column(db.Integer, nullable=False)
