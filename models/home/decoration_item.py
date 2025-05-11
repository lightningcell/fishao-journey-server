from models import db

class DecorationItem(db.Model):
    __tablename__ = 'decoration_item'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)

    # Foreign keys and relationships
    homeplan_id = db.Column(db.Integer, db.ForeignKey('homeplan.id'))
    homeplan = db.relationship('Homeplan', back_populates='decoration_items')

    decoration_id = db.Column(db.Integer, db.ForeignKey('decoration.id'))
    decoration = db.relationship('Decoration', back_populates='decoration_items')
