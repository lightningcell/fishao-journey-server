from app.models import db, BaseEntity

class Config(BaseEntity):
    __tablename__ = 'config'
    id = db.Column(db.Integer, primary_key=True)
    raft_start_time = db.Column(db.DateTime, nullable=False)
    raft_end_time = db.Column(db.DateTime, nullable=False)
