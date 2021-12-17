from Model.Tools import *
from Model.Client import Client
from Model.Session import Sesion
from Model.Package import Package


class ClientManager:
    activeClients = dict()    #A client is asociate with the lifetime of a socket
    sessions = dict()          #A socket is associated with a client id

    def __init__(self):
        pass

    def applyPachage(self, package, mySocket):
        # Daca detectam un pachet de tip CONNECT
        # cautam ID-ul clientului sa vedem daca inca mai exista in lista noasta de clienti
        # daca nu exista, cram un client nou, si asamblam pachetul CONNECT
        # pe care il trimitem inapoi tot aici

        if (package.type == PacketType.CONNECT):
            self.ProcessConnect(package, mySocket)
        elif (package.type == PacketType.SUBSCRIBE):
            self.ProcessSubscribe(package, mySocket)
        elif (package.type == PacketType.PUBLISH):
            self.ProcessPublish(package, mySocket)

    #This fuction exists in case the client dies before sending a disconect.
    def disconectClientWithSocket(self, mySocket):
        del self.activeClients[mySocket]

    #Logica de raspuns pentru diferite pachete


    def ProcessConnect(self,package, mySocket):
        #Flags for connack
        sessionAlreadyExisted = False

        ## CLIENT HANDDLELING ##

        #Clientul este un obiect care exista doar pe parcursul conectiuni !!
        if mySocket in self.activeClients:
           raise "This client has not been properly disconected last time."

        #Cream o structura de date de tip client
        newClient = Client(package.client_id, mySocket)
        self.activeClients[mySocket] = newClient           #Fiecare client este identificat dupa socket-ul pe care sta ?

        ## SESSION HANDDLELING ##
        if package.clearSession:  # Daca clear session este setat pe 1
            if package.client_id in self.sessions:
                del self.sessions[package.client_id]                #Daca gasim o sesiune, o stergem

            newSession = Sesion(persistent=False)           # cream o sesiune noua menita sa fie temporara
            self.sessions[package.client_id] = newSession
            newClient.associatedSession = newSession         #Asociem momentan clientul cu sesiunea
        else:                                           # Daca clear session este setat pe 0
            if package.client_id not in self.sessions:  # daca nu exista o sesiune existenta pentru client id-ul curent
                newSession = Sesion(persistent=True)    # cream noi o sesiune si o asociem noului client
                self.sessions[package.client_id] = newSession
                newClient.associatedSession = newSession
            else:                                       # daca exista deja o sesiune, doar confirmam asta prin connack
                sessionAlreadyExisted = True
                newClient.associatedSession = self.sessions[package.client_id]

         ##WILL MESSAGE HANDDLELINGN ##

        # if package.will_flag:
        #     newClient.willFlag = True
        #     newClient.willMessage = "I guess someone forgot to implement the actual WILL MESSAGEEEEEEEEEEE"

        ## CONNACK ##

        newPackage = Package()
        newPackage.type = PacketType.CONNACK
        newPackage.clearSession = package.clearSession  # We keep this data in order to form the CONNAK properly
        newPackage.sessionAlreadyExisted = sessionAlreadyExisted
        data = newPackage.serialize()

        mySocket.send(data)

    def ProcessSubscribe(self, package, mySocket):

        ## MEMORIZING SUBSCRIBE TOPICS ##

        ourClient = self.activeClients[mySocket]
        ourClient.associatedSession.addTopics(  package.topicList )
        #Here we should probably do important stuffs

        ## SUBACK ##

        newPackage = Package()
        newPackage.type = PacketType.SUBACK
        newPackage.packetIdentifier = package.packetIdentifier
        data = newPackage.serialize()
        mySocket.send(data)

    def ProcessPublish(self, package, mySocket):
        for client in self.activeClients.values():
            session = client.associatedSession
            value = (package.topic_name, package.QoS)
            if value  in session.subscribedTopics:
                self.PublishMessage(client, package.message, package.topic_name, 0, 0, 0)

    def PublishMessage(self ,client, message, topic, qos, duplicate, retain):
        pass