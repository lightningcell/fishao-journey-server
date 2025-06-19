from models import db, BaseEntity

class ClubPlayer(BaseEntity):
    __tablename__ = 'club_player'
    id = db.Column(db.Integer, primary_key=True)

    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    club = db.relationship('Club', back_populates='club_players')
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='club_players')
    created_date = db.Column(db.DateTime)
