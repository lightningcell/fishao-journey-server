from app.models import db, BaseEntity

class Fruit(BaseEntity):
    __tablename__ = 'fruit'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    items = db.relationship('Item', back_populates='fruit')  # One-to-many: a fruit can have many items, but an item can only be one fruit
    
    # Many-to-many relationship with Collection
    collections = db.relationship('Collection', secondary='collection_fruit', back_populates='fruits', lazy='dynamic')
