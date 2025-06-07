from models import db, BaseEntity

class TaskCompletion(BaseEntity):
    __tablename__ = 'task_completion'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, nullable=False)
    catched_fish_amount = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', back_populates='task_completions')

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates='task_completions')
