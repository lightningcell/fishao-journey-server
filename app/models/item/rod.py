from models import db, BaseEntity
from enums.enum_rod_sizes import RodSizes

class Rod(BaseEntity):
    __tablename__ = 'rod'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Enum(RodSizes), nullable=False)
    length_quality = db.Column(db.Integer, nullable=False)
    
    items = db.relationship('Item', back_populates='rod')  # One-to-many: a rod can have many items, but an item can only be one rod
    fishing_logs = db.relationship('FishingLog', back_populates='rod', lazy='dynamic')
