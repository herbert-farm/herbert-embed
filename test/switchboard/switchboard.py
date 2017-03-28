
import curses
import signal    

from util import assert_to_false

def print_data(d):
    print(d)

# Set pins up for output
PINS = [False for n in range(27)]

@assert_to_false
def validate_cmd(chunks):
    """
    Checks raw string to see if it is a valid command.
    """
    
    # must not be an empty string
    assert len(chunks) > 0
    
    # must be one of the commands listed in COMMANDS
    pcmd = chunks[0].upper()
    
    # validator for 'SET'
    if pcmd == 'SET':
        
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
    """
    Return action from type of command
    """
    cmd = chunks[0].upper()
    if cmd in COMMANDS:
        # parse cmd
        
        return {
            "action" : cmd,
            "data": chunks[1:]
        }
    else:
        return False

# initialize globals

def print_pin(pin):
    print("Pin {:7} : {:3}".format(pin, PINS[pin]))

def set_pin(pin, val):
    print("Setting pin {} to {}...".format(pin, val))
    PINS[int(pin)] = val
    print_pin(int(pin))

def list_pins(*args):
    for i, pin in enumerate(PINS):
        print_pin(i)

def leave(*args):
    exit()

HANDLERS = {
    'SET'   : set_pin,
    'LIST'  : list_pins,
    'EXIT'  : leave
}

COMMANDS = set(HANDLERS.keys())

ps2 = "(gpio) $ " 

# main
def main():
    # create the screens
    # scr = curses.initscr()
    
    while True:
        # get command
        chunks = input(ps2).strip().split()
        
        if not validate_cmd(chunks):
            print("Invalid command.")
            continue
        
        cmd = parse_cmd(chunks)
        
        if not cmd:
            print("No such command exists.")
            continue
        
        HANDLERS.get(cmd["action"], print_data)(*cmd["data"])

# boilerplate
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
