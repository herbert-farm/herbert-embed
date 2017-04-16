#!usr/bin/env python3
"""
"""

from collections import deque

from embed.gpio import Client
import signal

import sensor
import db
import utils

# The numbers of sensors in what area
SENSORS = {
    'MOIST-M'       : [
        sensor.Sensor.from_channel(0),
        sensor.Sensor.from_channel(1)
    ],
    'MOIST-F'       : [],
    'MOIST-L'       : [],
    'TEMP-M'        : [],
    'WATERLEVEL'    : [
        sensor.Sensor.from_pin(28)
    ]
}

DATA_QUEUES = { k : queue.Queue() for k in SENSORS.keys() }

INSTRUMENTS = {
    'FAN'   : [],
    'MOIST' : [],
    'LIGHT' : []
}

# which sensor values are modulated by which instrument
S_I_MAP = {
    'MOIST-M'   : 'MOIST',
    'MOIST-F'   : 'MOIST',
    'MOIST-L'   : 'MOIST',
    'TEMP-M'    : 'FAN',
}

# Main event loop
# 
# def main():
#     # connect to db
#     datastore = db.Database()
#     
#     # create sensor threads
#     controllers = {
#         name : sensor.Controller(name, sensors, DATA_QUEUES[name]) for name, sensors in SENSORS.items()
#         if len(SENSORS[name]) > 0 
#     }
#     
#     # create instrument threads
#     instruments = {
#         name : instrument.Controller(name, sensors, DATA_QUEUES[name]) for name, sensors in SENSORS.items()
#         if len(SENSORS[name]) > 0 
#     }
#     
#     # set up data listeners
#     for name, stream in DATA_QUEUES.items():
#         datastore.listen(stream)
#         # instruments[name].listen(stream)
#         
#     
#     print('ay2')
#     # start reading
#     for ctrl in controllers.values():
#         ctrl.start()
# 
#     # watch queue for > n readings per sensor
#     # TODO: figure out how to stream queue data in a non-blocking way
#     
#         
#     # wait for all threads to finish reading
#     signal.pause()
def main():
    
    t = 0
    while True:
        nt = time.time()
        d = nt - t
        
        # capture values from all pins/channels and put into deque
        
        # 
        
        # activate handlers based on time scale (ms, s, minute, hour, day)
        if d % 1 == 0:
            (handle(t) for handle in sec_handlers)
        
        if d % 60 == 0:
            (handle(t) for handle in sec_handlers)
        
        if d % 60 == 0:
            (handle(t) for handle in sec_handlers)
        
        # feed to controller, get outputs
        
        # dispatch outputs
        
        t = nt


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
