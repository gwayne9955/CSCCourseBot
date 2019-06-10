

def group_by(iterable, key):
    return assoc(iterable, key=key, value=lambda x: x)


def assoc(iterable, key, value):
    result = {}
    for item in iterable:
        k, v = key(item), value(item)
        if k not in result:
            result[k] = []
        result[k].append(v)
    return result
