from models import db

class SpecialLocation(db.Model):
    __tablename__ = 'special_location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    areas = db.relationship('Area', back_populates='special_location', lazy='dynamic')
