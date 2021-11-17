from Model.FixedHeader import ProcessFixedHeader, RL_Decode


class Client:
    def __init__(self,conn,addr):
        self.socket = conn
        self.adress = addr
        self.connected = False
        self.thread = None

    #This is the soul of our app.
    def ReadMQTTPackage(self):

        print(f"The fixed header is: {self.socket}") # Reads 8 bites
        ProcessFixedHeader(self)

        #Only needs exatly as much as it needs
        remainingLenght = RL_Decode(self)
        print(f" The size of the pachage is:{remainingLenght}")

        restOfPachet = self.socket.recv(remainingLenght)

        print(f" The rest of the pachage is:{restOfPachet}")
        return


