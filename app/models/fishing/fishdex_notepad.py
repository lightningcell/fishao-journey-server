from models import db, BaseEntity

class FishdexNotepad(BaseEntity):
    __tablename__ = 'fishdex_notepad'
    id = db.Column(db.Integer, primary_key=True)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="fishdex_notepads")

    # One-to-Many: FishdexNotepad -> Player
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='fishdex_notepads')
