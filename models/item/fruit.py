from models import db

class Fruit(db.Model):
    __tablename__ = 'fruit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    item = db.relationship('Item', back_populates='fruit', uselist=False)
