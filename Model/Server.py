import socket
import sys
import threading

import time

FORMAT = 'utf-8'
HEADER = 16
DISCONNECT_MESSAGE = "!DISCONNECT"


class MQTTServer:
    header = 64
    port = 1883  # Default MQTT Port

    clientSpckets = list() # A list of connected clients
    serverSocket = None

    def __init__(self):

        # Figure out primary ip of the machine.
        hostname = socket.gethostname()
        serverIP = socket.gethostbyname(hostname)
        print(serverIP)

        self.addr = (serverIP, self.port)

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
            self.clients.append(conn)

            #Here we start observing the incomming messages from the client
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

            print(self.clients)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION ]{addr} connected.")

        connected = True;
        while connected:
            #Initial fixed header interaction
            msg_lenght = conn.recv(HEADER).decode(FORMAT)

            if msg_lenght:
                msg_lenght = int(msg_lenght)

                #Variable header interaction
                msg = conn.recv(msg_lenght).decode(FORMAT)
                print(f"[{addr}] {msg}")

                #call to clone interaction
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    self.clients.remove(conn)
        conn.close()


def main() -> int:
    MQTTServer()

    while (True):
        print("Say cheese")
        time.sleep(3)

    return 0


if __name__ == '__main__':
    sys.exit(main())
