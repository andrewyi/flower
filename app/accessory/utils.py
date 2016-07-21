# coding: utf-8

def make_random_str(length):
    import random, string
    return ''.join([random.choice(string.ascii_letters) \
            for i in range(length)])


def to_int(o, d=0):
    if o is None:
        return d
    try:
        i = int(o)
    except (TypeError, ValueError):
        return d
    return i
