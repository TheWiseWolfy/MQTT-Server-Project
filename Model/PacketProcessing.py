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

    b8_modified = modifyBit(modifyBit(modifyBit(b8_int, 7, 0), 6, 0), 5,
                            0)  # am schimbat in '0' pe 3 cei mai semnificativi biti
    # pentru a verifica mai usor valorile bitilor 4 si 3

    if b8_modified < 24:
        if b8_modified <= 7:
            print("\nAvem Will QoS=0")
            package.will_qos = 0
        elif b8_modified <= 15:
            print("\nAvel Will QoS=1")
            package.will_qos = 1
        elif b8_modified <= 23:
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
    fmt = '22c'
    id_tuple = unpack(fmt, data[14:14 + client_id_length])
    package.client_id = ""
    for x in id_tuple:
        package.client_id += x.decode("utf-8")
    #main.App.add_element(App, package.client_id)
    package.QoS = 0


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
