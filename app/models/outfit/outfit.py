from app.models import db, BaseEntity

class Outfit(BaseEntity):
    __tablename__ = 'outfit'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String, nullable=False)

    outfit_template_id = db.Column(db.Integer, db.ForeignKey('outfit_template.id', use_alter=True, name='fk_outfit_outfit_template'), unique=True)
    outfit_template = db.relationship('OutfitTemplate', back_populates='outfit')
    
    # Reverse one-to-one for Player_Outfit
    player = db.relationship('Player', back_populates='outfit', uselist=False)
