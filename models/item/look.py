from models import db

class Look(db.Model):
    __tablename__ = 'look'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    item = db.relationship('Item', back_populates='look', uselist=False)
