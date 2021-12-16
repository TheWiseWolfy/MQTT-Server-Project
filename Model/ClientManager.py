import time
from datetime import datetime

from Model.Tools import *
from Model.Client import Client
from Model.Session import Sesion
from Model.Package import Package


class ClientManager:
    activeClients = dict()
    sessions = dict()

    def __init__(self):
        pass

    def applyPachage(self, package, mySocket):
        # Daca detectam un pachet de tip CONNECT
        # cautam ID-ul clientului sa vedem daca inca mai exista in lista noasta de clienti
        # daca nu exista, cram un client nou, si asamblam pachetul CONNECT
        # pe care il trimitem inapoi tot aici

        if (package.type == PacketType.CONNECT):
            self.ProcessConnect(package, mySocket)

        if (package.type == PacketType.SUBSCRIBE):
            self.ProcessSUBSCRIBE(package, mySocket)

    # This fuction exists in case the client dies before sending a disconect.
    def disconectClientWithSocket(self, mySocket):
        del self.activeClients[mySocket]

    # Logica de raspuns pentru diferite pachete

    def keep_alive_check(self):
        for x in self.activeClients.values():
            if x.deadline <= time.time() and x.ping_sent == False:
                newPackage = Package()
                newPackage.type = PacketType.PUBREQ
                data = newPackage.serialize()
                print("sa produs")
                x.ping_sent=True
                # mySocket.send(data)
            elif x.ext_deadline <= time.time():
                print("sa produs si asta")
                del x
                pass

    def ProcessConnect(self, package, mySocket):
        # Flags for connack
        sessionAlreadyExisted = False

        ## CLIENT HANDDLELING ##

        # Clientul este un obiect care exista doar pe parcursul conectiuni !!
        if package.client_id in self.activeClients:
            raise "This client has not been properly disconected last time."

        # Cream o structura de date de tip client
        newClient = Client(package.client_id, package.keep_alive)
        newClient.associatedSocket = mySocket  # Aici asociem fiecare socket cu un client
        self.activeClients[mySocket] = newClient  # Fiecare client este identificat dupa socket-ul pe care sta ?

        ## SESSION HANDDLELING ##
        if package.clearSession:  # Daca clear session este setat pe 1
            if package.client_id in self.sessions:
                del self.sessions[package.client_id]  # Daca gasim o sesiune, o stergem

            newSession = Sesion(persistent=False)  # cream o sesiune noua menita sa fie temporara
            self.sessions[package.client_id] = newSession

        else:  # Daca clear session este setat pe 0
            if package.client_id not in self.sessions:  # daca nu exista o sesiune existenta pentru client id-ul curent
                newSession = Sesion(persistent=True)  # cream noi o sesiune si o asociem noului client
                self.sessions[package.client_id] = newSession
            else:  # daca exista deja o sesiune, doar confirmam asta prin connack
                sessionAlreadyExisted = True

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

        newClient.associatedSocket.send(data)

    def ProcessSUBSCRIBE(self, package, mySocket):

        # Here we should probably do important stuffs

        ## SUBACK ##

        newPackage = Package()
        newPackage.type = PacketType.SUBACK
        newPackage.packetIdentifier = package.packetIdentifier
        data = newPackage.serialize()
        mySocket.send(data)

        pass
