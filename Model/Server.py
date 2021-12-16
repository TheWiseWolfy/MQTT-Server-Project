import socket
import threading
import select

from Model.Tools import bcol
from Model.Package import Package, readPackage
from Model.ClientManager import ClientManager

FORMAT = 'utf-8'


class MQTTServer:
    port = 1883  # Default MQTT Port

    socketList = list()
    clientManager = None

    running = False  # The status of the server

    serverIP = 0  # Ip used by the server
    serverSocket = None  # The socket used for listening to new clients
    serverThread = None
    receiveThread = None

    def __init__(self):
        # Figure out primary ip of the machine. Will fail if weird network adapters are not turned off.
        hostname = socket.gethostname()
        self.serverIP = socket.gethostbyname(hostname)

        print(f"{bcol.OKBLUE}Server has taked IP: {self.serverIP}{bcol.ENDC}")

        # Here we format the adress
        self.addr = (self.serverIP, self.port)

        # Logica interna care manageriaza clienti
        self.clientManager = ClientManager()

        # Here we bind the socket so we can use it for magic
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind(self.addr)

            # We need a thread for listening for new connections
            self.serverThread = threading.Thread(target=self.startServer, args=())
            self.serverThread.start()

            self.receiveThread = threading.Thread(target=self.handleClients, args=())
            self.receiveThread.start()
        except BaseException as err:
            print(f"{bcol.WARNING} Unexpected {err=}, {type(err)=} is server startup.{bcol.ENDC}")
            raise
        else:
            print(f"Server bound on port {self.port} is starting.")

            self.running = True

    def startServer(self):
        # Server starts listenning on port
        try:
            self.serverSocket.listen()
        except BaseException as err:
            print(f"{bcol.WARNING}Unexpected {err=}, {type(err)=}.Thread is quitting.{bcol.ENDC}")
            return

        print(f"Server is listening on {self.addr}\n")

        # This is the main loop for new clients
        while True:

            try:
                conn, addr = self.serverSocket.accept()  # This fuction is BLOKING

                # Here we add a new client
                self.socketList.append(conn)

            except OSError as err:
                self.running = False
                break  # this case if for quitting the loop once the socket has been closed
            except BaseException as err:
                print(f"{bcol.WARNING}Unexpected {err=}, {type(err)=} in starting client on adress.{bcol.ENDC}\n")
                continue
            else:  # this case runs when no exception has occured
                print(f"{bcol.OKBLUE}Client on address {addr} successfully started.{bcol.ENDC}")

        self.receiveThread.join()
        print(f"Server has quit.")

    def handleClients(self):

        while self.running:
            if len(self.socketList) == 0:
                continue

            selectedSockets, _, _ = select.select(self.socketList, [], [], 1)
            self.clientManager.keep_alive_check()

            if selectedSockets:
                for mySocket in selectedSockets:
                    data = readPackage(mySocket)

                    if not data:
                        # cand ajungem aici PRESUPUNEM ca pachetul de disconec a fost primti deja
                        self.socketList.remove(mySocket)
                        self.clientManager.disconectClientWithSocket(mySocket)
                        mySocket.close()

                    else:
                        newPackage = Package()
                        newPackage.deserialize(data)

                        # this is the final objective
                        self.clientManager.applyPachage(newPackage, mySocket)


    # This is not stupid, and actually very smart.
    def serverISKill(self):
        self.serverSocket.close()

        for client in self.socketList:
            client.close()
        self.running = False
