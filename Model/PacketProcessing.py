from Model.Tools import *
from struct import *

def processPackage(package, type, data):

    switcher = {
        PacketType.CONNECT: CONNECT,
        PacketType.CONNACK: CONNACK,
        PacketType.PUBLISH: PUBLISH,
        PacketType.PUBACK: PUBACK,
        PacketType.PUBREC: PUBREC,
        PacketType.PUBREL: PUBREL,
        PacketType.PUBCOMP: PUBCOMP,
        PacketType.SUBSCRIBE: SUBSCRIBE,
        PacketType.SUBACK: SUBACK,
        PacketType.UNSUBSCRIBE: UNSUBSCRIBE,
        PacketType.UNSUBACK: UNSUBACK,
        PacketType.PINGREQ: PINGREQ,
        PacketType.PINGRESP: PINGRESP,
        PacketType.DISCONNECT: DISCONNECT,
    }
    func = switcher.get(type)
    return func(package,data)

def CONNECT(package,data):
    formString = 'ccc'

    _, _, c = unpack(formString, data[0: 3])

    if c == b'\x10':
        print("all good")

    package.QoS = 0;
    package.abracadabra = 122

def CONNACK(data):
    pass


def PUBLISH(data):
    pass


def PUBACK(data):
    pass


def PUBREC(data):
    pass


def PUBREL(data):
    pass


def PUBCOMP(data):
    pass


def SUBSCRIBE(data):
    pass


def SUBACK(data):
    pass


def UNSUBSCRIBE(data):
    pass


def UNSUBACK(data):
    pass


def PINGREQ(data):
    pass


def PINGRESP(data):
    pass


def DISCONNECT(data):
    pass
