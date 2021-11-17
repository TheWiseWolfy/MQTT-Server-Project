from Model.FIxedHeader import ProcessFixedHeader


class Client:
    def __init__(self,conn,addr):
        self.socket = conn
        self.adress = addr
        self.connected = False
        self.thread = None

    #This is the soul of our app.
    def ReadMQTTPackage(self):
        fixedHeader = self.socket.recv(8)

        print(f"The fixed header is: {fixedHeader}")
        ProcessFixedHeader(fixedHeader)

        #Only needs exatly as much as it needs
        remainingLenght = RL_Decode(self.socket)
        print(f" The size of the pachage is:{remainingLenght}")

        restOfPachet = self.socket.recv(remainingLenght)

        print(f" The rest of the pachage is:{restOfPachet}")
        return

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


def RL_Decode(conn):
    bytesUsed = 1
    res = 0

    multiplier = 1
    while True:
        brah = conn.recv(8);

        encodedByte = to_int(brah)
        #print(f"\n{encodedByte}")

        res += (encodedByte & 127) * multiplier
        multiplier *= 128
        if multiplier > 128 * 128 * 128:
            raise Exception("Malformed Remaining Length")
        if encodedByte & 128 == 0:
            break
    return res

def to_int(x):
    enc=x.decode('utf-8')
    aux=1
    res=0
    for i in range(1,7):
        if enc[i]=='1':
            res+=aux
        aux = aux * 2
    return int(res)
