class EscPressedError(Exception):

    def __init__(self, message="User terminated the execution"):
        self.message = message
        super().__init__(self.message)
