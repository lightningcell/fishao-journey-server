from models import db

class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    traded_with_npc = db.Column(db.Boolean, nullable=False)
