import socket
import sys
import threading

from Model.Client import Client

FORMAT = 'utf-8'
FIXED_HEADER = 16
DISCONNECT_MESSAGE = "!DISCONNECT"


class MQTTServer:
    header = 64
    port = 1883  # Default MQTT Port
    clients = list()  # A list of connected clients
    running = False # The status of the server

    serverIP = 0
    serverSocket = None  # The socket used for this server in particular
    serverConnectionsThread = None # We sitting on this socket, alright

    def __init__(self):
        # Figure out primary ip of the machine. Will fail if weird network adapters are not turned off.
        hostname = socket.gethostname()
        self.serverIP = socket.gethostbyname(hostname)
        print(f"Server has taked IP: {self.serverIP}")

        # Here we format the adress
        self.addr = (self.serverIP, self.port)

        # Here we bind the socket so we can use it for magic
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(self.addr)

        print(f"Server bound on port {self.port} is starting.")

        # We neet a thread for listening for new connections
        serverConnectionsThread = threading.Thread(target=self.start, args=())
        serverConnectionsThread.daemon = True
        serverConnectionsThread.start()

        self.running = True

    def start(self):
        self.serverSocket.listen()
        print(f"Server is listening on {self.serverSocket}")

        while self.running:
            conn, addr = self.serverSocket.accept()  # This fuction is BLOKING

            # Here we add a new client
            newClient = Client(conn, addr)
            self.clients.append(newClient)

            print(f"Client on adress {addr} successfully connected.")

            # Here we start observing the incomming messages from the client
            newClient.thread = threading.Thread(target=self.handle_client, args=[newClient])
            newClient.thread.daemon = True
            newClient.thread.start()
        print(f"Server has quit.")

    # What we do when we have a new connection
    def handle_client(self, client):
        print(f"Thead for client {client.adress} has started.")

        client.connected = True

        # here we handle individual messages
        while client.connected:
            client.ReadMQTTPackage()

            # What we do after that, only god will know
            # msg_length:
            #    msg_length = int(msg_length)
            # Variable header interaction
            #    msg = conn.recv(msg_length).decode(FORMAT)
            #    print(f"[{addr}] {msg}")
            # call to clone interaction
            #    if msg == DISCONNECT_MESSAGE:
            #       clintConnected = False
            #       self.clientSpckets.remove(conn)
        client.conn.close()

        print(f"Thead for client {client.adress} has quit.")

    #This is stupid and wrong and should have not been written
    def serverISKill(self):
        for client in self.clients:
            client.socket.close()
            pass

        self.serverSocket.close()

