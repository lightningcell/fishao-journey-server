from models import db

class NPC(db.Model):
    __tablename__ = 'npc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
