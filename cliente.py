import socket
import threading

# Server Information
SERVER_ADDRESS = ('127.0.1.1', 1234)
HEADER_LENGTH = 10
FORMAT = 'utf-8'
DISCONNECT_COMMAND = '/disconnect'

def send_message(message):
    message_length = f"{len(message):<{HEADER_LENGTH}}"
    client_socket.send(bytes(message_length, FORMAT))
    client_socket.send(bytes(message, FORMAT))


def receive_message():
    while True:
        message_length = client_socket.recv(HEADER_LENGTH).decode(FORMAT)
        if message_length:
            message = client_socket.recv(int(message_length)).decode(FORMAT)
            return message


def receive_messages_in_real_time():
    while True:
        message = receive_message()
        print(message)


# Connecting to Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(SERVER_ADDRESS)

# Username Prompt
username = input("Enter your username:\n")
send_message(username)

# Server Message for successful connection, and previous messages in server
print(receive_message())
number_of_messages = receive_message()
for _ in range(int(number_of_messages)):
    print(receive_message())

# thread for receiving messages
receiving_thread = threading.Thread(target=receive_messages_in_real_time)
receiving_thread.daemon = True
receiving_thread.start()

# messaging in the server
connected = True
while connected:
    message = input(f"<Me> ")
    if message == DISCONNECT_COMMAND:
        send_message(f"The user {username} has disconnected!")
        connected = False
    else:
        send_message(message)