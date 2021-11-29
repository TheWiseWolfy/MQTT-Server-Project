from Model.Tools import PacketType

class HeaderException(Exception):
    def __init__(self, message="Header invalid"):
        self.message = message
        super().__init__(self.message)

# Aici primim bitisorii frumosi de la fixed header.
def ProcessFixedHeader(fixedHeader):

    switcher = {
        16: CONNECT,  # 1
        32: CONNACK,  # 2
        48: PUBLISH,  # 3
        64: PUBACK,  # 4
        80: PUBREC,  # 5
        96: PUBREL,  # 6
        112: PUBCOMP,  # 7
        128: SUBSCRIBE,  # 8
        144: SUBACK,  # 9
        160: UNSUBSCRIBE,  # 10
        176: UNSUBACK,  # 11
        192: PINGREQ,  # 12
        208: PINGRESP,  # 13
        224: DISCONNECT,  # 14
    }

    brah = fixedHeader[0] #0001 0011
    brah2 = brah & 240 # & 1111 0000  =   0011 0000
    func = switcher.get(brah2, ERROR)  # Here we pick a function for processing the packet type


    return func(fixedHeader[0]) # Execute the function and return the packet type

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


# We do different things based on different types


def ERROR(fh):
    print("ERROR")
    raise HeaderException()


def CONNECT(fh):
    ValidateZero(fh)
    print("CONNECT")
    return PacketType.CONNECT



def CONNACK(fh):
    ValidateZero(fh)
    print("CONNACK")
    return PacketType.CONNACK


def PUBLISH(fh):
    ValidateZero(fh)
    print("PUBLISH")
    return PacketType.PUBLISH


def PUBACK(fh):
    ValidateZero(fh)
    print("PUBACK")
    return PacketType.PUBACK


def PUBREC(fh):
    ValidateZero(fh)
    print("PUBREC")
    return PacketType.PUBREC


def PUBREL(fh):
    ValidateOne(fh)
    print("PUBREL")
    return PacketType.PUBREL

def PUBCOMP(fh):
    ValidateZero(fh)
    print("PUBCOMP")
    return PacketType.PUBCOMP

def SUBSCRIBE(fh):
    ValidateOne(fh)
    print("SUBSCRIBE")
    return PacketType.SUBSCRIBE

def SUBACK(fh):
    ValidateZero(fh)
    print("SUBACK")
    return PacketType.SUBACK

def UNSUBSCRIBE(fh):
    ValidateOne(fh)
    print("UNSUBSCRIBE")
    return PacketType.UNSUBSCRIBE

def UNSUBACK(fh):
    ValidateZero(fh)
    print("UNSUBACK")
    return PacketType.UNSUBACK

def PINGREQ(fh):
    ValidateZero(fh)
    print("PINGREQ")
    return PacketType.PINGREQ

def PINGRESP(fh):
    ValidateZero(fh)
    print("PINGRESP")
    return PacketType.PINGRESP

def DISCONNECT(fh):
    ValidateZero(fh)
    print("DISCONNECT")
    return PacketType.DISCONNECT

def ValidateZero(byte):
    byte = byte & 15
    if( byte != 0):
        raise HeaderException()

def ValidateOne(byte):
    byte = byte & 15
    if( byte != 2):
        raise HeaderException()