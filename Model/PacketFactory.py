import struct

from Model.Tools import *
from struct import *


def createPackage(package):

    if package.type == PacketType.CONNACK:
        return createCONNACK(package)
    elif package.type == PacketType.SUBACK:
        return createSUBACK(package)


def createSUBACK(package):
    format = "ccccc"

    identifier = (package.packetIdentifier).to_bytes(2,'big')
    data = struct.pack(format, b'\x90', b'\x03' ,identifier[0:1],identifier[1:2], b'\x00')
    return data

def createCONNACK(package):
    SP = b'\x00'

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