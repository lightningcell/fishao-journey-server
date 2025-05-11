from models import db

class ClubPlayer(db.Model):
    __tablename__ = 'club_player'
    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club', back_populates='club_players')
