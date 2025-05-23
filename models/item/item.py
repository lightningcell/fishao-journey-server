from models import db
from enums.enum_inventory_type import InventoryType

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.Enum(InventoryType), nullable=False)
    type = db.Column(db.String(50))

    bait_id = db.Column(db.Integer, db.ForeignKey('bait.id'))
    rod_id = db.Column(db.Integer, db.ForeignKey('rod.id'))
    look_id = db.Column(db.Integer, db.ForeignKey('look.id'))
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'))

    bait = db.relationship('Bait', back_populates='item')
    rod = db.relationship('Rod', back_populates='item')
    look = db.relationship('Look', back_populates='item')
    fruit = db.relationship('Fruit', back_populates='item')

    # Player relationship (One-to-Many)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='items')

    # Decoration relationship (One-to-One)
    decoration_id = db.Column(db.Integer, db.ForeignKey('decoration.id'), unique=True)
    decoration = db.relationship('Decoration', back_populates='item', uselist=False)

    # Trade relationships (One-to-Many for given and taken)
    trade_given_id = db.Column(db.Integer, db.ForeignKey('trade.id'))
    trade_given = db.relationship('Trade', back_populates='items_given', foreign_keys=[trade_given_id])

    trade_taken_id = db.Column(db.Integer, db.ForeignKey('trade.id'))
    trade_taken = db.relationship('Trade', back_populates='items_taken', foreign_keys=[trade_taken_id])

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }
