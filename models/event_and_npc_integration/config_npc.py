from models import db

class ConfigNPC(db.Model):
    __tablename__ = 'config_npc'
    id = db.Column(db.Integer, primary_key=True)
    herb_amount = db.Column(db.Integer, nullable=False)
    vasily_rate = db.Column(db.Integer, nullable=False)
