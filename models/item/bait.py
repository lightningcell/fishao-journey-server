from models import db

class Bait(db.Model):
    __tablename__ = 'bait'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bait_id = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('bait_category.id'))
    category = db.relationship('BaitCategory', back_populates='baits')

    items = db.relationship('Item', back_populates='bait')
