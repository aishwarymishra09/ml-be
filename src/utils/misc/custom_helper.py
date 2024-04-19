
class Response:
    def __init__(self, message, status_code,success, data, error=None):
        self.message = message
        self.status_code = status_code
        self.success = success
        self.data = data
        self.error = error

    def response(self):
        return {"message": self.message, "success": self.success,"data":self.data, "error": self.error}