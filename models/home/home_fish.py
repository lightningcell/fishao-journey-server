from models import db, BaseEntity

class HomeFish(BaseEntity):
    __tablename__ = 'home_fish'
    id = db.Column(db.Integer, primary_key=True)
    is_completed = db.Column(db.Boolean, nullable=False)
    
    # HomeFish_Fish relationship - HomeFish references one Fish
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship('Fish', back_populates='home_fishes')
    
    # HomeFish_Player relationship - HomeFish references one Player
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='home_fishes')
