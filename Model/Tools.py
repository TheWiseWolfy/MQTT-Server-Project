import enum

class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PacketType(enum.Enum):
    CONNECT=1
    CONNACK=2
    PUBLISH=3
    PUBACK=4
    PUBREC=5
    PUBREL=6
    PUBCOMP=7
    SUBSCRIBE=8
    SUBACK=9
    UNSUBSCRIBE=10
    UNSUBACK=11
    PINGREQ=12
    PINGRESP=13
    DISCONNECT=14