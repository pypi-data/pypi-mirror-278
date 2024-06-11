from datetime import datetime


def truncate_string(s: str, size: int, suffix: str = '...') -> str:
    '''Образать строу до заданного размера и добавить суффикс'''
    if not s:
        return s
    if len(s) > size:
        return s[:size] + '...'
    return s


def isonow():
    '''Текщая дата и время в формате iso-8601 с часовым поясом'''
    return datetime.now().astimezone().isoformat()


def humanize_size(num, suffix='B'):
    '''Человекочитаемый размер в байтах

    См. https://stackoverflow.com/a/15485265
    '''
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f'{num:3.1f} {unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f} Yi{suffix}'
