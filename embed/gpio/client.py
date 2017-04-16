"""
@name   GPIO Client
@desc   Client for interacting with the GPIO through the GPIO server.

The Client class exposes mutation high-level operations for readability. It
serializes the sent commands to the server using JSON.

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import json
# TODO: factor out socket, only rely on sock
import socket
import logging

from . import sock, actions
from .. import config, utils

if config.GPIOConfig.DEBUG:
    logging.basicConfig(
        level=config.GPIOConfig.LOG_LEVEL,
        format='%(asctime)s:%(levelname)s:GPIO/client:%(message)s'
    )

class Client(object):
    """
    @name   Client
    @desc   GPIO client class
    """
    
    host = config.NetworkConfig.HOST            # The remote host
    port = PORT = config.NetworkConfig.PORT     # The same port as the server
    
    def __init__(self, addr=None, port=None):
        self.host = addr if addr else self.host
        self.port = port if port else self.port
        self.addrport = (self.host, self.port)
                
        self.encoding = config.NetworkConfig.ENCODING
        
        self.sock = sock.Socket
    
    def send(self, act_type, params=None):
        """
        Serialize and send raw data.
        
        @see    `doc/ipc.md` for more explanation of the send mechanics and the data format
        
        @param      str     act_type    the type of action
        @param      dict    params      the specific
        @return     dict    the response, if any
        """
        # serialize cmd
        if params is None:
            params = {}

        msg = json.dumps({"type":act_type, "params":params})
        
        with self.sock(socket.AF_INET, socket.SOCK_STREAM) as sck:
            sck.connect(self.addrport)
            
            # send it
            sck.sendall(bytes(msg, self.encoding))
            logging.info("sent: %s", msg)
            
            # close write end
            sck.shutdown(socket.SHUT_WR)
            
            # log response, if any
            data = sck.recv(1024)
            
            try:
                data = json.loads(str(data, self.encoding))
            except ValueError:
                logging.error("Error parsing the response: `%s`", data)
                return {"ok" : False}
            
            logging.info("received: %s", data)
            
            if not data:
                return {"ok" : False}
                
            return data
    
    def set_pin(self, pin, val):
        """
        Set the value of a single pin.
        
        @pre        `pin` must be an non-negative integer
        @pre        `val` must be a 0 or 1
        
        @param      int     pin     the pin to set the value for
        @param      int     val     the value to set the pin to
        @return     bool    True if the operation succeeded, False otherwise
        
        ex.
        >>> gpio.set(0)
        {"pin": {'0': 0}}
        """
        res = self.send(actions.Types.SET_PIN, {"pin": pin, "val": val})
        
        if res['ok']:
            return res['data']
    
    def get_pin(self, pin):
        """
        Get the value of a single pin.
        
        ex.
        >>> gpio.get(0)
        {"pin": {'0': 0}}
        """
        res = self.send(actions.Types.GET_PIN, {"pin": pin})
        
        if res['ok']:
            return res['data']
    
    def get_pins(self):
        """
        Get the value of all the pins.
        
        ex.
        >>> gpio.get_pins()
        {"pins": {'0': 0, '1': 1, ... ,"6": 1}}
        """
        res = self.send(actions.Types.LIST_PINS)
        
        if res['ok']:
            return {"pins": utils.merge_dicts(*res['data'])}
    
    def get_channel(self, channel):
        """
        Get the value of a single pin.
        
        ex.
        >>> gpio.get_channel(0)
        {"channel": {'0': 0}}
        """
        res = self.send(actions.Types.GET_PIN, {"channel": channel})
        
        if res['ok']:
            return res['data']
    
    def get_channels(self):
        """
        Get the value of all the pins.
        
        ex.
        >>> gpio.get_channels()
        {"channels": {'0': 0, '1': 1, ... "6": 1}}
        """
        res = self.send(actions.Types.LIST_CNLS)
        
        if res['ok']:
            return {"channels": utils.merge_dicts(*res['data'])}
