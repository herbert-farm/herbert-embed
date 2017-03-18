#!usr/bin/env python3

import signal
import queue

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

def make_controller(name, sensors, q):
    return sensor.Controller(name, sensors, q)

# Main event loop
# 
def main():
    # connect to db
    datastore = db.Database()
    
    # create controller threads
    controllers = {
        name : make_controller(name, sensors, DATA_QUEUES[name]) for name, sensors in SENSORS.items()
        if len(SENSORS[name]) > 0 
    }
    
    # set up data listeners
    for stream in DATA_QUEUES.values():
        datastore.listen(stream)
    
    print('ay2')
    # start reading
    for ctrl in controllers.values():
        ctrl.start()
        
        
    print('ay3')
    # watch queue for > n readings per sensor
    # TODO: figure out how to stream queue data in a non-blocking way
    
        
    # wait for all threads to finish reading
    signal.pause()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
