import socket
import sys
import threading

#for your enjoyment https://docs.python.org/3/library/socket.html

HEADER = 64
PORT = 5050
SERVER_IP = "192.168.0.113"
ADDR = (SERVER_IP, PORT);

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION ]{addr} connected.")

    connected = True;
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)

            msg = conn.recv(msg_lenght).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

    conn.close()

def start(server):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while True:
        conn ,addr = server.accept()      # This fuction is BLOKING
        thread = threading.Thread (target=handle_client, args=(conn, addr))
        thread.start()
        print( f"[Active connections]{threading.active_count() - 1}")

def main() -> int:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print("[STARTING] server is starting...")
    start(server)
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit

