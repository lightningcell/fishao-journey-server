from app.models import db, BaseEntity

class FishingLog(BaseEntity):
    __tablename__ = 'fishing_log'
    id = db.Column(db.Integer, primary_key=True)
    is_shiny = db.Column(db.Boolean)
    earned_xp = db.Column(db.Float)
    width = db.Column(db.Float)
    created_date = db.Column(db.DateTime, nullable=False)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="fishing_logs")

    # One-to-Many: FishingLog -> Area
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    area = db.relationship('Area', back_populates='fishing_logs')

    # One-to-Many: FishingLog -> Bait
    bait_id = db.Column(db.Integer, db.ForeignKey('bait.id'))
    bait = db.relationship('Bait', back_populates='fishing_logs')

    # One-to-Many: FishingLog -> Player
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='fishing_logs')

    # One-to-Many: FishingLog -> Rod
    rod_id = db.Column(db.Integer, db.ForeignKey('rod.id'))
    rod = db.relationship('Rod', back_populates='fishing_logs')
