from datetime import datetime

__all__ = ['get_default_value']

types = {
    'str': "",
    'int': 0,
    'list': [],
    'dict': {},
    'bool': False,
    'float': 0.0,
    'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    'set': set(),
    'tuple': tuple()
}


def get_default_value(typing: str):
    typing = typing.lower()
    for type_key in types:
        if typing.find(type_key) != -1:
            return types[type_key]
    return None
