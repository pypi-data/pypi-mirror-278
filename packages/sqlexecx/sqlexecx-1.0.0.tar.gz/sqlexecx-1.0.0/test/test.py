from typing import Collection, Sequence, Union

t = ('1', '2')
print(isinstance(t, Collection), isinstance(t, Sequence))
# True True
l = ['1', '2']
print(isinstance(l, Collection), isinstance(l, Sequence))
# True True
s = set(l)
print(isinstance(s, Collection), isinstance(s, Sequence))
# True False
s = 'hello'
print(isinstance(s, Collection), isinstance(s, Sequence))
# True True


def get_dialect_str(src: Union[str, Collection[str]]):
    return src.strip() if isinstance(src, str) else ','.join([s.strip() for s in src])


def _dialect_str(src: str):
    assert isinstance(src, str), 'source must be a string.'
    if ',' in src:
        return ','.join(['`{}`'.format(s.strip()) for s in src.split(',')])
    elif '(' in src:
        return src.strip()
    else:
        return '`{}`'.format(src.strip())


def get_mysql_dialect_str(src: Union[str, Collection[str]]):
    assert src, 'src string is required.'
    if isinstance(src, str):
        return _dialect_str(src)
    return ','.join([_dialect_str(arg) for arg in src])


if __name__ == '__main__':
    # names = 'person'
    names = ['id', 'name, age']
    print(get_dialect_str(names))
    print(get_mysql_dialect_str(names))
