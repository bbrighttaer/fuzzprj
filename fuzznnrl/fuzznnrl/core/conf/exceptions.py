class AppConstantsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class OutputCodeError(Exception):
    def __init__(self, message):
        super().__init__(message)
