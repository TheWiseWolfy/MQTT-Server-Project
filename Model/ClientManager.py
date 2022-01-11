import time
from datetime import datetime

from Model.Autentification import checkPassword
from Model.Tools import *
from Model.Client import Client
from Model.Session import Sesion
from Model.Package import Package


class ClientManager:

    def __init__(self, server):
        self.server = server

        self.activeClients = dict()  # A client is asociated with the lifetime of a socket
        self.persistentSessions = dict()  # A socket is associated with a client id

        self.retainMessages = dict()  # Here we store the retain messages

    def applyPachage(self, package, mySocket):
        if mySocket in self.activeClients:
            self.activeClients[mySocket].resetTime()

        if (package.type == PacketType.CONNECT):
            self.ProcessConnect(package, mySocket)
        elif (package.type == PacketType.SUBSCRIBE):
            self.ProcessSubscribe(package, mySocket)
        elif (package.type == PacketType.PUBLISH):
            self.ProcessPublish(package, mySocket)
        elif (package.type == PacketType.DISCONNECT):
            self.ProcessDisconnected(package, mySocket)
        elif (package.type == PacketType.PINGREQ):
            self.ProcessPINGREQ(package, mySocket)
        elif (package.type == PacketType.PINGRESP):
            print(f"{bcol.OKBLUE}Received ping from client.{bcol.ENDC}")
        elif (package.type == PacketType.UNSUBSCRIBE):
            self.ProcessUNSUBSCRIBE(package, mySocket)

    # Logica de raspuns pentru diferite pachete

    def keepAliveCheck(self):
        for client in self.activeClients.values():
            if client.deadline  <= time.time() and client.ping_sent is False:

                newPackage = Package()
                newPackage.type = PacketType.PINGREQ  # Noi trimitem request daca trece prea mult timp ?
                data = newPackage.serialize()
                client.associatedSocket.send(data)
                client.ping_sent = True

                print(f"{bcol.WARNING}Checking client inactivity.{bcol.ENDC}")

            elif client.ext_deadline <= time.time():
                print("sa produs si asta")
                self.clientSocketFailed(client.associatedSocket)

    def ProcessConnect(self, package, mySocket):
        # Presupunem ca nu exista sesiune
        sessionAlreadyExisted = False

        ## CLIENT HANDDLELING ##

        # Clientul este un obiect care exista doar pe parcursul conectiuni !!
        if mySocket in self.activeClients:
            raise "This client has not been properly disconected last time."

        # Cream o structura de date de tip client
        newClient = Client(package.client_id, mySocket, package.keep_alive)
        self.activeClients[mySocket] = newClient  # Fiecare client este asociat strict unui socket

        ## SESSION HANDDLELING ##
        if package.clearSession:  # Daca clear session este setat pe 1
            if package.client_id in self.persistentSessions:
                del self.persistentSessions[package.client_id]  # Daca gasim o sesiune, o stergem

            newSession = Sesion(persistent=False)  # apoi acream o sesiune fara persistenta
            newClient.associatedSession = newSession  # Asociem momentan clientul cu sesiunea
        else:  # Daca clear session este setat pe 0
            if package.client_id not in self.persistentSessions:  # daca nu exista o sesiune existenta pentru client id-ul curent
                newSession = Sesion(persistent=True)  # cream o sesiune cu persistenta
                newClient.associatedSession = newSession  # Asociem momentan clientul cu sesiunea
                self.persistentSessions[package.client_id] = newSession  # Pastram sesiunea si persistent
            else:  # daca exista deja o sesiune, doar confirmam asta prin connack
                sessionAlreadyExisted = True
                newClient.associatedSession = self.persistentSessions[package.client_id]


        ##AUTENTIFICATION
        if package.password_flag and package.username_flag:
            if checkPassword( package.username , bytes(package.password , 'utf-8')):
                newClient.authenticated = True;
                print(f"{bcol.OKBLUE}Authentication successful{bcol.ENDC}")
            else:
                #raise RuntimeError("Autentification failed and I don't like that")
                print(f"{bcol.WARNING}Authentication failed.{bcol.ENDC}")

        # Calculate the time the client got into the system

        newClient.resetTime()

        ##WILL MESSAGE HANDDLELINGN ##

        if package.will_flag:
            newClient.willFlag = True
            newClient.willTopic = package.will_topic
            newClient.willMessage = package.will_message

        ## CONNACK ##

        newPackage = Package()
        newPackage.type = PacketType.CONNACK

        # We keep this data in order to form the CONNAK properly
        newPackage.clearSession = package.clearSession
        newPackage.sessionAlreadyExisted = sessionAlreadyExisted

        data = newPackage.serialize()
        mySocket.send(data)

    def ProcessSubscribe(self, package, mySocket):

        ## MEMORIZING SUBSCRIBE TOPICS ##
        ourClient = self.activeClients[mySocket]
        ourClient.associatedSession.addTopics(package.topicList)

        ## SUBACK ##
        newPackage = Package()
        newPackage.type = PacketType.SUBACK
        newPackage.packetIdentifier = package.packetIdentifier
        data = newPackage.serialize()
        mySocket.send(data)

        ## RETAIN FUCTIONALITY
        for topic in package.topicList:  # pentru toate topicurile primite, daca exista retain message pentru unul
            if topic in self.retainMessages:  # atunci trimite mesajul doar noului subcriber
                if self.retainMessages[topic][0] != '':   #Cand mesajul e gol, nu mai trimiti mesaje de ratain
                    self.publishRetainMessage(topic, self.retainMessages[topic], mySocket)

    def ProcessUNSUBSCRIBE(self, package, mySocket):
        ourClient = self.activeClients[mySocket]
        ourClient.associatedSession.removeTopics(package.topicList)

    def ProcessPublish(self, package, mySocket):
        self.publishMessage(package.topic_name, package.message)

        ## RETAIN FUCTIONALITY
        if package.retain:
            self.retainMessages[package.topic_name] = (package.message,package.QoS)

    def ProcessPINGREQ(self, package, mySocket):
        newPackage = Package()
        newPackage.type = PacketType.PINGRESP
        data = newPackage.serialize()
        mySocket.send(data)

    def ProcessDisconnected(self, package, mySocket):
        self.activeClients[mySocket].safelyDisconnected = True
        self.clientSafelyDisconnected(mySocket)

    # _________________________UTILITY FUCTIONS_________________________

    def publishMessage(self, topicName, message):
        for client in self.activeClients.values():
            session = client.associatedSession

            if topicName in session.subscribedTopics:
                newPackage = Package()
                newPackage.type = PacketType.PUBLISH
                newPackage.topic_name = topicName
                newPackage.message = message
                newPackage.QoS = 0

                data = newPackage.serialize()

                # If a client is subcribe to a topic it was it last will in, it will crash the server unless we ignore it.
                try:
                    client.associatedSocket.send(data)
                except:
                    pass


    def publishRetainMessage(self, topicName, retainMessage, mySocket):
        newPackage = Package()
        newPackage.type = PacketType.PUBLISH
        newPackage.topic_name = topicName
        newPackage.message = retainMessage[0]
        newPackage.retain = True
        newPackage.QoS = retainMessage[1]

        data = newPackage.serialize()
        mySocket.send(data)

    def clientSafelyDisconnected(self, mySocket):
        self.server.removeSocketFromList(mySocket)  # This is important is we don't want the select to go wild
        mySocket.close()
        self.activeClients.pop(mySocket)
        print(f"{bcol.OKBLUE}Client successfully disconnected.{bcol.ENDC}")

    def clientSocketFailed(self, mySocket):

        client = self.activeClients[mySocket]

        if client.willFlag:
            self.publishMessage(client.willTopic, client.willMessage)

        self.server.removeSocketFromList(mySocket)  # Eradicate the socket from the server list as well
        mySocket.close()
        self.activeClients.pop(mySocket)  # Delete the client

        print(f"{bcol.WARNING}Client unexpectedly disconnected.{bcol.ENDC}")

