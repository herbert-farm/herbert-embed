#!usr/bin/env python3
"""
@name   run
@desc   Nice
"""

from time import sleep
from collections import deque

import schedule

from embed import config
from embed.control import Sensor, InstrumentController
from embed.control import NaiveSystem

# import db
INPUTS = config.GPIOConfig.CHNL_NUMBERS
OUTPUTS = config.GPIOConfig.PIN_NUMBERS

# maps sensor inputs to relevant instrument outputs
S_I_MAP = config.SystemConfig.S_I_MAP

DQ = {k : deque(maxlen=100) for k in INPUTS.keys()}

def sleep_for_6_hours():
    """System sleeps from 12AM-6AM"""
    sleep()

def turn_white_lights_on():
    """Turns white lights on"""
    pass

def main_naive():
    """main boilerplate"""
    
    # instantiate inputs
    sensors = {}
    for input_name, gpio in INPUTS.items():
        if gpio.type == 'channel':
            sensors[input_name] = Sensor(channel=gpio.num)
        elif gpio.type == 'pin':
            sensors[input_name] = Sensor(pin=gpio.num)
    
    # instantiate outputs
    instruments = {name: InstrumentController(pin=gpio.num) for name, gpio in OUTPUTS.items()}
    
    # instantiate controllers
    controller = NaiveSystem(io_map=S_I_MAP)
    
    # schedule jobs
    schedule.every().day.at("00:00").do(sleep_for_6_hours)
    schedule.every().day.at("6:00").do(sleep_for_6_hours)
    schedule.every().day.at("8:00").do(sleep_for_6_hours)
    
    while True:
        
        # capture values from all pins/channels and put into deque
        inputs = {}
        for name, sense in sensors.items():
            inputs[name] = sense.read() 
        # `inputs` will be dict of of "input/name": num or num[].
        
        print("inputs", inputs)
        # TODO: save inputs
        
        # activate handlers based on time scale (ms, s, minute, hour, day)
        schedule.run_pending()
        
        # predict output for inputs
        outputs = controller.predict(inputs)
        
        print("outputs", outputs)
        
        # dispatch outputs
        for inst_name, val in outputs.items():
            if instruments.get(inst_name, False):
                instruments[inst_name].run(val)
            
        sleep(5)

if __name__ == '__main__':
    try:
        main_naive()
    except KeyboardInterrupt:
        exit()
