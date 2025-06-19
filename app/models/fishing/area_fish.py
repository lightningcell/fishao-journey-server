from models import db, BaseEntity

class AreaFish(BaseEntity):
    __tablename__ = 'area_fish'
    id = db.Column(db.Integer, primary_key=True)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="area_fishes")

    # One-to-Many: AreaFish -> Area
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    area = db.relationship('Area', back_populates='area_fishes')
