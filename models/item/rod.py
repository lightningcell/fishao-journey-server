from models import db

class Rod(db.Model):
    __tablename__ = 'rod'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Enum('Small', 'Medium', 'Large', name='rod_size_enum'), nullable=False)
    length_quality = db.Column(db.Integer, nullable=False)
    
    item = db.relationship('Item', back_populates='rod', uselist=False)
