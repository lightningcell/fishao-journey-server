from models import db

class OutfitTemplate(db.Model):
    __tablename__ = 'outfit_template'
    id = db.Column(db.Integer, primary_key=True)

    # One-to-one relationship with Outfit (OutfitTemplate is the owner)
    outfit = db.relationship('Outfit', back_populates='outfit_template', uselist=False)
