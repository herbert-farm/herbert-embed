
import threading
import uuid

import time
import sched
import random

SCHEDULER = sched.scheduler()

class Instrument(object):
    
    def __init__(self, p=None):
        pass
    
    # Reads a value from the given sensor
    # 
    # 
    def read(self):
        return random.random()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        return None
    
    @classmethod
    def from_pin(cls, pin_number):
        # TODO: create sensor from digital pin
        p = None
        return Instrument(p=p)

class Controller(threading.Thread):
    
    def __init__(self, name, sensors, q, delay=1):
        threading.Thread.__init__(self)
        self.thread_id = str(uuid.uuid4()).split('-')[-1]
        self.name = name
        self.sensors = sensors
        self.q = q
        
        self.delay = delay
        
        self.exit = False
        self.pause = False
    
    def read(self):
        readings = []
        for sense in self.sensors:
            
            with sense as sen:
                readings.append(sen.read())
        
        self.q.put({
            "id"    : self.thread_id,
            "name"  : self.name,
            "data"  : readings
        })
        # print("{:1f}  {:8}  {:15}  {}".format(time.time(), self.thread_id, self.name, readings))
        
        return readings
    
    # Reads a value from the given sensor and places it in the data queue.
    # 
    # @return   None
    def run(self):
        self.event = SCHEDULER.enter(self.delay, 1, self.read)
        
        # # # Look for exit flag
        while not self.exit:
            if not self.pause:
                reading = self.read()
                time.sleep(self.delay)
    
    def stop(self):
        SCHEDULER.cancel(self.event)
        
