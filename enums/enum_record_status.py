from enum import Enum

class RecordStatus(Enum):
    Pending = "Pending"
    Reviewed = "Reviewed"
    Rejected = "Rejected"
    Penalty = "Penalty"