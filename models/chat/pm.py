from models import db

class PM(db.Model):
    __tablename__ = 'pm'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)
