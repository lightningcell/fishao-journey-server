from models import db
from datetime import datetime

# Association Table for Friends
Player_Friend = db.Table(
    'player_friend',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

from .account import Account

class Player(Account):
    __tablename__ = 'player'
    id = db.Column(db.Integer, db.ForeignKey('account.id'), primary_key=True)
    fishbucks = db.Column(db.Integer)
    fishcoins = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    level = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    online = db.Column(db.Boolean, default=False)

    # Friendship (Self-referential Many-to-Many)
    friends = db.relationship(
        'Player',
        secondary=Player_Friend,
        primaryjoin=id==Player_Friend.c.player_id,
        secondaryjoin=id==Player_Friend.c.friend_id,
        backref='friend_of'
    )

    # One-to-one relationships (reverse side)
    settings = db.relationship("PlayerSettings", back_populates="player", uselist=False)
    stats = db.relationship("PlayerStats", back_populates="player", uselist=False)
    moneytree = db.relationship("MoneyTree", back_populates="player", uselist=False)

    # One-to-many relationships
    area_registrations = db.relationship("AreaRegistration", back_populates="player", lazy='dynamic')
    upgrade_records = db.relationship("UpgradeRecord", back_populates="player", lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'player',
    }
