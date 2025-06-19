from app.models import db, BaseEntity
from datetime import datetime
from app.enums.enum_upgrade_type import UpgradeType

class UpgradeRecord(BaseEntity):
    __tablename__ = 'upgrade_record'
    id = db.Column(db.Integer, primary_key=True)
    end_date = db.Column(db.DateTime)
    upgrade_type = db.Column(db.Enum(UpgradeType))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship("Player", back_populates="upgrade_records")
