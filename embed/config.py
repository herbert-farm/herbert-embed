"""
@name   Config
@desc   File for containing the program configuration
"""

import logging
from collections import OrderedDict, namedtuple

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
    
GPIO = namedtuple('GPIO', ['type', 'num']) 

class GPIOConfig(Config):
    """GPIO configuration"""
    
    # TODO: CONVERT to pins = { 2 :  GPIO(type="pin", name=2, etc)}
    
    PIN_NUMBERS = PINS = OrderedDict({
        "lights/enable"         : GPIO(type="pin", num=2),
        "lights/red/enable"     : GPIO(type="pin", num=0),
        "lights/green/enable"   : GPIO(type="pin", num=1),
        "lights/blue/enable"    : GPIO(type="pin", num=4),
        "sensors/enable"        : GPIO(type="pin", num=3),
        "pump/enable"           : GPIO(type="pin", num=5),
        "fan/enable"            : GPIO(type="pin", num=6),
        "heat/enable"           : GPIO(type="pin", num=8)
    })
    PIN_NAMES = FRIENDLY_NAMES = {out.num:name for name, out in PINS.items() if out is not None}
    
    CHNL_NUMBERS = OrderedDict({
        "temp/front"        : GPIO(type="channel", num=0),
        "temp/middle"       : GPIO(type="channel", num=1),
        "temp/back"         : GPIO(type="other", num=2),
        "moist/m"           : GPIO(type="channel", num=2),
        "tank/level"        : GPIO(type="channel", num=3),
    })
    CHNL_NAMES = {out.num:name for name, out in CHNL_NUMBERS.items() if out is not None}
    
    FILENAME = 'gpio_states.json'    # filename to load/store state from

class CLI_Config(Config):
    """CLI configuration"""
    
    PS2 = "[gpio] "

class SystemConfig(Config):
    """Controller Configuration"""
    
    S_I_MAP = {
        "temp/front": "lights/enable",
        "temp/middle": "lights/enable"
    }
