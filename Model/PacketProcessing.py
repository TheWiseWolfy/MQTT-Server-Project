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
    return func(package, data)


def CONNECT(package, data):
    formString = 'cccccccccccccc'

    _, _, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12 = unpack(formString, data[0: 14])

    if b1 == b'\x00' and b2 == b'\x04' and b3 == b'M' and b4 == b'Q' and b5 == b6 == b'T' and b7:
        print("\nAvem un nume protocol CONNECT valid")
    else:
        print("\n Protocol Name invalid")

    if b5 == b'T':
        print("\nAvem un protocol level CONNECT valid")
    else:
        print("\n Protocol Level invalid")
    b8_int = int.from_bytes(b8, byteorder='big', signed=False)
    if b8_int & 1 == 0:
        print("\nBitul reserved este 0, and that's good")
    else:
        print("\nBitul reserved nu este 0, cerem deconectarea clientului")

    if b8_int & 2 == 2:
        package.clean = True
        print("\nBitul CleanSession este 1")
    else:
        package.clean = False
        print("\nBitul CleanSession este 0")

    if b8_int & 4 == 4:
        package.will_flag = True
        print("\nAfisam un Will Message")
        if b8_int & 32 == 32:
            package.will_retain = True
            print("\nWill Message va fi retinut, will retain=1")
        else:
            package.will_retain = False
            print("\nWill Message NU va fi retinut, will retain=0")
    else:
        package.will_flag = False
        package.will_retain = False  # nu stiu daca asa functioneaza randul 509 din documentatie
        print("\nNu afisam un Will Message")

    if b8_int & 24 < 24:
        if b8_int & 24 <= 7:
            print("\nAvem Will QoS=0")
            package.will_qos = 0
        elif b8_int & 24 <= 15:
            print("\nAvel Will QoS=1")
            package.will_qos = 1
        elif b8_int & 24 <= 23:
            print("\nAvem Will QoS=2")
            package.will_qos = 2
    else:
        print("\nWill QoS invalid(=3)")

    if b8_int & 128 == 128:
        package.username = True
        print("\nTrebuie sa avem un username in payload")
    else:
        package.username = False
        package.password = True
        print("\nNU trebuie sa avem un username in payload, implicit nici o parola")  # nesigur si aici, randul 525

    if b8_int & 64 == 64:
        package.password = True
        print("\nTrebuie sa avem o parola in payload")
    else:
        package.password = False
        print("\nNU trebuie sa avem o parola in payload")

    package.keep_alive = int.from_bytes(b10 + b9, byteorder='big', signed=False)
    print("\nKeep alive =", package.keep_alive, "secunde")

    client_id_length = int.from_bytes(b11 + b12, byteorder='big', signed=False)
    fmt = str(client_id_length) + 'c'
    id_tuple = unpack(fmt, data[14:14 + client_id_length])
    package.client_id = ""
    for x in id_tuple:
        package.client_id += x.decode("utf-8")

    package.QoS = 0
    pass


def CONNACK(data):
    pass


def PUBLISH(package, data):
    formString = 'cccc'
    b1, _, b3, b4 = unpack(formString, data[0: 4])
    b1_int = int.from_bytes(b1, byteorder='big', signed=False)
    package.dup = b1_int & 8
    print("\nDUP flag = ", package.dup)

    if b1_int & 6 < 6:
        if b1_int & 6 <= 1:
            print("\nAvem QoS=0")
            package.qos = 0
        elif b1_int & 6 <= 3:
            print("\nAvel QoS=1")
            package.qos = 1
        elif b1_int & 6 <= 5:
            print("\nAvem QoS=2")
            package.qos = 2
    else:
        print("\nQoS invalid (=3), inchidem conexiunea")

    package.retain = b1_int & 1

    topic_name_length = int.from_bytes(b3 + b4, byteorder='big', signed=False)
    fmt = str(topic_name_length + (2 if package.qos > 0 else 0)) + 'c'
    tuple_pub = unpack(fmt, data[4:4 + topic_name_length + (2 if package.qos > 0 else 0)])

    package.topic_name = ""
    for x in range(0, topic_name_length):
        package.topic_name += tuple_pub[x].decode("utf-8")
    print("\n Topic name:", package.topic_name)

    if package.qos > 0:
        for y in range(topic_name_length, topic_name_length + 2):
            package.packetIdentifier += int.from_bytes(tuple_pub[y], byteorder='big', signed=False)
    print("\n Packet ID:", package.packetIdentifier)

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
