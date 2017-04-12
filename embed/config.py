"""
@name   Config
@desc   File for containing the program configuration
"""

class Config(object):
    """Global Config"""
    
    pass

class NetworkConfig(Config):
    """Networking configuration"""
    
    HOST = 'localhost'
    PORT = 50007
    ENCODING = 'utf-8'
    
    MAX_THREADS = 5

class GPIOConfig(Config):
    """GPIO configuration"""
    
    PINS = {
        "lights/enable"     : 2,
        "lights/red"        : None,
        "lights/green"      : None,
        "lights/blue"       : None,
        "sensors/enable"    : 3,
        "pump/enable"       : 5,
        "fan/enable"        : 6
    }
    
    FRIENDLY_NAMES = {out:name for name, out in PINS.items() if out}

class CLI_Config(Config):
    """CLI configuration"""
    
    CMD = {
        'LIST'  : 0,
        'BSET'  : 1,
        'HELP'  : 2,
        'EXIT'  : 7
    }
    
    PS2 = "[gpio] "
