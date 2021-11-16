# Aici primim bitisori frumosi de la fixed header.
def ProcessFixedHeader(fixedHeader):
    print(fixedHeader[0:4])

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
    func()  # Execute the function

    return 0





def ERROR():
    print("CONNECT")


def CONNECT():
    print("CONNECT")

def CONNACK():
    print("CONNACK")


def PUBLISH():
    print("PUBLISH")


def PUBACK():
    print("PUBACK")


def PUBREC():
    print("PUBREC")


def PUBREL():
    print("PUBREL")


def PUBCOMP():
    print("PUBCOMP")


def SUBSCRIBE():
    print("SUBSCRIBE")


def SUBACK():
    print("SUBACK")


def UNSUBSCRIBE():
    print("UNSUBSCRIBE")


def UNSUBACK():
    print("UNSUBACK")


def PINGREQ():
    print("PINGREQ")


def PINGRESP():
    print("PINGRESP")


def DISCONNECT():
    print("DISCONNECT")
