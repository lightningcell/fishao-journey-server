from models import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    item_type = db.Column(db.Enum('Bait', 'Rod', 'Look', 'Fruit', name='item_type_enum'), nullable=False)
    type = db.Column(db.String(50))

    bait_id = db.Column(db.Integer, db.ForeignKey('bait.id'))
    rod_id = db.Column(db.Integer, db.ForeignKey('rod.id'))
    look_id = db.Column(db.Integer, db.ForeignKey('look.id'))
    fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'))

    bait = db.relationship('Bait', back_populates='item')
    rod = db.relationship('Rod', back_populates='item')
    look = db.relationship('Look', back_populates='item')
    fruit = db.relationship('Fruit', back_populates='item')

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type
    }
