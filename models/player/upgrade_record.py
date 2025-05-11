from models import db
from datetime import datetime

class UpgradeRecord(db.Model):
    __tablename__ = 'upgrade_record'
    id = db.Column(db.Integer, primary_key=True)
    end_date = db.Column(db.DateTime)
    upgrade_type = db.Column(db.Enum('Speed', 'Capacity', name='upgrade_type_enum'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship("Player", back_populates="upgrade_records")
