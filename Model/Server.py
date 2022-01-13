import socket
import threading
import select

from Model.Tools import bcol, settings
from Model.Package import Package, readPackage
from Model.ClientManager import ClientManager

FORMAT = 'utf-8'


class MQTTServer:

    def __init__(self, tree,logs):
        settings.debugMode = False

        self.port = 1883  # Default MQTT Port

        self.socketList = list()
        self.clientManager = None

        self.running = False  # The status of the server

        self.serverIP = 0  # Ip used by the server
        self.serverSocket = None  # The socket used for listening to new clients
        self.serverThread = None
        self.receiveThread = None
        self.tree = tree
        self.logs=logs

        # Figure out primary ip of the machine. Will fail if weird network adapters are not turned off.
        hostname = socket.gethostname()
        self.serverIP = socket.gethostbyname(hostname)

        self.logs.insert(0,f"Server has taked IP: {self.serverIP}")

        # Here we format the adress
        self.addr = (self.serverIP, self.port)

        # Logica interna care manageriaza clienti
        self.clientManager = ClientManager(self)

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
            self.logs.insert(0,f"Unexpected {err=}, {type(err)=} is server startup.")
            raise
        else:
            self.logs.insert(0,f"Server bound on port {self.port} is starting.")

            self.running = True

    def startServer(self):
        # Server starts listenning on port
        try:
            self.serverSocket.listen()
        except BaseException as err:
            self.logs.insert(0,f"Unexpected {err=}, {type(err)=}.Thread is quitting.")
            return

        self.logs.insert(0,f"Server is listening on {self.addr}\n")

        # This is the main loop for new clients
        while True:

            try:
                conn, addr = self.serverSocket.accept()  # This fuction is BLOCKING

                # Here we add a new client
                self.socketList.append(conn)

            # this case if for quitting the loop once the socket has been closed because the socket is blocking
            except OSError as err:
                self.running = False
                break
            except BaseException as err:
                self.logs.insert(0,f"Unexpected {err=}, {type(err)=} in connecting client to address.")
                continue
            else:  # this case runs when no exception has occured
                self.logs.insert(0,f"Client on address {addr} successfully connected.")

        self.receiveThread.join()
        self.logs.insert(0,"Server has quit.")

    def handleClients(self):

        while self.running:
            if len(self.socketList) == 0:
                continue

            selectedSockets, _, _ = select.select(self.socketList, [], [], 1)
            self.clientManager.keepAliveCheck()

            if selectedSockets:
                for mySocket in selectedSockets:

                    try:
                        data = readPackage(mySocket)
                    except Exception as e:
                        self.clientManager.clientSocketFailed(mySocket)

                    else:
                        newPackage = Package()
                        newPackage.deserialize(data)

                        # this is the final objective
                        self.clientManager.applyPackage(newPackage, mySocket)

    def removeSocketFromList(self, socket):
        self.socketList.remove(socket)

    # This is not stupid, and actually very smart.
    def serverISKill(self):
        self.serverSocket.close()

        for socket in self.socketList:
            socket.close()

        self.running = False

