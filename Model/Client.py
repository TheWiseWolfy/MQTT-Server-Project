import time


class Client:

    def __init__(self, clientID, associatedSocket,keep_alive):
        self.associatedSocket = associatedSocket
        self.associatedSession = None

        self.clientID = clientID
        self.safelyDisconnected = False
        self.authenticated = False

        #Keep alive
        self.keep_alive = keep_alive
        self.time = None
        self.deadline = None
        self.ext_deadline = None
        self.ping_sent = None

        #Last will
        self.willFlag = False
        self.willTopic = None
        self.willMessage = None

    def resetTime(self):
        self.time = time.time()
        self.deadline = self.time + self.keep_alive
        self.ext_deadline = self.deadline + self.keep_alive / 2
        self.ping_sent = False