from models import db, BaseEntity

class Reject(BaseEntity):
    __tablename__ = 'reject'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    moderator_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    moderator = db.relationship('Player', back_populates='moderated_rejects', foreign_keys=[moderator_id])
