import socket
import threading

from Model.Client import Client
from Model.Tools import bcolors

FORMAT = 'utf-8'
FIXED_HEADER = 16
DISCONNECT_MESSAGE = "!DISCONNECT"


class MQTTServer:
    port = 1883  # Default MQTT Port
    clients = list()  # A list of connected clients
    running = False  # The status of the server

    serverIP = 0  # Ip used by the server
    serverSocket = None  # The socket used for listening to new clients
    serverConnectionsThread = None

    def __init__(self):
        # Figure out primary ip of the machine. Will fail if weird network adapters are not turned off.
        hostname = socket.gethostname()
        self.serverIP = socket.gethostbyname(hostname)

        print(f"{bcolors.OKBLUE }Server has taked IP: {self.serverIP}{bcolors.ENDC}")

        # Here we format the adress
        self.addr = (self.serverIP, self.port)

        # Here we bind the socket so we can use it for magic
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind(self.addr)

            # We need a thread for listening for new connections
            serverConnectionsThread = threading.Thread(target=self.start, args=())
            serverConnectionsThread.daemon = True
            serverConnectionsThread.start()
        except BaseException as err:
            print(f"{bcolors.WARNING} Unexpected {err=}, {type(err)=} is server startup.{bcolors.ENDC}")
            raise

        print(f"Server bound on port {self.port} is starting.")
        self.running = True

    def start(self):
        # Server starts listenning on port
        try:
            self.serverSocket.listen()
        except BaseException as err:
            print(f"{bcolors.WARNING}Unexpected {err=}, {type(err)=}.Thread is quitting.{bcolors.ENDC}")
            return

        print(f"Server is listening on {self.addr}\n")

        while self.running:
            # Here we start observing the incomming messages from the client
            try:
                conn, addr = self.serverSocket.accept()  # This fuction is BLOKING

                # Here we add a new client
                newClient = Client(conn, addr)

                newClient.thread = threading.Thread(target=self.handleClient, args=[newClient])
                newClient.thread.daemon = True
                newClient.thread.start()

                self.clients.append(newClient)
            except BaseException as err:
                print(f"{bcolors.WARNING}Unexpected {err=}, {type(err)=} in starting client on adress {addr}.{bcolors.ENDC}\n")
                continue

            print(f"{bcolors.OKBLUE}Client on address {addr} successfully started.{bcolors.ENDC}")

        print(f"Server has quit.")

    # What we do when we have a new connection
    def handleClient(self, client):
        print(f"Client on adress {client.adress} is starting.\n")
        client.connected = True

        # here we handle individual messages
        while client.connected:
            try:
                byteArray = client.socket.recv(8, socket.MSG_PEEK)  # This is blocking
                if len(byteArray) == 0:
                    print(f"Socket has quit");
                    break

                client.ReadMQTTPackage()
            except BaseException as err:
                print(f"{bcolors.WARNING}Unexpected {err=}, {type(err)=} in packet processing on {client.adress}{bcolors.ENDC}\n")
                continue

        client.connected = False
        client.socket.close()
        print(f"Thead for client {client.adress} has quit.")

    # This is probably stupid, can't say tho.
    def serverISKill(self):
        for client in self.clients:
            client.socket.close()
            pass

        self.serverSocket.close()

