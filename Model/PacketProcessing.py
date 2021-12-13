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
        package.clearSession = True
        print("\nBitul CleanSession este 1")
    else:
        package.clearSession = False
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

    package.keep_alive = int.from_bytes(b9 + b10, byteorder='big', signed=False)
    print("\nKeep alive =", package.keep_alive, "secunde")

    client_id_length = int.from_bytes(b11 + b12, byteorder='big', signed=False)
    fmt = str(client_id_length) + 'c'

    id_tuple = unpack(fmt, data[14:14 + client_id_length])
    package.client_id = ""
    for x in id_tuple:
        package.client_id += x.decode("utf-8")
    print('\n', package.client_id)

    package.QoS = 0


def CONNACK(package, data):
    pass


def PUBLISH(package, data):
    formString = 'cccc'
    b1, b2, b3, b4 = unpack(formString, data[0: 4])
    b1_int = int.from_bytes(b1, byteorder='big', signed=False)
    b2_int = int.from_bytes(b2, byteorder='big', signed=False)

    package.dup = b1_int & 8
    print("DUP flag = ", package.dup)

    if b1_int & 6 < 6:
        if b1_int & 6 <= 1:
            print("Avem QoS=0")
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

    package.packetIdentifier = ""
    if package.qos > 0:
        package.packetIdentifier = int.from_bytes(tuple_pub[topic_name_length] + tuple_pub[topic_name_length + 1],
                                                  byteorder='big', signed=False)
    print("\n Packet ID:", package.packetIdentifier)

    brah = 4 + topic_name_length + (2 if package.qos > 0 else 0)
    fmt = str(b2_int - brah+2) + 'c'
    message = unpack(fmt, data[brah: b2_int + 2])

    package.message = ""
    for x in range(0, b2_int - brah+2):
        package.message += message[x].decode("utf-8")
    print("\n Publish message:", package.message)


def PUBACK(package, data):
    pass


def PUBREC(package, data):
    pass


def PUBREL(package, data):
    pass


def PUBCOMP(package, data):
    pass


def SUBSCRIBE(package, data):
    formString = 'cccc'

    #Variable header
    _, _, b1, b2, = unpack(formString, data[0: 4])
    package.packetIdentifier =  int.from_bytes(b1 + b2 ,"big", signed=False)

    #Payload
    dataPointer = 4

    topicSize = int.from_bytes(data[dataPointer:dataPointer + 2]  ,"big", signed=False)
    print(f"My topic size is {topicSize}")

    startOfTopicPointer =  dataPointer + 2
    endOfTopicPointer = topicSize + startOfTopicPointer   #Calculam unde se termina sirul de caractere al topicului dupa dataPointer

    topicName = data[startOfTopicPointer:endOfTopicPointer].decode("utf-8")
    topicQoS = data[endOfTopicPointer]

    package.topicList.append((topicName, topicQoS))     #Aici inseram un touple format din numele topicului si QoS-ul

    #Aici ar trebui sa poata citi o lista de topicuri dar cu clientul asta, nu pare sa fie necesar aparent.
    dataPointer = endOfTopicPointer

def SUBACK(package, data):
    pass


def UNSUBSCRIBE(package, data):
    pass


def UNSUBACK(package, data):
    pass


def PINGREQ(package, data):
    pass


def PINGRESP(package, data):
    pass


def DISCONNECT(package, data):
    pass
