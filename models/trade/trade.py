from models import db

class Trade(db.Model):
    __tablename__ = 'trade'
    id = db.Column(db.Integer, primary_key=True)
    traded_with_npc = db.Column(db.Boolean, nullable=False)
    # Reverse one-to-many for Item_TradeGiven
    items_given = db.relationship('Item', back_populates='trade_given', foreign_keys='Item.trade_given_id', lazy='dynamic')
    # Reverse one-to-many for Item_TradeTaken
    items_taken = db.relationship('Item', back_populates='trade_taken', foreign_keys='Item.trade_taken_id', lazy='dynamic')
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    area = db.relationship('Area', back_populates='trades')
    given_by_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    given_by = db.relationship('Player', back_populates='trades_given', foreign_keys=[given_by_id])
    taken_by_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    taken_by = db.relationship('Player', back_populates='trades_taken', foreign_keys=[taken_by_id])
    created_date = db.Column(db.DateTime)
