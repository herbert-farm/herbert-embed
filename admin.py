"""
@name   GPIO Admin Client
@desc   Basic program for managing the RPi3 GPIO

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import curses

from embed.gpio import Client
from embed import config, utils

PINS = config.GPIOConfig.PINS.values()
NAMES = config.GPIOConfig.FRIENDLY_NAMES
VALID_COMMANDS = set(['BSET', 'LIST', 'HELP', 'EXIT'])

@utils.assert_to_false
def valid_cmd(chunks):
    """
    Checks raw string to see if it is a valid command.
    """
    # must not be an empty string
    assert len(chunks) > 0
    # must be one of the commands listed in COMMANDS
    pcmd = chunks[0]
    
    print(pcmd)
    if utils.caseless_compare(pcmd, 'BSET'):
        # validator for 'SET'
        # must have at least 2 arguments
        assert len(chunks) >= 3
        # both must be numeric
        assert chunks[1].isnumeric() and chunks[2].isnumeric()
        # pin number must be within range
        assert int(chunks[1]) in PINS
        return True
    elif utils.caseless_compare(pcmd, 'LIST'):
        # validator for 'LIST'
        # no args needed
        return True
    elif utils.caseless_compare(pcmd, 'HELP'):
        # validator for 'HELP'
        return True
    elif utils.caseless_compare(pcmd, 'EXIT'):
        # validator for  'EXIT'
        return True
    elif pcmd in VALID_COMMANDS:
        # validate all other commands in VALID_COMMANDS
        return True
    return False

def parse_cmd(chunks):
    """Return action from type of command."""
    cmd = chunks[0]
    action = {"type" : cmd}
    
    if utils.caseless_compare(cmd, 'BSET'):
        action['pin'] = int(chunks[1])
        action['val'] = int(chunks[2])
    
    return action
    
# main
def main():
    """
    """
    # TODO: create the screens
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
        if utils.caseless_compare(action['type'], 'BSET'):
            pin = action['pin']
            val = action['val']
            
            try:
                res = client.set(pin, val)
                print("'{}' (pin #{}) is now: {}".format(NAMES[pin], pin, val))
            except:
                print("Error setting pin #{} to {}.".format(pin, val))
        elif utils.caseless_compare(action['type'], 'LIST'):
            res = client.get_all()
            
            for pin, val in res['pins'].items():
                print("{:20} (pin #{:0>2}): {}".format(NAMES[int(pin)], pin, val))
                
        elif utils.caseless_compare(action['type'], 'HELP'):
            print("Valid commands: " + ','.join(map("'{}'".format, VALID_COMMANDS)))
                
        elif utils.caseless_compare(action['type'], 'EXIT'):
            # let em off easy
            print("Have a nice day!")
            exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
