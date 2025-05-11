from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NPC(db.Model):
    __tablename__ = 'npc'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class ConfigNPC(db.Model):
    __tablename__ = 'config_npc'
    id = db.Column(db.Integer, primary_key=True)
    herb_amount = db.Column(db.Integer, nullable=False)
    vasily_rate = db.Column(db.Integer, nullable=False)

class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    raft_start_time = db.Column(db.DateTime, nullable=False)
    raft_end_time = db.Column(db.DateTime, nullable=False)