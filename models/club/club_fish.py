from models import db

class ClubFish(db.Model):
    __tablename__ = 'club_fish'
    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club', back_populates='club_fishes')
