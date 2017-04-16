"""
@name   Stub
@desc   GPIO Stubs for use with testing the GPIO library in non-RPI environments
"""

class Stub(object):
    """Stub"""
    
    def __init__(self, pin, val):
        self.pin = pin
        self.value = val
