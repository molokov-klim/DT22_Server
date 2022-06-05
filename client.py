import socket

HEADER = 64
PORT = 9700
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SHUTDOWN_MESSAGE = '0P9o8I7u6Y5t'
SERVER = "188.127.239.39"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


cmd = input('Введите команду: ')

while True:
    if cmd == 'shutdown':
        send(SHUTDOWN_MESSAGE)
    else:
        client.send(bytes(cmd, "utf-8"))

