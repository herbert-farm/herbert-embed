#!/usr/bin/env python3
"""
`sock.py`
Builds upon the socket class to allow easy parsing of variable-length messages during IPC.
"""

import socket

from embed import config

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


# class Socket(object):
#     """demonstration class only
#       - coded for clarity, not efficiency
#     """
# 
#     def __init__(self, sock=None):
#         if sock is None:
#             self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self.encoding = config.NetworkConfig.ENCODING
#         else:
#             self.sock = sock
# 
#     def connect(self, host, port):
#         self.sock.connect((host, port))
# 
#     def mysend(self, msg):
#         totalsent = 0
#         while totalsent < MSGLEN:
#             sent = self.sock.send(msg[totalsent:])
#             if sent == 0:
#                 raise RuntimeError("socket connection broken")
#             totalsent = totalsent + sent
# 
#     def myreceive(self):
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < MSGLEN:
#             chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
#             if chunk == b'':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
#         return b''.join(chunks)
