from models import db

class HomeFish(db.Model):
    __tablename__ = 'home_fish'
    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean, nullable=False)
