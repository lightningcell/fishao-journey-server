from models import db, BaseEntity

class SpecialLocation(BaseEntity):
    __tablename__ = 'special_location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', back_populates='special_locations')    # Many-to-Many: SpecialLocation <-> Fish
    fishes = db.relationship('Fish', secondary='fish_special_location', back_populates='special_locations')
    
    # One-to-many relationship with Task
    tasks = db.relationship('Task', back_populates='special_location', lazy='dynamic')
