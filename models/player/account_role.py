from models import db, BaseEntity

class AccountRole(BaseEntity):
    __tablename__ = 'account_role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    
    # Many-to-many relationship with Account
    accounts = db.relationship('Account', secondary='account_roles', back_populates='roles')
    
    def __repr__(self):
        return f'<AccountRole {self.name}>'
