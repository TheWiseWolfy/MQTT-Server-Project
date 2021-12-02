import struct

from Model.Tools import *
from struct import *


def createPackage(package):
    SP = b'\x00'
    if package.type == PacketType.CONNACK:
        format = "cccc"

        if package.clearSession:
            SP = b'\x00'  # If the Server accepts a connection with CleanSession set to 1, the Server MUST set Session Present to 0
        else:  # If the Server accepts a connection with CleanSession set to 0
            if package.sessionAlreadyExisted:  # If the Server has stored Session state, it MUST set Session Present to 1
                SP = b'\x01'
            else:  # If the Server does not have stored Session state, it MUST set Session Present to 0
                SP = b'\x00'

        data = struct.pack(format, b'\x20', b'\x02', SP, b'\x00')
        return data