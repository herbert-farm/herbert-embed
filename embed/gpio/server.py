"""
@name   GPIO Server
@desc   Multi-threaded server for atomically reading/writing RPI GPIO pins.

GPIO read/write requests are handled in separate threads. However, GPIO is
locked via semaphores, so rw is guaranteed to be atomic, and will take the value
of the operation on that pin, or default if none.

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import json
import logging
import threading
import socket
from time import time
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4 as uuid
from numbers import Real as REAL_NUMS

from . import actions
from . import sock
from .. import utils, config

if config.GPIOConfig.DEBUG:
    logging.basicConfig(
        level=config.GPIOConfig.LOG_LEVEL,
        format='%(asctime)s:%(levelname)s:GPIO/server:%(message)s'
    )

################################### GLOBALS ###################################

# pins & channels to use
# _PINS = map(lambda k, v: _PINS.items())
_PINS = list(
    filter(lambda v: v.num is not None, config.GPIOConfig.PINS.values())
)
_CHNLS = list(
    filter(lambda v: v.num is not None, config.GPIOConfig.CHNL_NUMBERS.values())
)

# pin and channel locks
PIN_LOX = {n.num : threading.Semaphore(1) for n in _PINS}
CHNL_LOX = {n.num : threading.Semaphore(1) for n in _CHNLS}
SAVEFILE_LOCK = threading.Semaphore(1)

try:                # on-rpi env
    import gpiozero
    
    # set up pins for binary output
    PINS = {gpio.num : gpiozero.LED(int(gpio.num)) for gpio in _PINS}
    # instantiate ADC for sensor channels
    CHNLS = {}
    for gpio in _CHNLS:
        if gpio.type == 'channel':
            CHNLS[gpio.num] = gpiozero.MCP3008(channel=gpio.num)
        elif gpio.type == 'pin':
            CHNLS[gpio.num] = gpiozero.Button(gpio.num)
        else:
            pass
except ImportError: # non-rpi env
    import random
    from . import stub

    PINS = {gpio.num : stub.Stub(gpio.num, 0) for gpio in _PINS}
    CHNLS = {}
    for gpio in _CHNLS:
        if gpio.type == 'channel':
            CHNLS[gpio.num] = stub.Stub(gpio.num, random.random())
        elif gpio.type == 'pin':
            CHNLS[gpio.num] = stub.Stub(gpio.num, random.random())
        else:
            pass
    
################################### HANDLERS ###################################

############################## HANDLERS/FUNCTIONS ##############################

def set_pin(pin, val):
    """
    Set the value of a pin.
    
    @pre        `pin` must be an non-negative integer
    @pre        `val` must be a 0 or 1
    
    @param      int     pin     the pin to set the value for
    @param      int     val     the value to set the pin to
    
    @return     dict    {pin : val} where `pin` is the pin number and `val` is
    the val that the GPIO pin is currently set to
    """
    pin_num = int(pin)
    pin = PINS.get(pin_num, None)
    
    if pin is None:
        msg = "{} is not a valid pin number.".format(pin_num)
        logging.error(msg)
        raise LookupError(msg)
    
    logging.info("Setting pin %s to %s...", pin_num, val)
    with PIN_LOX[pin_num]:
        try:
            PINS[pin_num].value = val
        except Exception as err:
            logging.error("`Error setting pin `%s` to `%s`", pin_num, val)
            return {pin_num: get_pin(pin_num)}
    
    return {pin_num : val}

def get_pin(pin):
    """
    Get the value of a single pin.
    
    @pre        `pin` must be an non-negative integer
    @pre        `val` must be a 0 or 1
    @post       fetches the value of the pin specified
    
    @raises     LookupError when the specified `pin_num` paramater is invalid
    
    @see        `doc/ipc.md` for more informaton on the structure of `action`
    
    @param      int     pin     the pin number to read from
    @return     dict    {pin : val} where `pin` is the pin number and `val` is
    the val that the GPIO pin is currently set to
    """
    pin_num = int(pin)
    pin = PINS.get(pin_num, None)
    
    if pin is None:
        msg = "{} is not a valid pin number".format(pin_num)
        logging.error(msg)
        raise LookupError(msg)
    
    val = None
    with PIN_LOX[pin_num]:
        val = pin.value
            
    return {pin_num : val}

def list_pins():
    """
    Get the value of all the pins.
    
    @see        `get_pin()` for the specific reading implementation
    @return     list        list of {pin:val} dicts
    """
    pin_stats = []
    
    for pin_num in PINS.keys():
        try:
            pin_stats.append(get_pin(pin_num))
        except LookupError:
            msg = "`get_pin()` raised LookupError when there should be none."
            logging.warning(msg)
            
    return pin_stats

def get_channel(channel):
    """
    Get the value of a single channel.
    
    @post       fetches the value of the channel specified
    
    @raises     LookupError when the specified `chnl_num` paramater is invalid
    
    @see        `doc/ipc.md` for more informaton on the structure of `action`
    
    @param      int     chnl        the channel number to read
    @return     dict    {chnl : val} where `chnl` is the chnl number and `val`
    is the val that the sensor channel is currently reading
    """
    chnl_num = int(channel)
    chnl = CHNLS.get(chnl_num, None)
    
    if chnl is None:
        msg = "{} is not a valid channel number".format(chnl_num)
        logging.error(msg)
        raise LookupError(msg)
    
    val = None
    with CHNL_LOX[chnl_num]:
        val = chnl.value
            
    return {chnl_num : val}

def list_channels():
    """
    Get the value of all the channels.
    
    @see        `get_chnl()` for the specific reading implementation
    @return     list        list of {pin:val} dicts
    """
    chnl_stats = []
    
    for chnl_num in CHNLS.keys():
        try:
            chnl_stats.append(get_channel(chnl_num))
        except LookupError:
            msg = "`get_channel()` raised LookupError when there should be none."
            logging.warning(msg)
            
    return chnl_stats

def echo(*args, **kwargs):
    """Echoes the given args and kwargs."""
    return {"args": args, "kwargs" : kwargs}

HANDLERS = {
    actions.Types.SET_PIN       : set_pin,
    actions.Types.GET_PIN       : get_pin,
    actions.Types.LIST_PINS     : list_pins,
    actions.Types.GET_CHNL      : get_channel,
    actions.Types.LIST_CNLS     : list_channels,
    "default"   : echo
}

COMMANDS = set(HANDLERS.keys())

############################## HANDLERS/VALIDATOR ##############################

@utils.assert_to_false
def valid_action(action):
    """
    Validates the given action object.
    """
    # action.type must exist, and be a valid string
    act_type = action.get('type', False)
    assert act_type is not False
    assert isinstance(act_type, str)
    assert act_type in COMMANDS
    
    # action.params must exist and be a dict
    act_params = action.get('params', False)
    assert act_params is not False
    assert isinstance(act_params, dict)
    
    if utils.caseless_compare(act_type, 'BSET'):
        # validator for 'BSET'
        # must have at least pin and val
        assert action.get('pin') is not None
        assert action.get('val') is not None
        
        # both must be numeric
        assert isinstance(action['pin'], REAL_NUMS) == isinstance(action['val'], REAL_NUMS)
        
        # pin number must be within range
        assert action['pin'] in _PINS
    elif utils.caseless_compare(act_type, 'LIST'):
        # validator for 'LIST'
        pass # none
    return True
    
############################### HANDLERS/MATCHER ###############################

def match_handler(act_type):
    """
    Returns and action handler based on the given action type `act_type`.
    
    If it cannot match a handler to the action type, it will fall back to the
    default handler, and if there is no default handler defined, it will raise a
    `KeyError`.
    
    @raises     KeyError    if cannot handle the given action type with a
    specified or default handler.
    
    @param      str     act_type        the action to handle
    @returns    func    the handler for the action
    """
    spec_handler = HANDLERS.get(act_type)
    def_handler = HANDLERS.get("default")
    
    if spec_handler is None:
        if def_handler is None:
            raise KeyError
        else:
            logging.warning("No handler for action.type: `%s`, using default.", act_type)
            return def_handler
    
    return spec_handler

#################################### SERVER ####################################

class Server(object):
    """
    Receives connections requests to access the GPIO, validates and acts upon them.
    
    @pre    networking lib must be initialized
    @pre    thread pool lib must be initialized
    
    @attr   dict    HANDLERS    dict containing valid commands and their
    respective handlers
    @attr   set     COMMANDS    set containing command names
    
    @method bool    valid_action(action)    Validates the given action object.
    @method None    handle(conn)            Parse, validate and dispatch a
    message from the connection.
    @method None    listen                  Continuously listens for new
    connections to the server at (addr, port).
    """
    
    fname = config.GPIOConfig.FILENAME
    
    @classmethod
    def from_file(cls, fname, addr=None, num_workers=None):
        """
        Initilazes the server with the given pin states.
        
        @param      dict    pin_states  
        """
        states = {n.num : 0 for n in _PINS}
        
        try:
            with open(fname, 'r') as file:
                data = json.load(file)
                states = utils.merge_dicts(*data["pins"])
        except OSError:
            # account for non-existent file
            logging.warning("Error opening: `%s`, creating file, starting \
server with zeroed GPIOs", fname)
            with open(fname, 'x') as file:
                pass
        except ValueError:
            # account for invalid in file
            logging.warning("Error deserializing GPIO states from `%s`, \
starting server with zeroed GPIOs", fname)
        
        return Server.from_state(states, addr=addr, num_workers=num_workers)
    
    @classmethod
    def from_state(cls, pin_states, addr=None, num_workers=None, fname=None):
        """
        Initilazes the server with the given pin states.
        
        @param      dict    pin_states  
        """
        for pin, state in pin_states.items():
            set_pin(pin, state)
        
        return Server(addr=addr, num_workers=num_workers, fname=fname)
    
    def __init__(self, addr=None, num_workers=None, fname=None):
        """
        Constructor for the Server class.
        
        @param      str     addr        the adress to bind the server to
        @param      int     num_workers the number of threads to create
        @return     Server  the GPIO server object
        """
        # savefile config
        self.fname = fname if fname else self.fname
        
        # network config
        self.addr = addr if addr else config.NetworkConfig.HOST
        self.num_workers = num_workers if num_workers else config.NetworkConfig.MAX_THREADS
        self.encoding = config.NetworkConfig.ENCODING
        
        # creating sockets
        self.sock = sock.Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socks = {}
        
        # create thread pool
        self.workers = ThreadPoolExecutor(max_workers=self.num_workers)
        
        # save initial state
        self.save_state()
    
    def save_state(self):
        """
        Saves the state of the GPIO to disk in the filename specified at construction.
        
        @post       the state of the GPIO will be saved to the disk. If the file
        does not exist, it will be created.
        
        @returns    None
        """
        try:
            with SAVEFILE_LOCK:
                with open(self.fname, 'w') as file:
                    json.dump({"timestamp" : time(), "pins" : list_pins()}, file)
        except OSError as err:
            # account for incorrect file
            logging.warning("Error writing GPIO states to file `%s`", self.fname)
            print(err)
    
    def handle(self, conn, _id):
        """
        Parse, validate and dispatch a message from the connection.
        
        @pre        the socket `conn` must be open and initialized
        @post       the socket will be closed
        
        @param      socket.socket       conn        the socket object
        @return     None
        """
        with conn:
            # receive full transmission
            chunks = conn.recv(1024)
            if not chunks:
                return
            
            # parse
            try:
                raw = str(chunks, self.encoding)
                action = json.loads(raw)
                logging.info("received: %s", action)
            except ValueError:
                logging.error("Error deserializing action: %s", raw)
                return
            
            # validate
            if not valid_action(action):
                logging.error("Invalid command: '%s'", action['type'])
                return
            
            # dispatch
            try:
                # match and execute
                resp = match_handler(action["type"])(**action["params"])
                
                self.save_state()
                
                # respond
                resp = {"ok" : True, "data": resp}
            except KeyError:
                resp = {
                    "ok" : False,
                    "error": {"message" : "Could not match command to handler."}
                }
                logging.error("Could not match command `%s` to handler", action['type'])
            except Exception as err:
                resp = {
                    "ok" : False,
                    "error": {"message" : "Error handling command."}
                }
                logging.error("Error handling command `%s`: %s", action['type'], err)
                
            logging.info("responded: %s", resp)
            conn.sendall(bytes(json.dumps(resp), self.encoding))
            
            conn.shutdown(socket.SHUT_RDWR)
            
            # cleanup
            del self.socks[_id]
                
    def listen(self, port=None):
        """
        Continuously listens for new connections to the server at (addr, port).
        
        @param      int     port        the port to for the server listen on
        @return     None
        """
        port = port if port else config.NetworkConfig.PORT
        with self.sock:
            self.sock.bind((self.addr, port))
            self.sock.listen(5)
            
            logging.info("listening at %s:%d", self.addr, port)
            
            while True:
                conn, _ = self.sock.accept()
                if conn:
                    _id = str(uuid()).split('-')[-1]
                    self.workers.submit(self.handle, conn, _id)
                    self.socks[_id] = conn
