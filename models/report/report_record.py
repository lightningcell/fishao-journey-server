from models import db
from enums.enum_record_status import RecordStatus

class ReportRecord(db.Model):
    __tablename__ = 'report_record'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(RecordStatus), nullable=False)
