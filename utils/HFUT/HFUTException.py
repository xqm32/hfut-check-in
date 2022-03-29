class LoginError(Exception):
    def __init__(self, what):
        super().__init__(what)


class CheckInError(Exception):
    def __init__(self, what):
        super().__init__(what)
