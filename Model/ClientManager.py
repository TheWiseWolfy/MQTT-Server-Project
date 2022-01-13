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

        self.activeClients = dict()  # A client is associated with the lifetime of a socket
        self.persistentSessions = dict()  # A socket is associated with a client id

        self.retainMessages = dict()  # Here we store the retain messages
        self.savedMessages = dict()  # Here we store saved messages for the QoS system
        self.topicEntry = dict()  # Here we store each topic's messages

    def applyPackage(self, package, mySocket):
        if mySocket in self.activeClients:
            self.activeClients[mySocket].resetTime()

        if package.type == PacketType.CONNECT:
            self.ProcessConnect(package, mySocket)
        elif package.type == PacketType.SUBSCRIBE:
            self.ProcessSubscribe(package, mySocket)
        elif package.type == PacketType.PUBLISH:
            self.ProcessPublish(package, mySocket)
        elif package.type == PacketType.PUBACK:
            self.ProcessPUBACK(package, mySocket)
        elif package.type == PacketType.DISCONNECT:
            self.ProcessDisconnected(package, mySocket)
        elif package.type == PacketType.PINGREQ:
            self.ProcessPINGREQ(package, mySocket)
        elif (package.type == PacketType.PINGRESP):
            print(f"{bcol.OKBLUE}Received ping from client.{bcol.ENDC}")
        elif (package.type == PacketType.UNSUBSCRIBE):
            self.ProcessUNSUBSCRIBE(package, mySocket)
        elif package.type == PacketType.PUBREL:
            self.ProcessPUBREL(package, mySocket)
        elif package.type == PacketType.PUBREC:
            self.ProcessPUBREC(package, mySocket)
        elif package.type == PacketType.PUBCOMP:
            self.ProcessPUBCOMP(package, mySocket)
        elif package.type == PacketType.PINGRESP:
            self.server.logs.insert(0, f"Received ping from client.")

    # Logica de raspuns pentru diferite pachete

    def keepAliveCheck(self):
        for client in self.activeClients.values():
            if client.ext_deadline <= time.time():
                self.clientSocketFailed(client.associatedSocket)

    def ProcessConnect(self, package, mySocket):
        # Presupunem ca nu exista sesiune
        sessionAlreadyExisted = False

        ## CLIENT HANDLING ##

        # Clientul este un obiect care exista doar pe parcursul conectiuni !!
        if mySocket in self.activeClients:
            raise "This client has not been properly disconected last time."

        # Cream o structura de date de tip client
        newClient = Client(package.client_id, mySocket, package.keep_alive)
        self.activeClients[mySocket] = newClient  # Fiecare client este asociat strict unui socket

        ## SESSION HANDLING ##
        if package.clearSession:  # Daca clear session este setat pe 1
            if package.client_id in self.persistentSessions:
                del self.persistentSessions[package.client_id]  # Daca gasim o sesiune, o stergem

            newSession = Sesion(persistent=False)  # apoi cream o sesiune fara persistenta
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
            if checkPassword(package.username, bytes(package.password, 'utf-8')):
                newClient.authenticated = True;
                print(f"{bcol.OKBLUE}Authentication successful{bcol.ENDC}")
            else:
                # raise RuntimeError("Autentification failed and I don't like that")
                print(f"{bcol.WARNING}Authentication failed.{bcol.ENDC}")

        # Calculate the time the client got into the system

        newClient.resetTime()

        ## WILL MESSAGE HANDLING ##

        if package.will_flag:
            newClient.willFlag = True
            newClient.willTopic = package.will_topic
            newClient.willMessage = package.will_message
            newClient.willQoS = package.will_qos

        ## CONNACK ##

        newPackage = Package()
        newPackage.type = PacketType.CONNACK

        # We keep this data in order to form the CONNACK properly
        newPackage.clearSession = package.clearSession
        newPackage.sessionAlreadyExisted = sessionAlreadyExisted

        data = newPackage.serialize()
        mySocket.send(data)

        self.server.tree.event_generate("<<CONNECT>>")

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
        for topic in package.topicList:

            # pentru toate topicurile primite, daca exista retain message pentru unul

            if topic in self.retainMessages:  # atunci trimite mesajul doar noului subcriber
                if self.retainMessages[topic][0] != '':  # Cand mesajul e gol, nu mai trimiti mesaje de ratain
                    self.publishRetainMessage(topic, self.retainMessages[topic], mySocket)

            if topic not in self.topicEntry:
                self.topicEntry[topic] = list()
        self.server.logs.insert(0,
                                f"Client {self.activeClients[mySocket].clientID} subscribed to topic {package.topicList}.")

        self.server.tree.event_generate("<<SUBSCRIBE>>")

    def ProcessUNSUBSCRIBE(self, package, mySocket):
        ourClient = self.activeClients[mySocket]
        ourClient.associatedSession.removeTopics(package.topicList)

    def ProcessPublish(self, package, mySocket):
        self.server.logs.insert(0, f"Received PUBLISH packet from {self.activeClients[mySocket].clientID}.")
        if package.QoS == 0:
            self.publishMessage(package.topicName, package.message, package.QoS)

        if package.QoS == 1:
            self.savedMessages[mySocket] = package.packetIdentifier
            self.publishMessage(package.topicName, package.message, package.QoS)
            newPackage = Package()
            newPackage.type = PacketType.PUBACK
            newPackage.packetIdentifier = package.packetIdentifier

            data = newPackage.serialize()
            mySocket.send(data)

        if package.QoS == 2:
            self.savedMessages[mySocket] = package.packetIdentifier
            self.publishMessage(package.topicName, package.message, package.QoS)
            newPackage = Package()
            newPackage.type = PacketType.PUBREC
            newPackage.packetIdentifier = package.packetIdentifier

            data = newPackage.serialize()
            mySocket.send(data)

        self.addInDict(self.topicEntry, package.topicName, package.message)
        ## RETAIN FUCTIONALITY
        if package.retain:
            self.retainMessages[package.topicName] = (package.message, package.QoS)

        self.server.tree.event_generate("<<PUBLISH>>")

    def ProcessPUBACK(self, package, mySocket):
        for key in self.savedMessages.keys():
            if key.values() == package.packetIdentifier:
                self.savedMessages.pop(key, None)

    def ProcessPUBREL(self, package, mySocket):

        newPackage = Package()
        newPackage.type = PacketType.PUBCOMP
        newPackage.packetIdentifier = package.packetIdentifier

        data = newPackage.serialize()
        mySocket.send(data)
        self.server.logs.insert(0,
                                f"Received PUBREL from {self.activeClients[mySocket].clientID}, responded with PUBCOMP.")

    def ProcessPUBCOMP(self, package, mySocket):

        self.server.logs.insert(0,
                                f"Received PUBCOMP from {self.activeClients[mySocket].clientID}.")

    def ProcessPUBREC(self, package, mySocket):
        for key in self.savedMessages.keys():
            if key.values() == package.packetIdentifier:
                self.savedMessages.pop(key, None)

        newPackage = Package()
        newPackage.type = PacketType.PUBREL
        newPackage.packetIdentifier = package.packetIdentifier

        data = newPackage.serialize()
        mySocket.send(data)
        self.server.logs.insert(0,
                                f"Received PUBREC from {self.activeClients[mySocket].clientID}, responded with PUBREL.")

    def ProcessPINGREQ(self, package, mySocket):
        newPackage = Package()
        newPackage.type = PacketType.PINGRESP
        data = newPackage.serialize()
        mySocket.send(data)
        self.server.logs.insert(0,
                                f"Received PINGREQ from {self.activeClients[mySocket].clientID}, responded with PINGRESP.")

    def ProcessDisconnected(self, package, mySocket):
        self.activeClients[mySocket].safelyDisconnected = True
        self.clientSafelyDisconnected(mySocket)

    # _________________________UTILITY FUNCTIONS_________________________

    def publishMessage(self, topicName, message, qos):
        for client in self.activeClients.values():
            session = client.associatedSession

            if topicName in session.subscribedTopics:
                newPackage = Package()
                newPackage.type = PacketType.PUBLISH
                newPackage.topicName = topicName
                newPackage.message = message
                newPackage.QoS = qos

                data = newPackage.serialize()
                # If a client is subcribe to a topic it was it last will in, it will crash the server unless we ignore it.
                try:
                    client.associatedSocket.send(data)
                except:
                    pass
        self.server.logs.insert(0,
                                f"Sent PUBLISH packet with the topic '{topicName}',the message '{message}' and QoS {qos}.")

    def publishRetainMessage(self, topicName, retainMessage, mySocket):
        newPackage = Package()
        newPackage.type = PacketType.PUBLISH
        newPackage.topicName = topicName
        newPackage.message = retainMessage[0]
        newPackage.retain = True
        newPackage.QoS = retainMessage[1]

        data = newPackage.serialize()
        mySocket.send(data)
        self.server.logs.insert(0,
                                f"Published retain message {retainMessage[0]}, topic {topicName} and QoS {retainMessage[1]}.")

    def clientSafelyDisconnected(self, mySocket):
        self.server.logs.insert(0, f"Client {self.activeClients[mySocket].clientID} successfully disconnected.")
        self.server.removeSocketFromList(mySocket)  # This is important is we don't want the select to go wild
        mySocket.close()
        self.activeClients.pop(mySocket)
        self.server.tree.event_generate("<<DISCONNECT>>")

    def clientSocketFailed(self, mySocket):

        client = self.activeClients[mySocket]

        if client.willFlag:
            self.publishMessage(client.willTopic, client.willMessage, client.willQoS)
            self.server.logs.insert(0,
                                    f"Client {self.activeClients[mySocket].clientID} Last Will message:{client.willMessage}.")

        self.server.removeSocketFromList(mySocket)  # Eradicate the socket from the server list as well
        mySocket.close()
        self.activeClients.pop(mySocket)  # Delete the client

        self.server.logs.insert(0, f"Client {self.activeClients[mySocket].clientID} unexpectedly disconnected.")

    def addInDict(self, dict, key, values):
        if key not in dict:
            dict[key] = list()
        dict[key].append(str(values))
        return dict
