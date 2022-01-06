import time


class Client:
    clientID = None
    associatedSocket = None
    time = None
    deadline = None
    ext_deadline = None
    keep_alive = None
    ping_sent = None
    associatedSession = None

    def __init__(self, clientID, associatedSocket,keep_alive):
        self.clientID = clientID
        self.keep_alive = keep_alive
        self.resetTime()

        self.associatedSocket = associatedSocket

    def applyPachage(self, Pachage):
        pass



    def resetTime(self):
        self.time = time.time()
        self.deadline = self.time + self.keep_alive
        self.ext_deadline = self.deadline + self.keep_alive / 2
        self.ping_sent = False