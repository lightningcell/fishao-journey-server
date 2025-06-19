from app.models import db, BaseEntity
from app.enums.enum_tournament_type import TournamentType
from datetime import datetime


class Tournament(BaseEntity):
    """
    Turnuvanın kendisini temsil eden model.
    Turnuva şablonu/tanımı gibi düşünülebilir.
    """
    __tablename__ = 'tournament'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    tournament_type = db.Column(db.Enum(TournamentType), nullable=False)
    max_participants = db.Column(db.Integer, default=15)
    duration_minutes = db.Column(db.Integer, default=60)  # Turnuva süresi dakika cinsinden
    is_active = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    tournament_histories = db.relationship('TournamentHistory', backref='tournament', lazy=True)
    
    def __repr__(self):
        return f'<Tournament {self.name}>'
