from models import db, BaseEntity

class CaughtDate(BaseEntity):
    __tablename__ = 'caught_date'
    id = db.Column(db.Integer, primary_key=True)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="caught_dates")
