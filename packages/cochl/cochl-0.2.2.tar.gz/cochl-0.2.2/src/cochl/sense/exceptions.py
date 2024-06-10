class CochlSenseException(BaseException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"{self.message} Please contact support@cochl.ai"
