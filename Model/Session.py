
class Sesion:


    def __init__(self, persistent):
        self.persistent = persistent
        self.clientIdentifier = None
        self.subscribedTopics = set()


    def addTopics(self, topics):
        self.subscribedTopics.update( topics )