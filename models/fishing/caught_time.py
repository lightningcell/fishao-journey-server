from models import db, BaseEntity

class CaughtTime(BaseEntity):
    __tablename__ = 'caught_time'
    id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="caught_times")
