from app.models import db, BaseEntity
from app.enums.enum_width_unit import WidthUnit

class PlayerSettings(BaseEntity):
    __tablename__ = 'player_settings'
    id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.DateTime)
    show_birth_date_on_profile = db.Column(db.Boolean)
    show_email_on_profile = db.Column(db.Boolean)
    show_inventory_on_profile = db.Column(db.Boolean)
    receive_emails = db.Column(db.Boolean)
    width_unit = db.Column(db.Enum(WidthUnit))
    time_zone_last_update = db.Column(db.DateTime)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    player = db.relationship("Player", back_populates="settings", uselist=False)
