import socket

HEADER = 64
PORT = 9700
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SHUTDOWN_MESSAGE = '0P9o8I7u6Y5t'
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(ADDR)


loop = True

while loop:
    cmd = input('Введите команду: ')
    if cmd == 'shutdown':
        send(SHUTDOWN_MESSAGE)
    elif cmd == 'stopSession':
        socket.send(cmd.encode(FORMAT))
        socket.shutdown(socket.SHUT_WR)
        socket.close()
        loop = False
    else:
        socket.send(cmd.encode(FORMAT))
    try:
        msg = socket.recv(1024)
        print(msg.decode("utf-8"))
    except:
        print('No have data')
    
