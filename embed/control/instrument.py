"""
@name   instrument.py
@desc   Defines the Instrument and InstrumentController classes
"""

import logging
import threading
from time import sleep

from embed.gpio import Client

CLIENT = Client()

class Instrument(object):
    """
    Instrument class
    """
    def __init__(self, pin=None):
        """
        """
        assert pin is not None
        
        self.run_lock = threading.Semaphore()
        self.pin = pin
        self.device = CLIENT
        
    def turn_on(self):
        """
        Turns on the attached gpio device.
        
        @return     dict        the 
        """
        return self.device.set_pin(self.pin, 1)
    
    def turn_off(self):
        """
        Turns off the attached gpio device.
        
        @return     number      the value from the gpio device
        """
        return self.device.set_pin(self.pin, 0)
    
    def turn_on_for(self, interval=1):
        """
        Turns on the gpio device, waits for the specified number of seconds,
        then turns the gpio device off.
        
        @return     None
        """
        assert interval > 0
        
        with self.run_lock:
            logging.info("Turning on pin %s for %s seconds", self.pin, interval)
            self.turn_on()
            sleep(interval)
            self.turn_off()

class InstrumentController(object):
    """
    The
    """

    def __init__(self, pin, interval=1):
        """
        Constructor for the InstrumentController
        """
        assert interval > 0
        
        self.interval = interval
        self.running = False
        self.gpio = Instrument(pin)
        
    def run(self, interval=None):
        """
        Activates the instrument output for the given time interval in a separate thread
        
        @param      number      interval        The number of seconds to wait
        """
        if interval is None:
            interval = 1
        
        worker = threading.Thread(
            target=self.gpio.turn_on_for,
            kwargs={'interval':interval}
        )
        worker.start()
