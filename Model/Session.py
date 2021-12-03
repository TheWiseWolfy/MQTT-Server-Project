
class Sesion:


    persistent = False
    clientIdentifier = None

    def __init__(self, persistent):
        self.persistent = persistent
