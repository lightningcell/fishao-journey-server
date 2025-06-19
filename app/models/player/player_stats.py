from models import db, BaseEntity

class PlayerStats(BaseEntity):
    __tablename__ = 'player_stats'
    id = db.Column(db.Integer, primary_key=True)
    total_game_play_hours = db.Column(db.Integer)
    won_tournament_count = db.Column(db.Integer)
    earned_award_count = db.Column(db.Integer)
    completed_tasks_count = db.Column(db.Integer)
    biggest_fish_catched_width = db.Column(db.Integer)
    total_fish_catched_count = db.Column(db.Integer)
    total_fish_species_catched_count = db.Column(db.Integer)
    home_points = db.Column(db.Integer)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    player = db.relationship("Player", back_populates="stats", uselist=False)
