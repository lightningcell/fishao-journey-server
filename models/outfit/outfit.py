from models import db

class Outfit(db.Model):
    __tablename__ = 'outfit'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String, nullable=False)

    outfit_template_id = db.Column(db.Integer, db.ForeignKey('outfit_template.id'), unique=True)
    outfit_template = db.relationship('OutfitTemplate', back_populates='outfit')
