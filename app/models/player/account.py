from models import db, BaseEntity
from datetime import datetime

# Association table for many-to-many relationship between Account and AccountRole
account_roles = db.Table('account_roles',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
    db.Column('account_role_id', db.Integer, db.ForeignKey('account_role.id'), primary_key=True)
)

class Account(BaseEntity):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)    
    is_active = db.Column(db.Boolean, default=True)
    is_banned = db.Column(db.Boolean, default=False)
    changed_date = db.Column(db.DateTime)
    owner = db.Column(db.String)
    changed_by = db.Column(db.String)
    # Add more fields as needed
    
    type = db.Column(db.String(50))

    # Many-to-many relationship with AccountRole
    roles = db.relationship('AccountRole', secondary=account_roles, back_populates='accounts')

    __mapper_args__ = {
        'polymorphic_identity': 'account',
        'polymorphic_on': 'type'
    }
