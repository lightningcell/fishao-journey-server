from models import db

class Fish(db.Model):
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
    fruit_combination_count_to_unlock = db.Column(db.Integer)

    # Relationships
    fishing_logs = db.relationship("FishingLog", back_populates="fish", lazy='dynamic')
    fishdex_notepads = db.relationship("FishdexNotepad", back_populates="fish", lazy='dynamic')
    caught_times = db.relationship("CaughtTime", back_populates="fish", lazy='dynamic')
    caught_dates = db.relationship("CaughtDate", back_populates="fish", lazy='dynamic')
    collection_completions = db.relationship("CollectionCompletion", back_populates="fish", lazy='dynamic')
    area_fishes = db.relationship("AreaFish", back_populates="fish", lazy='dynamic')
