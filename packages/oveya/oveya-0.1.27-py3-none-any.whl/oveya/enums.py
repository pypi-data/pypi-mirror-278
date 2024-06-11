

class RequestMethod:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'

    @classmethod
    def to_list(cls):
        return [cls.GET, cls.POST, cls.PUT, cls.DELETE, cls.OPTIONS]
