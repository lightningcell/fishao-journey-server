from app.models import db, BaseEntity

class DecorationCategory(BaseEntity):
    __tablename__ = 'decoration_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    decorations = db.relationship('Decoration', back_populates='category', lazy='dynamic')
