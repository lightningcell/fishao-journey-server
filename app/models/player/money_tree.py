from models import db, BaseEntity

class MoneyTree(BaseEntity):
    __tablename__ = 'money_tree'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), unique=True)
    player = db.relationship("Player", back_populates="moneytree", uselist=False)
