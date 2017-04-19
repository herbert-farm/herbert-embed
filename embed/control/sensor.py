"""
@name   sensory.py
@desc   Defines a sensor class to use the 
"""

import functools

from embed.gpio import Client

CLIENT = Client()

class Sensor(object):
    """
    Sensor class
    """
    def __init__(self, channel=None, pin=None):
        """
        """
        self.read_fn = None
        
        if channel is not None:
            self.chnl = channel
            self.read_fn = functools.partial(CLIENT.get_channel, channel)
        
        if pin is not None:
            self.pin = pin
            self.read_fn = functools.partial(CLIENT.get_pin, pin)
        
        assert self.read_fn is not None

    def read(self):
        """
        Reads a value from the attached gpio device.
        
        @return     number      the value from the gpio device
        """
        return self.read_fn()
