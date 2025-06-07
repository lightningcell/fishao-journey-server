from models import db, BaseEntity

class PM(BaseEntity):
    __tablename__ = 'pm'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    seen = db.Column(db.Boolean, nullable=False, default=False)
    created_date = db.Column(db.DateTime)

    # One-to-Many: PM -> Player (Receiver)
    receiver_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    receiver = db.relationship('Player', back_populates='received_pms', foreign_keys=[receiver_id])

    # One-to-Many: PM -> Player (Sender)
    sender_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    sender = db.relationship('Player', back_populates='sent_pms', foreign_keys=[sender_id])
