#!/usr/bin/env python3
"""
`sock.py`
Builds upon the socket class to allow easy parsing of variable-length messages during IPC.
"""

import socket

class Socket(socket.socket):
    """
    `Socket`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_var(self, var_msg, *args, **kwargs):
        """
        Sends a variable length message with a length header.
        """
        return super(Socket, self).sendall(var_msg, *args, **kwargs)

    def recv_var(self, *args, **kwargs):
        """
        Receives the entirety of a message sent using send_var.
        """
        # Keeps receiving until N-bytes length header fully uncovered
        
        # Align stream and start reading untilJ
        return super(Socket, self).recv(1024, *args, **kwargs)
