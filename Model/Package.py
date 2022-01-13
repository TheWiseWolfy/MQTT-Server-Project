
from Model.FixedHeader import ProcessFixedHeader
from Model.PacketProcessing import *
from Model.PacketFactory import createPackage

# https://docs.python.org/3/library/struct.html

class Package:
    def __init__(self):
        self.type = None

        # General package fields
        self.dup = False  # Duplicate delivery of a PUBLISH Control Packet
        self.QoS = None  # PUBLISH Quality of Service
        self.retain = False  # PUBLISH Retain flag
        self.packetIdentifier = 0
        self.client_id = ''

        # Subscribe
        self.topicList = list()
        self.topicQoS = dict()

        # Sessions
        self.clearSession = None

        # Last will
        self.will_flag = None
        self.will_retain = None
        self.will_qos = None
        self.will_message = ''
        self.will_topic = ''

        # Authentification
        self.username = None
        self.password = None

        # Keep alive
        self.keep_alive = None

        # Connak flags
        self.sessionAlreadyExisted = False

        # Publish
        self.message = ""
        self.topicName = ""

    def deserialize(self, data):
        self.type = ProcessFixedHeader(data)
        processPackage(self, data)

    def serialize(self):
        return createPackage(self)


# This fuction can read a pachage from a socket
def readPackage(socket):
    packageBites = b''
    try:
        packageBites += socket.recv(2)

        if packageBites:
             remainingLengthOfPackage = packageBites[1]
        else:
            return 0

        #The standard includes packages bigger than 128 bytes but we don't for now.
        packageBites += socket.recv(remainingLengthOfPackage)

        return packageBites
    except Exception:
        raise Exception("Socket failed")

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
