import shlex

def str2dict(s: str, fields: list | None = None) -> dict:
    
    d=dict()

    for elem in shlex.split(s):
        key, value = elem.split('=')
        if fields is None or key in fields:
            d[key] = fields[key](value)

    return d

