from models.item.item import Item
from models import db

class TaskAward(Item):
    __tablename__ = 'task_award'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', back_populates='task_awards')

    __mapper_args__ = {
        'polymorphic_identity': 'task_award',
    }
