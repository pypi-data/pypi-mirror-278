class InputError(Exception):

    def __init__(self, obj, message=None):
        self.obj = obj
        self.message = message
        

class Failure(Exception):

    def __init__(self, reason: str):
        self.reason = reason

class AlreadyExist(Exception):

    def __init__(self, obj: str, reason: str | None = None):
        self.obj = obj
        self.reason = reason

class NotAllowed(Exception):

    def __init__(self, reason):
        self.reason = reason
