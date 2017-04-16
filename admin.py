"""
@name   GPIO Admin Client
@desc   Basic program for managing the RPi3 GPIO

@author Joshua Paul A. Chan (@joshpaulchan)
"""

from embed.gpio import Client
from embed import config, utils

PINS = config.GPIOConfig.PINS.values()
CHNLS = config.GPIOConfig.CHNL_NUMBERS.values()
PIN_NAMES = config.GPIOConfig.FRIENDLY_NAMES
CHNL_NAMES = config.GPIOConfig.CHNL_NAMES
VALID_COMMANDS = set(['SET', 'GET', 'LIST', 'HELP', 'EXIT'])

@utils.assert_to_false
def valid_cmd(chunks):
    """
    Checks raw string to see if it is a valid command.
    """
    # must not be an empty string
    assert len(chunks) > 0
    # must be one of the commands listed in COMMANDS
    pcmd = chunks[0]
    
    if utils.caseless_compare(pcmd, 'SET'):
        # validator for 'SET'
        # must have at least 2 arguments
        assert len(chunks) >= 3
        # pin must be numeric
        assert chunks[1].isnumeric() and chunks[2].isnumeric()
        # pin number must be within range
        assert int(chunks[1]) in PINS
    elif utils.caseless_compare(pcmd, 'GET'):
        # validator for 'GET'
        # must have at least 2 arguments (pin or channel) and specifier
        assert len(chunks) >= 3
        
        # first arg (pin/channel) must be alpha, and either 'p' or 'c'
        assert chunks[1].isalpha() and chunks[1] in ('p'.casefold(), 'c'.casefold())
        
        # pin/channel specifier must be numeric
        assert chunks[2].isnumeric()
        if utils.caseless_compare(chunks[1], 'p'):
            # pin number must be within range
            assert int(chunks[1]) in PINS
        elif utils.caseless_compare(chunks[1], 'c'):
            # channel number must be within range
            assert int(chunks[1]) in CHNLS
    elif utils.caseless_compare(pcmd, 'LIST'):
        # validator for 'LIST'
        # must have at least 1 arg
        assert len(chunks) >= 2
        
        # arg (pin/channel) must be alpha, and either 'p' or 'c'
        assert chunks[1].isalpha() and chunks[1] in ('p'.casefold(), 'c'.casefold())
    elif utils.caseless_compare(pcmd, 'HELP'):
        # validator for 'HELP'
        # no args needed
        pass
    elif utils.caseless_compare(pcmd, 'EXIT'):
        # validator for  'EXIT'
        # no args needed
        pass
    elif pcmd not in VALID_COMMANDS:
        # validate all other commands in VALID_COMMANDS
        return False
    return True

def parse_cmd(chunks):
    """Return action from type of command."""
    cmd = chunks[0]
    action = {"type" : cmd}
    
    if utils.caseless_compare(cmd, 'SET'):
        # parse pin and val
        action['pin'] = int(chunks[1])
        action['val'] = int(chunks[2])
    elif utils.caseless_compare(cmd, 'LIST'):
        # parse which to list, 'p' for pins or 'c' for channels
        action['which'] = chunks[1]
    return action
    
# main
def main():
    """main boilerplate"""
    # initialize client
    ps2 = config.CLI_Config.PS2
    client = Client()
    
    while True:
        # get command
        pcmd = input(ps2).strip().split(' ')
        
        # if valid command
        if not valid_cmd(pcmd):
            print("Nah. Type 'HELP' to see a list of possible commands.")
            continue
            
        action = parse_cmd(pcmd)
        act_type = action['type']
        
        if utils.caseless_compare(act_type, 'SET'):
            pin = action['pin']
            val = action['val']
            
            try:
                res = client.set_pin(pin, val)
                if res:
                    print("'{}' (pin #{}) is now: {}".format(PIN_NAMES[pin], pin, val))
            except:
                print("Error setting pin #{} to {}.".format(pin, val))
        elif utils.caseless_compare(act_type, 'LIST'):
            which = action['which']
            
            if which == 'p':
                pins = client.get_pins()
                for pin, val in pins.items():
                    name = PIN_NAMES[int(pin)]
                    print("{:20} (pin #{:0>2}): {}".format(name, pin, val))
            elif which == 'c':
                channels = client.get_channels()
                for channel, val in channels.items():
                    name = CHNL_NAMES[int(channel)]
                    print("{:20} (channel #{:0>2}): {}".format(name, channel, val))
            else:
                print("No such listing `{}` available.".format(which))
                
        elif utils.caseless_compare(act_type, 'HELP'):
            print("Valid commands: " + ','.join(map("'{}'".format, VALID_COMMANDS)))
                
        elif utils.caseless_compare(act_type, 'EXIT'):
            # let em off easy
            print("Have a nice day!")
            exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
