

def flatten(l):
    for subl in l:
        for i in subl:
            yield i

def assert_to_false(fn):
    def func(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except AssertionError:
            return False
    return func

def caseless_compare(str_a, str_b):
    return str_a.casefold() == str_b.casefold()
