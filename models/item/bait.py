from models import db, BaseEntity

class Bait(BaseEntity):
    __tablename__ = 'bait'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bait_id = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('bait_category.id'))
    category = db.relationship('BaitCategory', back_populates='baits')

    items = db.relationship('Item', back_populates='bait')  # One-to-many: a bait can have many items, but an item can only be one bait

    # Reverse relationship for FishingLog_Bait
    fishing_logs = db.relationship('FishingLog', back_populates='bait', lazy='dynamic')
