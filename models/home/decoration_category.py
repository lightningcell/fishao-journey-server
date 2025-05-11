from models import db

class DecorationCategory(db.Model):
    __tablename__ = 'decoration_category'
    id = db.Column(db.Integer, primary_key=True)
    # Add fields if needed

    decorations = db.relationship('Decoration', back_populates='category', lazy='dynamic')
