"""
@name   GPIO Server
@desc   Multi-threaded server for atomically reading/writing RPI GPIO pins.

GPIO read/write requests are handled in separate threads. However, GPIO is
locked via semaphores, so rw is guaranteed to be atomic, and will take the value
of the operation on that pin, or default if none.

@author Joshua Paul A. Chan (@joshpaulchan)
"""

from numbers import Real as REAL_NUMS
import json
import logging
import threading
import concurrent.futures
import socket

import sock

# FIXME: relative imports
from .. import utils
from embed import config, utils
from .. import config

################################### GLOBALS ###################################

# pins to use
_PINS = filter(any, config.GPIOConfig.PINS.values())

# pin locks
LOCKS = {n : threading.Semaphore(1) for n in _PINS}

# Set pins up for output
try:                # on-rpi env
    import gpiozero
    PINS = {n : gpiozero.LED() for n in _PINS}
    
except ImportError: # non-rpi env
    class OutputStub(object):
        
        def __init__(self, pin, val):
            self.pin = pin
            self.value = val

    PINS = {n : OutputStub(n, 0) for n in _PINS}
    
################################### HANDLERS ###################################

def set_pin(action):
    """
    Set the value of a pin.
    
    @pre        `pin` must be an non-negative integer
    @pre        `val` must be a 0 or 1
    
    @param      int     pin     the pin to set the value for
    @param      int     val     the value to set the pin to
    @return     bool    True if the operation succeeded, False otherwise
    """
    pin = action['pin']
    val = action['val']
    print("Setting pin {} to {}...".format(pin, val))
    
    with LOCKS[pin]:
        PINS[pin].value = val
    
    return True

def list_pins(action):
    """
    Get the value of all the pins.
    
    ex.
    >>> gpio.get_all()
    {"pins": ['0': 0, '1': 1, ... "6": 1]}
    
    @pre
    """
    stats = {}
    for k, pin in PINS.items():
        with LOCKS[k]:
            stats[k] = pin.value
    
    return stats

def echo(*args):
    """Echoes the given args."""
    return ','.join(args)

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
    
    HANDLERS = {
        'BSET'  : set_pin,
        'LIST'  : list_pins,
    }

    COMMANDS = set(map(lambda s: s.casefold(), HANDLERS.keys()))
    
    def __init__(self, addr=None, num_workers=None):
        self.addr = addr if addr else config.NetworkConfig.HOST
        self.num_workers = num_workers if num_workers else config.NetworkConfig.MAX_THREADS
        self.encoding = config.NetworkConfig.ENCODING
        
        # creating sockets
        self.sock = sock.Socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socks = {}
        
        # create thread pool
        self.workers = concurrent.futures.Executor(max_workers=self.num_workers)
    
    @utils.assert_to_false
    def valid_action(self, action):
        """
        Validates the given action object.
        """
        # must be a valid action
        act_type = action.get('type', None)
        assert act_type in self.COMMANDS
        
        if act_type == 'BSET':
            # validator for 'BSET'
            # must have at least pin and val
            assert action.get('pin', None) is not None
            assert action.get('val', None) is not None
            
            # both must be numeric
            assert isinstance(action['pin'], REAL_NUMS) == isinstance(action['val'], REAL_NUMS)
            
            # pin number must be within range
            assert action['pin'] in _PINS
        elif act_type == 'LIST':
            # validator for 'LIST'
            pass
        return True
    
    def handle(self, conn):
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
                msg = json.loads(str(chunks, self.encoding))
                logging.info("[@server] %s", msg)
            except ValueError:
                logging.warning("[@server]")
                return
            
            # validae
            if not self.valid_action(msg):
                logging.warning("[@server] Invalid command: %s", msg)
                return
            
            # dispatch
            resp = self.HANDLERS.get(msg["action"], echo)(msg)
            print("[@server] responded: {}".format(resp))
            
            # respond
            conn.sendall(bytes(json.dumps(resp), self.encoding))
            
        # cleanup
        del self.socks[conn.get_ident()]
                
    def listen(self, port=None):
        """
        Continuously listens for new connections to the server at (addr, port).
        
        @param      int     port        the port to for the server listen on
        @return     None
        """
        port = port if port else config.NetworkConfig.PORT
        with self.sock:
            self.sock.bind((self.addr, port))
            self.sock.listen()
            
            while True:
                conn, _ = self.sock.accept()
                if conn:
                    self.workers.submit(self.handle, conn)
                    self.socks[conn.get_ident()] = conn
                    
##################################### MAIN #####################################

def main():
    """Main boilerplate."""
    server = Server(addr=config.NetworkConfig.HOST, num_workers=5)
    server.listen(port=config.NetworkConfig.PORT)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
