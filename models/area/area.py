from models import db

class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    badge_id = db.Column(db.Integer)
    is_sub_area = db.Column(db.Boolean, default=False)
    area_id = db.Column(db.Integer, unique=True)  # Unique AreaID
    level_requirement = db.Column(db.Integer)

    # Foreign key to SpecialLocation
    special_location_id = db.Column(db.Integer, db.ForeignKey('special_location.id'))
    special_location = db.relationship('SpecialLocation', back_populates='areas')

    # Self-referential one-to-many for subareas
    parent_area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    sub_areas = db.relationship('Area', backref=db.backref('parent_area', remote_side=[id]), lazy='dynamic')
