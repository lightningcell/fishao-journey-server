from app.models import db, BaseEntity
from datetime import datetime

class FruitRecord(BaseEntity):
    __tablename__ = 'fruit_record'
    id = db.Column(db.Integer, primary_key=True)
    fruit_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship("Player", back_populates="fruit_records")
