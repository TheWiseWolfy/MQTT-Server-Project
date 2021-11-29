import struct

from Model.FixedHeader import ProcessFixedHeader, lengthDecode

# https://docs.python.org/3/library/struct.html

class Package:
    type = None
    dup = False # Duplicate delivery of a PUBLISH Control Packet

    QoS = None # PUBLISH Quality of Service
    retain = False # PUBLISH Retain flag

    length = 0

    packetIdentifier =0
    payload = None

    def __init__(self,data):
        pass

    def deserialize(self, data):
        pass

    def serialize(self):
        pass


#This fuction can read a pachage from a socket
def readPackage(socket):
    packageBites = b''
    packageBites += socket.recv(8)

    if packageBites:
        remainingLengthOfPackage = lengthDecode(socket)
        print(f" The size of the pachage is:{remainingLengthOfPackage}")

        packageBites += socket.recv(remainingLengthOfPackage)

    return packageBites





