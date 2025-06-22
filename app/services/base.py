class ServiceResponse:
    def __init__(self, success, data=None, message=None, error=None):
        self.success = success
        self.data = data
        self.message = message
        self.error = error

    def to_dict(self):
        return {
            'success': self.success,
            'data': self.data,
            'message': self.message,
            'error': self.error
        }

class BaseService:
    def __init__(self, db):
        self.db = db
