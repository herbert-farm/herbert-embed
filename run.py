#!/usr/bin/env python3
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
    # turn everything off
    turn_white_lights_off()
    turn_other_lights_ff()
    turn_pump_off()
    
    # sleep for 6 hours
    sleep(60*60*6)

def turn_white_lights_on():
    """Turns white lights on"""
    pass

def turn_white_lights_off():
    """Turn white lights off"""
    pass

def turn_other_lights_on():
    """Turns the other lights on"""
    pass

def turn_other_lights_off():
    """Turns the other lights off"""
    pass

def turn_pump_on():
    """Turn the pump on"""
    pass

def turn_pump_off():
    """Turn pump off"""
    pass

def at_zero():
    """At 00:00"""
    sleep_for_6_hours()

def at_six():
    """At 06:00"""
    turn_white_lights_on()
    
def at_eight():
    """At 08:00"""
    turn_white_lights_off()
    turn_other_lights_on()

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
    schedule.every().day.at("00:00").do(at_zero)
    schedule.every().day.at("6:00").do(at_six)
    schedule.every().day.at("8:00").do(at_eight)
    
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
