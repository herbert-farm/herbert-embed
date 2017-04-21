"""
@name   utils.py
@desc   File containing several common functions
"""

import uuid

def flatten(_list):
    """
    Allows iteration over a 2 dimensional list
    
    @param      list            l       the 2-dimensional list to flatten
    @return     generator       generator yielding the flattened values
    """
    for subl in _list:
        for i in subl:
            yield i

def assert_to_false(func):
    """
    Decorator that stifles Assertion errors by returning the output if it 
    succeeds and returing False is an AssertionError is raised
    
    @param      function        func        the function to wrap
    @return     function        the wrapped function
    """
    def funct(*args, **kwargs):
        """Wrapper function"""
        try:
            return func(*args, **kwargs)
        except AssertionError:
            return False
    return funct

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
    
    @param      dict[]      dicts       the dicts to merge
    @return     dict        the merge dict               
    """
    ctx = {}
    for _dict in dicts:
        ctx.update(_dict)
    
    return ctx

def make_uuid():
    """
    Generate a simple four character uuid
    
    @return     str     a fairly unique uuid
    """
    return str(uuid.uuid4()).split('-')[-1]
