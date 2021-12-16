

class Client:
    clientID = None
    associatedSocket = None
    associatedSession = None

    def __init__(self, clientID, associatedSocket):
        self.clientID = clientID
        self.associatedSocket = associatedSocket

    def applyPachage(self, Pachage):
        pass

