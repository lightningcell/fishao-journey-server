from models import db

class FishdexNotepad(db.Model):
    __tablename__ = 'fishdex_notepad'
    id = db.Column(db.Integer, primary_key=True)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="fishdex_notepads")
