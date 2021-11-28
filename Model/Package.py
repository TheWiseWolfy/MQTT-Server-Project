from  Model.Tools  import PacketType


# https://docs.python.org/3/library/struct.html

class Package:
    type = None
    dup = False # Duplicate delivery of a PUBLISH Control Packet

    QoS = None # PUBLISH Quality of Service
    retain = False # PUBLISH Retain flag

    length = 0

    packetIdentifier =0
    payload = None

    def __init__(self):
        pass
