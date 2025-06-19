from models import db, BaseEntity

class ConfigNPC(BaseEntity):
    __tablename__ = 'config_npc'
    id = db.Column(db.Integer, primary_key=True)
    herb_amount = db.Column(db.Integer, nullable=False)
    vasily_rate = db.Column(db.Integer, nullable=False)
    
    herb_area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    herb_area = db.relationship('Area', back_populates='config_npc')

    herb_fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    herb_fish = db.relationship('Fish', back_populates='config_npc')
