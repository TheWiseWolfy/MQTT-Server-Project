
class Sesion:


    def __init__(self, persistent):
        self.persistent = persistent
        self.clientIdentifier = None
        self.subscribedTopics = set()
        self.subscribedTopicsQoS = dict()


    def addTopic(self, topic, QoS):
        self.subscribedTopics.add(topic)
        self.subscribedTopicsQoS[topic] = QoS

    def removeTopics(self, topics):
        self.subscribedTopics = self.subscribedTopics - set(topics)

    def getTopicQoS(self,topic ):
        return self.subscribedTopicsQoS[topic]
