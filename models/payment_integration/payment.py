from models import db

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    owner = db.Column(db.String)
