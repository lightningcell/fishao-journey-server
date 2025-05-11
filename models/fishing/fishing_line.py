from models import db

class FishingLine(db.Model):
    __tablename__ = 'fishing_line'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    color = db.Column(db.String)
