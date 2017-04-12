"""
@name   GPIO Client
@desc   Client for interacting with the GPIO through the GPIO server.

The Client class exposes mutation high-level operations for readability. It serializes the sent commands to the server using JSON.

@author Joshua Paul A. Chan (@joshpaulchan)
"""

import sock
import json
from .. import config

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
        self.conn = None
    
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
        {"pins": ['0': 0]}
        """
        pass
    
    
    def get(self, pin):
        """
        Get the value of a single pin.
        
        ex.
        >>> gpio.get(0)
        {"pins": ['0': 0]}
        """
        pass
    
    
    def get_many(self, pins, *args):
        """
        Get the value of many pins.
        
        ex.
        >>> gpio.get_many(0)
        {"pins": ['0': 0]}
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
        pass
    
# main
def main():
    # create the screens
    with sock.Socket(sock.socket.AF_INET, sock.socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
            
        pcmd = {"action": 'SET', "pin": 12, "val": 1}
        
        # serialize cmd
        
        # send it
        s.sendall(bytes(pcmd, config.NetworkConfig.ENCODING))
        
        # print response, if any
        data = s.recv(1024)
        
        if not data:
            continue
        
        print("@client: {}".format(str(data)))

if __name__ == '__main__':
    try: main()
    except KeyboardInterrupt: exit()
