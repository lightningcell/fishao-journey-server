from models import db

class ReportRecord(db.Model):
    __tablename__ = 'report_record'
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('OPEN', 'IN_PROGRESS', 'RESOLVED', 'REJECTED', name='report_status_enum'), nullable=False)
