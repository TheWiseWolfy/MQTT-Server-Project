import time


class Client:

    def __init__(self, clientID, associatedSocket, keep_alive):
        self.associatedSocket = associatedSocket
        self.associatedSession = None

        self.clientID = clientID
        self.safelyDisconnected = False

        # Keep alive
        self.keep_alive = keep_alive
        self.time = None
        self.ext_deadline = None

        # Last will
        self.willFlag = False
        self.willTopic = None
        self.willMessage = None
        self.willQoS = None

    def resetTime(self):
        self.time = time.time()
        self.ext_deadline = self.time + self.keep_alive + self.keep_alive / 2
