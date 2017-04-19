"""
@name   utils.py
@desc   File containing several common functions
"""

import uuid

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
    """
    Checks if two strings are equivalent, regardless of case
    
    @param      str     str_a       the first string to compare
    @param      str     str_b       the second string to compare
    @return     bool    True if the strings are equivalent, False o.w.
    """
    return str_a.casefold() == str_b.casefold()

def merge_dicts(*dicts):
    """
    Merges multiple dicts together, with later dicts taking priority.
    
    @param      dict        
    """
    ctx = {}
    for di in dicts:
        ctx.update(di)
    
    return ctx

def make_uuid():
    """
    Generate a simple four character uuid
    
    @return     str     a fairly unique uuid
    """
    return str(uuid.uuid4()).split('-')[-1]
