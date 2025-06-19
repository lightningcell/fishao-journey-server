from app.models.item.item import Item
from app.models import db, BaseEntity

class ShopItem(Item):
    __tablename__ = 'shop_item'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'shop_item',
    }