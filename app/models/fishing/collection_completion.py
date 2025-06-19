from app.models import db, BaseEntity

class CollectionCompletion(BaseEntity):
    __tablename__ = 'collection_completion'
    id = db.Column(db.Integer, primary_key=True)
    completion_id = db.Column(db.Integer)
    name = db.Column(db.String)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="collection_completions")
