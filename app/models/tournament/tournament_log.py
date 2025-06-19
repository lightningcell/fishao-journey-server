from app.models import db, BaseEntity
from datetime import datetime


class TournamentLog(BaseEntity):
    """
    Oyuncunun turnuvadaki performans kaydı.
    Oyuncunun bir TournamentHistory'deki sıralama bilgisi.
    """
    __tablename__ = 'tournament_log'
    
    id = db.Column(db.Integer, primary_key=True)
    
    tournament_history_id = db.Column(db.Integer, db.ForeignKey('tournament_history.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    order = db.Column(db.Integer, nullable=False)  # Sıralama (1 = kazandı, 2 = ikinci, vs.)
    score = db.Column(db.Integer, default=0)  # Turnuvadaki puan
    participation_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)  # Turnuva tamamlama zamanı

      # İlişkiler
    player = db.relationship('Player', backref='tournament_logs', lazy=True)
    
    def __repr__(self):
        return f'<TournamentLog Player:{self.player_id} Order:{self.order}>'
    
    @property
    def is_winner(self):
        """Oyuncu turnuvayı kazandı mı?"""
        return self.order == 1
    
    @property
    def is_podium(self):
        """Oyuncu ilk 3'te mi?"""
        return self.order <= 3
