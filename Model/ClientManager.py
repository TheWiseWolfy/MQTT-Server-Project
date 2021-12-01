from Model.Tools import *
from Model.Client import Client
from Model.Session import Sesion


class ClientManager:
    clients = dict()
    sessions = dict()

    def __init__(self):
        pass

    def applyPachage(self, package, socket):
        # Daca detectam un pachet de tip CONNECT
        # cautam ID-ul clientului sa vedem daca inca mai exista in lista noasta de clienti
        # daca nu exista, cram un client nou, si asamblam pachetul CONNECT
        # pe care il trimitem inapoi tot aici

        if (package.type == PacketType.CONNECT):
            newClient = None

            ## CLIENT HANDDLELING ##

            if package.client_id not in self.clients:
                newClient = Client(package.client_id)
                self.clients[package.client_id] = newClient
            else:
                raise "this is not allowed buddy"


            ## SESSION HANDDLELING ##
            if package.clearSession:        # Daca clear session este setat pe 1
                if package.client_id in self.sessions:
                    del self.sessions[package.client_id]

                newSession = Sesion(persistent=False)       #cream o sesiune noua menita sa fie temporara
                self.sessions[package.client_id] = newSession
                newClient.currentSession = newSession
            else:                            # Daca clear session este setat pe 0
                if package.client_id not in self.sessions:       #daca nu exista o sesiune existenta pentru client id-ul curent

                    newSession = Sesion(persistent=True)        #cream noi o sesiune si o asociem noului client
                    self.sessions[package.client_id] = newSession
                    newClient.currentSession = newSession
                else:                                            #daca exista deja o sesiune, doar o reasociem
                    newClient.currentSession = self.sessions[package.client_id]

            ##WILL MESSAGE HANDDLELINGN ##

            if package.will_flag:
                newClient.willFlag = True
                newClient.willMessage = "I guess someone forgot to implement the actual WILL MESSAGEEEEEEEEEEE"

