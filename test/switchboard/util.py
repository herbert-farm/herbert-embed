
def assert_to_false(fn):
    def func(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except AssertionError:
            return False
    return func
    
