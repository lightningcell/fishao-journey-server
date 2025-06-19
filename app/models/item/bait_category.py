from app.models import db, BaseEntity

class BaitCategory(BaseEntity):
    __tablename__ = 'bait_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    baits = db.relationship('Bait', back_populates='category', lazy='dynamic')
    # Many-to-Many: BaitCategory <-> Fish
    fishes = db.relationship('Fish', secondary='fish_bait_category', back_populates='bait_categories')
