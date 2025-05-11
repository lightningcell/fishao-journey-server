from models import db

class AreaFish(db.Model):
    __tablename__ = 'area_fish'
    id = db.Column(db.Integer, primary_key=True)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="area_fishes")
