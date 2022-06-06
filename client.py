import socket

HEADER = 64
PORT = 9700
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SHUTDOWN_MESSAGE = '0P9o8I7u6Y5t'
SERVER = "188.127.239.39"
ADDR = (SERVER, PORT)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(ADDR)




while True:
    cmd = input('Введите команду: ')
    if cmd == 'shutdown':
        send(SHUTDOWN_MESSAGE)
    else:
        socket.send(cmd.encode(FORMAT))
    try:
        msg = socket.recv(1024)
        print(msg.decode("utf-8"))
    except:
        print('No have data')
    
