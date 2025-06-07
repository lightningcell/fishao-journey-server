from models import db, BaseEntity

class Homeplan(BaseEntity):
    __tablename__ = 'homeplan'
    id = db.Column(db.Integer, primary_key=True)
    # Add fields if needed

    # One-to-many relationship with DecorationItem
    decoration_items = db.relationship('DecorationItem', back_populates='homeplan', lazy='dynamic')

    # Reverse one-to-one for Player_Homeplan
    player = db.relationship('Player', back_populates='homeplan', uselist=False)
