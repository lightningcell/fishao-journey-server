from models import db

class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    badge_id = db.Column(db.Integer)
    is_sub_area = db.Column(db.Boolean, default=False)
    area_id = db.Column(db.Integer, unique=True)  # Unique AreaID
    level_requirement = db.Column(db.Integer)

    special_locations = db.relationship('SpecialLocation', back_populates='area', lazy='dynamic')

    # Self-referential one-to-many for subareas
    parent_area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    sub_areas = db.relationship('Area', backref=db.backref('parent_area', remote_side=[id]), lazy='dynamic')

    # Reverse relationship for Player_CurrentArea
    players = db.relationship('Player', back_populates='current_area', foreign_keys='Player.current_area_id', lazy='dynamic')

    # Reverse relationship for FishingLog_Area
    fishing_logs = db.relationship('FishingLog', back_populates='area', lazy='dynamic')

    # Many-to-Many: Area <-> Fish
    fishes = db.relationship('Fish', secondary='fish_area', back_populates='areas')

    # One-to-Many: AreaFish -> Area
    area_fishes = db.relationship('AreaFish', back_populates='area', lazy='dynamic')

    # Reverse relationship for ConfigNPC_HerbArea
    config_npc = db.relationship('ConfigNPC', back_populates='herb_area', uselist=False)

    # One-to-Many: Area -> Task
    tasks = db.relationship('Task', back_populates='area', lazy='dynamic')

    # One-to-Many: Area -> Trade
    trades = db.relationship('Trade', back_populates='area', lazy='dynamic')
