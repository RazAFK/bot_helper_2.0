class DatabaseError(Exception):
    '''Базовое исключение для ошибок базы данных'''
    def __init__(self, message, field=None, value=None, details=None):
        self.message = message
        self.field = field
        self.value = value
        self.details = details or {}
        super().__init__(self.message)

class InsertValueError(DatabaseError):
    '''Исключение при неправильном вводе данных'''
    pass
