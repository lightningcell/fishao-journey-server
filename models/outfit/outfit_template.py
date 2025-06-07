from models import db, BaseEntity

class OutfitTemplate(BaseEntity):
    __tablename__ = 'outfit_template'
    id = db.Column(db.Integer, primary_key=True)

    # One-to-one relationship with Outfit (OutfitTemplate is the owner)
    outfit = db.relationship('Outfit', back_populates='outfit_template', uselist=False)

    # One-to-Many: OutfitTemplate -> Player
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='outfit_templates')
