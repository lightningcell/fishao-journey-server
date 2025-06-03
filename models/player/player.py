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
    last_activity_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Friendship (Self-referential Many-to-Many)
    friends = db.relationship(
        'Player',
        secondary=Player_Friend,
        primaryjoin=id==Player_Friend.c.player_id,
        secondaryjoin=id==Player_Friend.c.friend_id,
        backref='friend_of'
    )

    # One-to-one and one-to-many relationships for current state
    current_area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    current_area = db.relationship('Area', back_populates='players', foreign_keys=[current_area_id])

    # Current rod/bait relationships
    current_rod_id = db.Column(db.Integer, db.ForeignKey('item.id'), unique=True)
    current_rod = db.relationship('Item', foreign_keys=[current_rod_id], back_populates='player_rod', uselist=False)

    current_bait_id = db.Column(db.Integer, db.ForeignKey('item.id'), unique=True)
    current_bait = db.relationship('Item', foreign_keys=[current_bait_id], back_populates='player_bait', uselist=False)

    homeplan_id = db.Column(db.Integer, db.ForeignKey('homeplan.id'), unique=True)
    homeplan = db.relationship('Homeplan', back_populates='player', uselist=False)

    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), unique=True)
    outfit = db.relationship('Outfit', back_populates='player', uselist=False)

    # Reverse relationship for Item_Player
    items = db.relationship('Item', back_populates='player', lazy='dynamic')

    # One-to-one relationships (reverse side)
    settings = db.relationship("PlayerSettings", back_populates="player", uselist=False)
    stats = db.relationship("PlayerStats", back_populates="player", uselist=False)
    moneytree = db.relationship("MoneyTree", back_populates="player", uselist=False)

    # One-to-many relationships
    area_registrations = db.relationship("AreaRegistration", back_populates="player", lazy='dynamic')
    upgrade_records = db.relationship("UpgradeRecord", back_populates="player", lazy='dynamic')
    home_fishes = db.relationship("HomeFish", back_populates="player", lazy='dynamic')

    # Reverse relationship for FishingLog_Player
    fishing_logs = db.relationship('FishingLog', back_populates='player', lazy='dynamic')

    # One-to-one relationship for FishingLine_Player
    fishing_line = db.relationship('FishingLine', back_populates='player', uselist=False)

    # Reverse relationship for FishdexNotepad_Player
    fishdex_notepads = db.relationship('FishdexNotepad', back_populates='player', lazy='dynamic')

    # Reverse relationship for OutfitTemplate_Player
    outfit_templates = db.relationship('OutfitTemplate', back_populates='player', lazy='dynamic')

    # Reverse relationships for PM
    received_pms = db.relationship('PM', back_populates='receiver', foreign_keys='PM.receiver_id', lazy='dynamic')
    sent_pms = db.relationship('PM', back_populates='sender', foreign_keys='PM.sender_id', lazy='dynamic')

    # Reverse relationships for Penalty (moderator and penalized)
    moderated_penalties = db.relationship('Penalty', back_populates='moderator', foreign_keys='Penalty.moderator_id', lazy='dynamic')
    penalized_penalties = db.relationship('Penalty', back_populates='penalized_player', foreign_keys='Penalty.penalized_player_id', lazy='dynamic')

    # Reverse relationships for ReportRecord (reported, reporting, reviewer)
    reported_reports = db.relationship('ReportRecord', back_populates='reported_player', foreign_keys='ReportRecord.reported_player_id', lazy='dynamic')
    reporting_reports = db.relationship('ReportRecord', back_populates='reporting_by_player', foreign_keys='ReportRecord.reporting_by_player_id', lazy='dynamic')
    reviewed_reports = db.relationship('ReportRecord', back_populates='reviewer_moderator', foreign_keys='ReportRecord.reviewer_moderator_id', lazy='dynamic')

    # Reverse relationship for Reject (moderator)
    moderated_rejects = db.relationship('Reject', back_populates='moderator', foreign_keys='Reject.moderator_id', lazy='dynamic')

    # ClubPlayer reverse relationship
    club_players = db.relationship('ClubPlayer', back_populates='player', lazy='dynamic')
    # Club Leader reverse relationship
    led_club = db.relationship('Club', back_populates='leader', uselist=False, foreign_keys='Club.leader_id')

    # One-to-Many: Player -> TaskCompletion
    task_completions = db.relationship('TaskCompletion', back_populates='player', lazy='dynamic')

    # One-to-Many: Player -> MoneyHistory
    money_histories = db.relationship('MoneyHistory', back_populates='player', lazy='dynamic')

    # One-to-Many: Player -> Trade (Given)
    trades_given = db.relationship('Trade', back_populates='given_by', foreign_keys='Trade.given_by_id', lazy='dynamic')
    # One-to-Many: Player -> Trade (Taken)
    trades_taken = db.relationship('Trade', back_populates='taken_by', foreign_keys='Trade.taken_by_id', lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'player',
    }
