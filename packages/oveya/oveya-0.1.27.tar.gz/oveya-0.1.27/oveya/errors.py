class VaulError(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'error': self.message}


class InvalidRequestError(VaulError):
    def __init__(self, message: str):
        super().__init__(400, message)


class InternalServerError(VaulError):
    def __init__(self, message: str):
        super().__init__(500, message)
