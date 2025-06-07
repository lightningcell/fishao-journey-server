from models import db, BaseEntity

class CollectionCompletion(BaseEntity):
    __tablename__ = 'collection_completion'
    id = db.Column(db.Integer, primary_key=True)
    completion_id = db.Column(db.Integer)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="collection_completions")
