from models import db, BaseEntity

class Payment(BaseEntity):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    owner = db.Column(db.String)
