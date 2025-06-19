from models import db, BaseEntity

class ClubFish(BaseEntity):
    __tablename__ = 'club_fish'
    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club', back_populates='club_fishes')
    
    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship('Fish', back_populates='club_fishes')
