from models import db

class TaskCompletion(db.Model):
    __tablename__ = 'task_completion'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, nullable=False)
    catched_fish_amount = db.Column(db.Integer, nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', back_populates='task_completions')
