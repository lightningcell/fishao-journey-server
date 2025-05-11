from models import db

class CaughtTime(db.Model):
    __tablename__ = 'caught_time'
    id = db.Column(db.Integer, primary_key=True)
    time_range = db.Column(db.String)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="caught_times")
