
def ToProcess(client,type, data):
    switcher = {
        1: CONNECT,
        2: CONNACK,
        3: PUBLISH,
        4: PUBACK,
        5: PUBREC,
        6: PUBREL,
        7: PUBCOMP,
        8: SUBSCRIBE,
        9: SUBACK,
        10: UNSUBSCRIBE,
        11: UNSUBACK,
        12: PINGREQ,
        13: PINGRESP,
        14: DISCONNECT,
    }
    func = switcher.get(type.value)
    func(client,data)
    return 0


def CONNECT(client,data):
    byte1_str = data[0:8].decode('utf-8')
    byte2_str = data[8:16].decode('utf-8')
    byte3_str = data[16:24].decode('utf-8')
    byte4_str = data[24:32].decode('utf-8')
    byte5_str = data[32:40].decode('utf-8')
    byte6_str = data[40:48].decode('utf-8')

    if byte1_str != '00000000':
        client.Disconnect()
    if byte2_str!='00000100':
        client.Disconnect()
    if byte3_str != '01001101':
        client.Disconnect()
    if byte4_str != '01010001':
        client.Disconnect()
    if byte5_str != '01010100':
        client.Disconnect()
    if byte6_str != '01010100':
        client.Disconnect()
    print("\nS-a facut cu succes")

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
