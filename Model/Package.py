
from Model.FixedHeader import ProcessFixedHeader
from Model.PacketProcessing import *
from Model.PacketFactory import createPackage

# https://docs.python.org/3/library/struct.html

class Package:
    type = None
    dup = False  # Duplicate delivery of a PUBLISH Control Packet

    QoS = None  # PUBLISH Quality of Service
    retain = False  # PUBLISH Retain flag

    length = 0

    packetIdentifier = 0
    client_id = None

    #Connect
    clearSession = None
    will_flag = None

    #Connak
    sessionAlreadyExisted = False

    def __init__(self):
        pass

    def deserialize(self, data):
        self.type = ProcessFixedHeader(data)
        processPackage(self, self.type, data)

    def serialize(self):
        return createPackage( self)


# This fuction can read a pachage from a socket
def readPackage(socket):
    packageBites = b''
    packageBites += socket.recv(1024)

    # if packageBites:
    # remainingLengthOfPackage = lengthDecode(socket)
    # print(f" The size of the pachage is:{remainingLengthOfPackage}")

    # packageBites += socket.recv(remainingLengthOfPackage)

    return packageBites
