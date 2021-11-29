from Model.FixedHeader import ProcessFixedHeader, RL_Decode
from Model.PacketProcessing import ToProcess

class Client:
    def __init__(self,conn,addr):
        self.socket = conn
        self.adress = addr
        self.connected = False
        self.thread = None

    #This is the soul of our app.
    def ReadMQTTPackage(self):

        print(f"The fixed header is: {self.socket}") # Reads 8 bites
        type=ProcessFixedHeader(self)

        #Only needs exactly as much as it needs
        remainingLength = RL_Decode(self)
        print(f" The size of the pachage is:{remainingLength}")

        restOfPacket = self.socket.recv(remainingLength)

        print(f" The rest of the pachage is:{restOfPacket}")
        ToProcess(self,type,restOfPacket)
        return

    def Disconnect(self):
        print("\nDeconectam pe domnu client")

