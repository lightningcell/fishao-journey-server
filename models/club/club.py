from models import db

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)

    # One-to-many relationships
    club_players = db.relationship('ClubPlayer', back_populates='club', lazy='dynamic')
    club_fishes = db.relationship('ClubFish', back_populates='club', lazy='dynamic')
