import os
import socket
import threading

# Server Information
SERVER_ADDRESS = ('127.0.1.1', 1234)
HEADER_LENGTH = 10
FORMAT = 'utf-8'
DISCONNECT_COMMAND = '/disconnect'
SEND_FILE_COMMAND = '/file'

def send_message(message):
    message_length = f"{len(message):<{HEADER_LENGTH}}"
    client_socket.send(bytes(message_length, FORMAT))
    if type(message) == bytes:
        client_socket.send(message)
    else:
        client_socket.send(bytes(message, FORMAT))

def send_file(path):
    send_message("/file")
    file = open(path, "rb")
    send_message(os.path.split(path)[1])
    message = file.read()
    send_message(message)
    file.close()

def receive_file(filename, data):
    file = open(filename, "wb")
    file.write(data)
    file.close()
    print("El archivo fue guardado en la misma carpeta del programa.")

def receive_message(decode = True):
    while True:
        message_length = client_socket.recv(HEADER_LENGTH).decode(FORMAT)
        if message_length:
            if decode:
                message = client_socket.recv(int(message_length)).decode(FORMAT)
            else:
                message = client_socket.recv(int(message_length))
            return message

def receive_messages_in_real_time():
    while True:
        message = receive_message()
        if message == SEND_FILE_COMMAND:
            filename = receive_message()
            data = receive_message(decode=False)
            receive_file(filename, data)
        else:
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
    elif str.split(message)[0] == SEND_FILE_COMMAND:
        try:
            send_file(str.split(message)[1])
        except:
            print("Hubo en error al cargar el archivo. Recuerda que para usar este comando: /file ruta_del_archivo")
    else:
        send_message(message)