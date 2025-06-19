from app.models import db, BaseEntity
from datetime import datetime

class DecorationRecord(BaseEntity):
    __tablename__ = 'decoration_record'
    id = db.Column(db.Integer, primary_key=True)
    decor_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship("Player", back_populates="decoration_records")
