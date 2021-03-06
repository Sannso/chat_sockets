import threading
import socket

# constants
DISCONNECT_COMMAND = '/disconnect'
HEADER_LENGTH = 10
FORMAT = 'utf-8'
IP = '127.0.1.1'
PORT = 1234
SERVER_ADDRESS = (IP, PORT)
print("[SERVER] Starting Server...")

# creating and listening to socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen()

# clients information
clients = {} # {client_socket: {'username': username, 'address': address}}
messages = [] #


def close_connection(client_socket):
    print(f"[DISCONNECTION] {clients[client_socket]['username']} has disconnected!")
    del clients[client_socket]
    client_socket.close()

def send_message(socket, message):
    try:
        socket.send(bytes(f"{len(message):<{HEADER_LENGTH}}", FORMAT))
        socket.send(bytes(message, FORMAT))
    except:
        print(f"[ERROR] SENDING '{message}' to {clients[socket]['username']}")

def send_file(socket, file):
    try:
        data = open(file, "rb")
        socket.send(bytes(f"{len(data):<{HEADER_LENGTH}}", FORMAT))
        socket.send(data)
    except:
        print(f"[ERROR] SENDING FILE '{file}' to {clients[socket]['username']}")

def receive_message(client_socket):
    while True:
        message_length = client_socket.recv(HEADER_LENGTH).decode(FORMAT)
        message = client_socket.recv(int(message_length)).decode(FORMAT)
        return message

def send_to_all_clients(message, sender_socket):
    user_message = f"{clients[sender_socket]['username']} > {message}"
    messages.append((clients[sender_socket]['username'], message))
    print(user_message)
    for client_socket in clients:
        if sender_socket != client_socket:
            send_message(client_socket, user_message)

def handle_client(client_socket, client_address):
    # user name and server prompt for new connections
    username = receive_message(client_socket)
    clients[client_socket] = {'username': username, 'address': client_address}
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    print(f"[NEW CONNECTION] {username} has connected!")

    # server prompt for connection, and receiving previous messages of server.
    send_message(client_socket, f'You have connected to the server with the username "{clients[client_socket]["username"]}"!')
    send_message(client_socket, str(len(messages))) # sending of previous messages to new client
    for i in range(len(messages)):
        send_message(client_socket, f"<{messages[i][0]}> {messages[i][1]}")

    # receiving messages and sending it to other clients
    connected = True
    while connected:
        try:
            message = receive_message(client_socket)
            if message == DISCONNECT_COMMAND:
                connected = False

            send_to_all_clients(message, client_socket)

        except:
            connected = False

    close_connection(client_socket)

# listening for clients
print("[LISTENING] Listening for Clients")
while True:
    client_socket, client_address = server_socket.accept()
    handling_thread = threading.Thread(target=handle_client, args=[client_socket, client_address])
    handling_thread.start()