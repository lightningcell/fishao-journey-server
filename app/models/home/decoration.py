from models import db, BaseEntity

class Decoration(BaseEntity):
    __tablename__ = 'decoration'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    homepoints = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('decoration_category.id'))
    category = db.relationship('DecorationCategory', back_populates='decorations')

    decoration_items = db.relationship('DecorationItem', back_populates='decoration', lazy='dynamic')
    
    # Reverse one-to-one for Item_Decoration
    item = db.relationship('Item', back_populates='decoration', uselist=False)  # One-to-one: a decoration can have one item, and an item can only be one decoration
    
    # Many-to-many relationship with Collection
    collections = db.relationship('Collection', secondary='collection_decoration', back_populates='decorations', lazy='dynamic')
