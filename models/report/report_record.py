from models import db
from enums.enum_record_status import RecordStatus

class ReportRecord(db.Model):
    __tablename__ = 'report_record'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(RecordStatus), nullable=False)
    created_date = db.Column(db.DateTime)

    reported_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    reported_player = db.relationship('Player', back_populates='reported_reports', foreign_keys=[reported_player_id])

    reporting_by_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    reporting_by_player = db.relationship('Player', back_populates='reporting_reports', foreign_keys=[reporting_by_player_id])

    reviewer_moderator_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    reviewer_moderator = db.relationship('Player', back_populates='reviewed_reports', foreign_keys=[reviewer_moderator_id])
