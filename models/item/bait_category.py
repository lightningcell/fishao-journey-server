from models import db

class BaitCategory(db.Model):
    __tablename__ = 'bait_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    baits = db.relationship('Bait', back_populates='category', lazy='dynamic')
