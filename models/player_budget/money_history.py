from models import db, BaseEntity

class MoneyHistory(BaseEntity):
    __tablename__ = 'money_history'
    id = db.Column(db.Integer, primary_key=True)
    is_fish_bucks = db.Column(db.Boolean, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='money_histories')
    created_date = db.Column(db.DateTime)
