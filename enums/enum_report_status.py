from enum import Enum

class ReportStatus(Enum):
    Pending = "Pending"
    Reviewed = "Reviewed"
    Rejected = "Rejected"
    Penalty = "Penalty"