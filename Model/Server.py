import socket
import sys
import threading

from Model.FIxedHeader import ProcessFixedHeader

FORMAT = 'utf-8'
FIXED_HEADER = 16
DISCONNECT_MESSAGE = "!DISCONNECT"

class MQTTServer:
    header = 64
    port = 1883  # Default MQTT Port

    serverIP = 0;
    clientSpckets = list()  # A list of connected clients
    serverSocket = None  # The socjet used for this server in particular

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
        thread = threading.Thread(target=self.start, args=())
        thread.start()

    def start(self):
        self.serverSocket.listen()
        print(f"Server is listening on {self.serverSocket}")

        while True:
            conn, addr = self.serverSocket.accept()  # This fuction is BLOKING
            print(f"Client on adress {addr} successfully connected.")
            self.clientSpckets.append(conn)

            # Here we start observing the incomming messages from the client
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

            print(self.clientSpckets)

    # What we do when we have a new connection
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION ]{addr} connected.")

        clintConnected = True;

        # here we handle individual messages
        while clintConnected:
            # Initial fixed header interaction
            fixedHeader = conn.recv(FIXED_HEADER)

            print(f"\n{fixedHeader}")

            # Here we process the fixed header.
            ProcessFixedHeader(fixedHeader)

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

        conn.close()

