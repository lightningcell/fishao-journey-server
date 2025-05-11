from models import db

class Reject(db.Model):
    __tablename__ = 'reject'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
