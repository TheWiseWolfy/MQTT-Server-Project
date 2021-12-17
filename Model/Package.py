
from Model.FixedHeader import ProcessFixedHeader
from Model.PacketProcessing import *
from Model.PacketFactory import createPackage

# https://docs.python.org/3/library/struct.html

class Package:
    type = None

    #General package fields
    dup = False  # Duplicate delivery of a PUBLISH Control Packet
    QoS = None  # PUBLISH Quality of Service
    retain = False  # PUBLISH Retain flag
    packetIdentifier = 0
    client_id = None

    #Subscribe
    topicList = list()

    #Sessions
    clearSession = None

    #Last will
    will_flag = None
    will_retain = None
    will_qos = None

    #Authentification
    username = None
    password = None

    #Keep alive
    keep_alive = None

    #Connak flags
    sessionAlreadyExisted = False

    #Publish
    message = ""
    topic_name = ""

    def __init__(self):
        pass

    def deserialize(self, data):
        self.type = ProcessFixedHeader(data)
        processPackage(self, self.type, data)

    def serialize(self):
        return createPackage(self)


# This fuction can read a pachage from a socket
def readPackage(socket):
    packageBites = b''
    packageBites += socket.recv(2)

    if packageBites:
         remainingLengthOfPackage = packageBites[1]
    else:
        return 0

    #The pachage includes packages bigger than 128 bytes but we don't for now.
    packageBites += socket.recv(remainingLengthOfPackage)

    return packageBites

# def lengthDecode(socket):
#     res = 0
#
#     multiplier = 1
#     while True:
#         bytes = socket.recv(8)
#         encodedByte = int(bytes)
#         # print(f"\n{encodedByte}")
#
#         res += (encodedByte & 127) * multiplier
#         multiplier *= 128
#         if multiplier > 128 * 128 * 128:
#             raise Exception("Malformed Remaining Length")
#         if encodedByte & 128 == 0:
#             break
#     return res


# def RL_Encode(x):
#     while True:
#         encodedByte = x % 128
#         x = x / 128
#         if x > 0:
#             encodedByte = encodedByte | 128
#         res = encodedByte
#         if x < 0:
#             break
#     return res
