from models import db, BaseEntity

class CaughtDate(BaseEntity):
    __tablename__ = 'caught_date'
    id = db.Column(db.Integer, primary_key=True)
    date_range = db.Column(db.String)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="caught_dates")
