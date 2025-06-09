from models import db, BaseEntity
from enums.enum_inventory_type import InventoryType

class Item(BaseEntity):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.Enum(InventoryType), nullable=False)
    type = db.Column(db.String(50))

    # Only one of the following can be set for each item:
    bait_id = db.Column(db.Integer, db.ForeignKey('bait.id'), nullable=True)
    rod_id = db.Column(db.Integer, db.ForeignKey('rod.id'), nullable=True)
    look_id = db.Column(db.Integer, db.ForeignKey('look.id'), nullable=True)
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=True)
    decoration_id = db.Column(db.Integer, db.ForeignKey('decoration.id'), unique=True, nullable=True)

    bait = db.relationship('Bait', back_populates='items')
    rod = db.relationship('Rod', back_populates='items')
    look = db.relationship('Look', back_populates='items')
    fruit = db.relationship('Fruit', back_populates='items')
    decoration = db.relationship('Decoration', back_populates='item', uselist=False)

    # Player relationship (One-to-Many)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='items')

    # Reverse relationships for a player's currently selected items
    current_bait_for_player = db.relationship(
        'Player',
        back_populates='current_bait_item',
        foreign_keys='Player.current_bait_item_id',
        uselist=False
    )
    current_rod_for_player = db.relationship(
        'Player',
        back_populates='current_rod_item',
        foreign_keys='Player.current_rod_item_id',
        uselist=False
    )

    # Trade relationships (One-to-Many for given and taken)
    trade_given_id = db.Column(db.Integer, db.ForeignKey('trade.id'))
    trade_given = db.relationship('Trade', back_populates='items_given', foreign_keys=[trade_given_id])

    trade_taken_id = db.Column(db.Integer, db.ForeignKey('trade.id'))
    trade_taken = db.relationship('Trade', back_populates='items_taken', foreign_keys=[trade_taken_id])

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }
