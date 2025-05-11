from models import db

class FishingLog(db.Model):
    __tablename__ = 'fishing_log'
    id = db.Column(db.Integer, primary_key=True)
    is_shiny = db.Column(db.Boolean)
    earned_xp = db.Column(db.Float)
    width = db.Column(db.Float)
    created_date = db.Column(db.DateTime, nullable=False)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="fishing_logs")
