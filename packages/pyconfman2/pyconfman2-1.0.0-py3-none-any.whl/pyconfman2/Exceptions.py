class InvalidPropertyError(Exception):
    def __init__(self, message="Invalid property."):
        self.message = message
        super().__init__(self.message)

class EmptyValueProperty(Exception):
    def __init__(self, message="Value cannot be empty or None."):
        self.message = message
        super().__init__(self.message)

class KeyExistsError(Exception):
    def __init__(self, message="Key already exists."):
        self.message = message
        super().__init__(self.message)