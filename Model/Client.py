import time


class Client:
    clientID = None
    associatedSocket = None
    time = None
    deadline = None
    ext_deadline = None
    keep_alive = None
    ping_sent = None

    def __init__(self, clientID, keep_alive):
        self.clientID = clientID
        self.keep_alive = keep_alive
        self.time = time.time()
        self.deadline = self.time + keep_alive
        self.ext_deadline = self.deadline + keep_alive / 2
        self.ping_sent=False

    def applyPachage(self, Pachage):
        pass
