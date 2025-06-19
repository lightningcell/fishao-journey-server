from app.models import db, BaseEntity
from datetime import datetime
from app.enums.enum_tournament_status import TournamentStatus


class TournamentHistory(BaseEntity):
    """
    Düzenlenen/gerçekleşen turnuva kayıtları.
    Belirli bir Tournament'ın gerçek zamanlı kaydı.
    """
    __tablename__ = 'tournament_history'
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    actual_participants = db.Column(db.Integer, default=0)
    status = db.Column(db.Enum(TournamentStatus), default=TournamentStatus.WAITING)
    
    # İlişkiler
    tournament_logs = db.relationship('TournamentLog', backref='tournament_history', lazy=True)
    
    def __repr__(self):
        return f'<TournamentHistory {self.id} - {self.tournament.name}>'
    @property
    def is_completed(self):
        """Turnuva tamamlandı mı?"""
        return self.status == TournamentStatus.COMPLETED
    
    @property
    def is_active(self):
        """Turnuva aktif mi?"""
        return self.status == TournamentStatus.ACTIVE
