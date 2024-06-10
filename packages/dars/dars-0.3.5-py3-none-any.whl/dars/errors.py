'''Классы ошибок'''


class Error(Exception):
    '''Базовая ошибка программы'''


class EisClientError(Error):
    '''Ошибка при взаимодействии с СОИ ЕИС'''


class EisClientUnexpectedStatus(EisClientError):
    '''СОИ ЕИС вернул неожиданный статус'''
    def __init__(self, code: int):
        self.code = code

    def __str__(self):
        return f'СОИ вернул неожиданный статус {self.code}'
