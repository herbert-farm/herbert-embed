"""
@name   GPIO Client
@desc   Client for interacting with the GPIO through the GPIO server.

The Client class exposes mutation high-level operations for readability. It serializes the sent commands to the server using JSON.

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import json
import socket
import logging

from . import sock
from .. import config

if config.NetworkConfig.DEBUG:
    logging.basicConfig(level=logging.DEBUG)

HOST = config.NetworkConfig.HOST   # The remote host
PORT = config.NetworkConfig.PORT   # The same port as used by the server

class Client(object):
    """
    @name   Client
    @desc   GPIO client class
    """
    
    def __init__(self, addrport=None):
        if addrport is None:
            addrport = (HOST, PORT)
        
        assert len(addrport) == 2
        if not all(addrport):
            if addrport is None:
                addrport = (HOST, PORT)
                
        self.encoding = config.NetworkConfig.ENCODING
        
        self.sock = sock.Socket
    
    def send(self, data):
        """
        Serialize and send raw data.
        
        @param      dict        data        the data to serialize and send
        @return     dict        the response, if any
        """
        with self.sock(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            # serialize cmd
            msg = json.dumps(data)
            
            # send it
            s.sendall(bytes(msg, self.encoding))
            
            # close write end
            s.shutdown(socket.SHUT_WR)
            
            # print response, if any
            data = s.recv(1024)
            data = json.loads(str(data, self.encoding))
            
            logging.info("@client: {}".format(data))
            
            if not data:
                return
                
            return data
    
    def set(self, pin, val):
        """
        Set the value of a single pin.
        
        @pre        `pin` must be an non-negative integer
        @pre        `val` must be a 0 or 1
        
        @param      int     pin     the pin to set the value for
        @param      int     val     the value to set the pin to
        @return     bool    True if the operation succeeded, False otherwise
        
        ex.
        >>> gpio.set(0)
        {"pins": {'0': 0}}
        """
        pcmd = {"type": 'BSET', "pin": pin, "val": val}
        res = self.send(pcmd)
        
        if res['ok']:
            return res['data']
    
    def get(self, pin):
        """
        Get the value of a single pin.
        
        ex.
        >>> gpio.get(0)
        {"pins": {'0': 0}}
        """
        pcmd = {"type": 'SHOW', "pin": pin}
        res = self.send(pcmd)
        
        if res['ok']:
            return res['data']
    
    def get_many(self, pins, *args):
        """
        Get the value of many pins.
        
        ex.
        >>> gpio.get_many(0)
        {"pins": {'0': 0}}
        """
        # NOTE: not hp
        pass
    
    def get_all(self):
        """
        Get the value of all the pins.
        
        ex.
        >>> gpio.get_all()
        {"pins": ['0': 0, '1': 1, ... "6": 1]}
        """
        pcmd = {"type": 'LIST'}
        res = self.send(pcmd)
        
        if res['ok']:
            return res['data']
