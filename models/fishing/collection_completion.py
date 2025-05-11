from models import db

class CollectionCompletion(db.Model):
    __tablename__ = 'collection_completion'
    id = db.Column(db.Integer, primary_key=True)
    completion_id = db.Column(db.Integer)

    fish_id = db.Column(db.Integer, db.ForeignKey('fish.id'))
    fish = db.relationship("Fish", back_populates="collection_completions")
