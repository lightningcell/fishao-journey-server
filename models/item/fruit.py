from models import db, BaseEntity

class Fruit(BaseEntity):
    __tablename__ = 'fruit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    items = db.relationship('Item', back_populates='fruit')
