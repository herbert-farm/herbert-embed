"""
@name   GPIO Admin Client
@desc   Basic program for managing the RPi3 GPIO

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import gpio
import curses
import signal
import utils
from .. import config

NAMES = config.GPIOConfig.FRIENDLY_NAMES
VALID_COMMANDS = set('BSET', 'LIST', 'HELP', 'EXIT')

@utils.assert_to_false
def valid_cmd(chunks):
    """
    Checks raw string to see if it is a valid command.
    """
    # must not be an empty string
    assert len(chunks) > 0
    # must be one of the commands listed in COMMANDS
    pcmd = chunks[0].upper()
    # validator for 'SET'
    if pcmd == 'BSET':
        # must have at least 2 arguments
        assert len(chunks) >= 3
        # both must be numeric
        assert chunks[1].isnumeric() and chunks[2].isnumeric()
        # pin number must be within range
        assert 0 <= int(chunks[1]) <= len(PINS)
        return True
    # validator for 'LIST'
    if pcmd == 'LIST':
        # no args needed
        return True
    # validate all other commands in COMMANDS
    if pcmd in COMMANDS:
        return True
    return False

def parse_cmd(chunks):
    """Return action from type of command."""
    cmd = chunks[0].upper()
    if cmd in COMMANDS:
        # parse cmd
        
        return {
            "action" : cmd,
            "data": chunks[1:]
        }
    else:
        return False

# main
def main():
    """
    """
    # TODO: create the screens
    # initialize client
    ps2 = config.CLI_Config.PS2
    client = gpio.client.Client()
    
    while True:
        # get command
        pcmd = input(ps2).strip()
        
        # if valid command
        if not valid_cmd(pcmd):
            print("Nah. Type 'HELP' to see a list of possible commands.")
            continue
            
        action = parse_cmd(pcmd)
        if action['type'] == 'BSET':
            
            res = client.set(action['pin'], action['val'])
            pin = action['pin']
            val = action['val']
            
            if res is True:
                print("{} (pin #{}) is now: {}".format(NAMES[pin], pin, val))
            else:
                print("Error setting pin #{} to {}.".format(pin, val))
        elif action['type'] == 'LIST':
            # TODO: display human-readable (i.e. FAN), pin outs, and values
            res = client.get_all()
            
            print("\n".join(res['pins']))
        elif action['type'] == 'HELP':
            # TODO: print out the possible commands
            res = ''
            print(res)
        elif action['type'] == 'EXIT':
            # let em off easy
            print("Have a nice day!")
            exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
