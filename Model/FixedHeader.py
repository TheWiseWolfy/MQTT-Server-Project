from Model.Tools import PacketType

class HeaderException(Exception):
    def __init__(self, message="Header invalid"):
        self.message = message
        super().__init__(self.message)

# Aici primim bitisorii frumosi de la fixed header.
def ProcessFixedHeader(client):
    fixedHeader = client.socket.recv(8)

    switcher = {
        b'0001': CONNECT,  # 1
        b'0010': CONNACK,  # 2
        b'0011': PUBLISH,  # 3
        b'0100': PUBACK,  # 4
        b'0101': PUBREC,  # 5
        b'0110': PUBREL,  # 6
        b'0111': PUBCOMP,  # 7
        b'1000': SUBSCRIBE,  # 8
        b'1001': SUBACK,  # 9
        b'1010': UNSUBSCRIBE,  # 10
        b'1011': UNSUBACK,  # 11
        b'1100': PINGREQ,  # 12
        b'1101': PINGRESP,  # 13
        b'1110': DISCONNECT,  # 14
    }

    func = switcher.get(fixedHeader[0:4], ERROR)  # Here we pick a function for processing the packet type

    return func(fixedHeader[4:8]) # Execute the function and return the packet type

def RL_Decode(client):
    res = 0

    multiplier = 1
    while True:
        bytes = client.socket.recv(8)
        encodedByte = to_int(bytes)
        # print(f"\n{encodedByte}")

        res += (encodedByte & 127) * multiplier
        multiplier *= 128
        if multiplier > 128 * 128 * 128:
            raise Exception("Malformed Remaining Length")
        if encodedByte & 128 == 0:
            break
    return res


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


def to_int(x):
    enc = x.decode('utf-8')
    aux = 128
    res = 0
    for i in range(0, 8):
        if enc[i] == '1':
            res += aux
        aux = aux / 2
    return int(res)


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

def ValidateZero(fh):
    enc = fh.decode('utf-8')
    for i in range(0, 4):
        if enc[i] != '0':
            raise HeaderException()

def ValidateOne(fh):
    enc = fh.decode('utf-8')
    if enc[0] != '0' and enc[1] != '1' and enc[2] != '0' and enc[3] != '0':
        raise HeaderException()
