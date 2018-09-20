
def flatten(value, prefix=''):
    if isinstance(value, list):
        ret = {}
        for idx, e in enumerate(value):
            flattened = flatten(e, prefix='{}[{}]'.format(prefix, idx))
            ret.update(flattened)
        return ret
    if isinstance(value, dict):
        ret = {}
        for field, e in value.items():
            flattened = flatten(e, prefix='{}[{}]'.format(prefix, field))
            ret.update(flattened)
        return ret
    return {prefix: value}

