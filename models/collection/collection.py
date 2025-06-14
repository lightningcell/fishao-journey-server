from models import db, BaseEntity
from enums.enum_collection_type import CollectionType

# Association table for Collection-Decoration Many-to-Many relationship
collection_decoration = db.Table(
    'collection_decoration',
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True),
    db.Column('decoration_id', db.Integer, db.ForeignKey('decoration.id'), primary_key=True)
)

# Association table for Collection-Fish Many-to-Many relationship
collection_fish = db.Table(
    'collection_fish',
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True),
    db.Column('fish_id', db.Integer, db.ForeignKey('fish.id'), primary_key=True)
)

# Association table for Collection-Fruit Many-to-Many relationship
collection_fruit = db.Table(
    'collection_fruit',
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True),
    db.Column('fruit_id', db.Integer, db.ForeignKey('fruit.id'), primary_key=True)
)

class Collection(BaseEntity):
    __tablename__ = 'collection'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(CollectionType), nullable=False)
    
    # Many-to-many relationships
    decorations = db.relationship(
        'Decoration',
        secondary=collection_decoration,
        back_populates='collections',
        lazy='dynamic'
    )
    
    fishes = db.relationship(
        'Fish',
        secondary=collection_fish,
        back_populates='collections',
        lazy='dynamic'
    )
    
    fruits = db.relationship(
        'Fruit',
        secondary=collection_fruit,
        back_populates='collections',
        lazy='dynamic'
    )
