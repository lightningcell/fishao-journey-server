from models import db, BaseEntity

class DecorationCategory(BaseEntity):
    __tablename__ = 'decoration_category'
    id = db.Column(db.Integer, primary_key=True)
    # Add fields if needed

    decorations = db.relationship('Decoration', back_populates='category', lazy='dynamic')
