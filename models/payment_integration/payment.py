from models import db, BaseEntity

class Payment(BaseEntity):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    owner = db.Column(db.String)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
