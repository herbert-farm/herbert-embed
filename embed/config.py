"""
@name   Config
@desc   File for containing the program configuration
"""

import logging
from collections import OrderedDict

class Config(object):
    """Global Config"""
    
    DEBUG = True
    
    # loggin
    LOG_FILE = "herbert.log"
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(levelname)s:%(message)s'

class NetworkConfig(Config):
    """Networking configuration"""
    
    HOST = 'localhost'
    PORT = 50007
    ENCODING = 'utf-8'
    
    MAX_THREADS = 5

class GPIOConfig(Config):
    """GPIO configuration"""
    
    # TODO: change from PINS to PIN_NUMBERS and FRIENDLY_NAMES to PIN_NAME
    PINS = OrderedDict({
        "lights/enable"     : 2,
        "lights/red"        : None,
        "lights/green"      : None,
        "lights/blue"       : None,
        "sensors/enable"    : 3,
        "pump/enable"       : 5,
        "fan/enable"        : 6
    })
    FRIENDLY_NAMES = {out:name for name, out in PINS.items() if out is not None}
    
    CHNL_NUMBERS = OrderedDict({
        "temp/front"        : 0,
        "temp/middle"       : 1
    })
    CHNL_NAMES = {out:name for name, out in CHNL_NUMBERS.items() if out is not None}
    
    FILENAME = 'gpio_states.json'    # filename to load/store state from

class CLI_Config(Config):
    """CLI configuration"""
    
    PS2 = "[gpio] "
