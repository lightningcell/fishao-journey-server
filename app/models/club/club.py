from app.models import db, BaseEntity

class Club(BaseEntity):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    leader = db.relationship('Player', back_populates='led_club', uselist=False, foreign_keys=[leader_id])
    created_date = db.Column(db.DateTime)

    # One-to-many relationships
    club_players = db.relationship('ClubPlayer', back_populates='club', lazy='dynamic')
    club_fishes = db.relationship('ClubFish', back_populates='club', lazy='dynamic')
