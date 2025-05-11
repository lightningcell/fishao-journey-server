from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ChatLog(db.Model):
    __tablename__ = 'chat_log'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

class PM(db.Model):
    __tablename__ = 'pm'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)