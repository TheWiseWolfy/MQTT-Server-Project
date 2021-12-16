
class Sesion:


    persistent = False
    clientIdentifier = None

    subscribedTopics = set()

    def __init__(self, persistent):
        self.persistent = persistent

    def addTopics(self, topics):
        self.subscribedTopics.update( topics )