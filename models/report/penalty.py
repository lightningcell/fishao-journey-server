from models import db, BaseEntity
from enums.enum_penalty_type import PenaltyType

class Penalty(BaseEntity):
    __tablename__ = 'penalty'
    id = db.Column(db.Integer, primary_key=True)
    penalty_type = db.Column(db.Enum(PenaltyType), nullable=False)
    period_minutes = db.Column(db.Integer, nullable=False)
    moderator_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    moderator = db.relationship('Player', back_populates='moderated_penalties', foreign_keys=[moderator_id])
    created_date = db.Column(db.DateTime)

    penalized_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    penalized_player = db.relationship('Player', back_populates='penalized_penalties', foreign_keys=[penalized_player_id])
