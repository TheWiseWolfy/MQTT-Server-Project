import time


class Client:

    def __init__(self, clientID, associatedSocket,keep_alive):
        self.clientID = clientID
        self.keep_alive = keep_alive
        self.resetTime()

        self.associatedSocket = associatedSocket

        self.time = None
        self.deadline = None
        self.ext_deadline = None
        self.ping_sent = None
        self.associatedSession = None

    def applyPachage(self, Pachage):
        pass



    def resetTime(self):
        self.time = time.time()
        self.deadline = self.time + self.keep_alive
        self.ext_deadline = self.deadline + self.keep_alive / 2
        self.ping_sent = False