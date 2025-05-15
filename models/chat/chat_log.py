from models import db

class ChatLog(db.Model):
    __tablename__ = 'chat_log'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime)
