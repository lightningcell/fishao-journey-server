from app.models import db, BaseEntity

# Association table for Fish_Area
fish_area = db.Table(
    'fish_area',
    db.Column('fish_id', db.Integer, db.ForeignKey('fish.id'), primary_key=True),
    db.Column('area_id', db.Integer, db.ForeignKey('area.id'), primary_key=True)
)

# Association table for Fish_SpecialLocation
fish_special_location = db.Table(
    'fish_special_location',
    db.Column('fish_id', db.Integer, db.ForeignKey('fish.id'), primary_key=True),
    db.Column('special_location_id', db.Integer, db.ForeignKey('special_location.id'), primary_key=True)
)

# Association table for Fish_BaitCategory
fish_bait_category = db.Table(
    'fish_bait_category',
    db.Column('fish_id', db.Integer, db.ForeignKey('fish.id'), primary_key=True),
    db.Column('bait_category_id', db.Integer, db.ForeignKey('bait_category.id'), primary_key=True)
)

class Fish(BaseEntity):
    __tablename__ = 'fish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    star_rate = db.Column(db.Integer)
    rarity_factor = db.Column(db.Float)
    min_length = db.Column(db.Integer)
    average_length = db.Column(db.Integer)
    max_length = db.Column(db.Integer)
    breed_duration_hours = db.Column(db.Integer)
    breed_cost = db.Column(db.Integer)
    breed_success_rate = db.Column(db.Float)
    hue_shift_of_shiny = db.Column(db.Integer)
    price = db.Column(db.Integer)
    club_points = db.Column(db.Integer)
    fishcoins_to_unlock = db.Column(db.Integer)
    
    # Foreign key for fruit combination requirement
    fruit_combination_id = db.Column(db.Integer, db.ForeignKey('fruit_combination.id'))

    # Relationships
    fishing_logs = db.relationship("FishingLog", back_populates="fish", lazy='dynamic')
    fishdex_notepads = db.relationship("FishdexNotepad", back_populates="fish", lazy='dynamic')
    caught_times = db.relationship("CaughtTime", back_populates="fish", lazy='dynamic')
    caught_dates = db.relationship("CaughtDate", back_populates="fish", lazy='dynamic')
    collection_completions = db.relationship("CollectionCompletion", back_populates="fish", lazy='dynamic')
    area_fishes = db.relationship("AreaFish", back_populates="fish", lazy='dynamic')
    home_fishes = db.relationship("HomeFish", back_populates="fish", lazy='dynamic')

    # One-to-many: ClubFish-Fish reverse relationship
    club_fishes = db.relationship('ClubFish', back_populates='fish', lazy='dynamic')

    # One-to-Many: Fish -> Task
    tasks = db.relationship('Task', back_populates='fish', lazy='dynamic')

    # Many-to-Many: Fish <-> Area
    areas = db.relationship('Area', secondary=fish_area, back_populates='fishes')

    # Many-to-Many: Fish <-> BaitCategory
    bait_categories = db.relationship('BaitCategory', secondary=fish_bait_category, back_populates='fishes')    # Many-to-Many: Fish <-> SpecialLocation
    special_locations = db.relationship('SpecialLocation', secondary=fish_special_location, back_populates='fishes')

    # One-to-One: Fish -> FruitCombination (for unlock requirement)
    fruit_combination = db.relationship('FruitCombination', backref='unlocked_fish', uselist=False)    # Reverse relationship for ConfigNPC_HerbFish
    config_npc = db.relationship('ConfigNPC', back_populates='herb_fish', uselist=False)
    
    # Many-to-many relationship with Collection
    collections = db.relationship('Collection', secondary='collection_fish', back_populates='fishes', lazy='dynamic')
