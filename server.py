import socket
import threading

HEADER = 1024  # Длина сообщения в байтах
PORT = 9700  # Порт сервера
SERVER = '188.127.239.39'  # socket.gethostbyname(socket.gethostname()) # IP адрес сервера
SERVER_ADDRESS = (SERVER, PORT)  # Адрес сервера в виде tuple IP, порт
FORMAT = 'utf-8'  # формат преобразования текста по умолчанию
SHUTDOWN_MESSAGE = '0P9o8I7u6Y5t'  # сообщение для удаленного выключения сервера

SESSION_LIST = {}  # лист открытых сессий
CONNECTION_LIST = {}  # лист с открытыми подключениями

# DATA = '0'  # сообщение от клиента
# METHOD = '0'  # первая часть сообщения - метод
# TOKEN = '0'  # вторая часть сообщения - токен
# IP = '0'  # третья часть сообщения - IP
# DIRECTION = '0'  # четвертая часть сообщения - направление

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen(500)  # подключений одновременно
except KeyboardInterrupt:
    server.close()
    print('shutdown')
    exit()


def server_start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    connected = True
    while connected:
        data = client_socket.recv(HEADER).decode(FORMAT)

        try:
            method = data.split()[0]
        except:
            print('No have data[0]')
        try:
            token = data.split()[1]
        except:
            print('No have data[1]')
        try:
            direction = data.split()[2]
        except:
            print('No have data[2]')

        if method == "startSession":
            start_session(token, client_socket, client_address)
            client_socket.send(bytes("startSessionOK", "utf-8"))

        elif method == "stopSession":
            stop_session(token)
            client_socket.send(bytes("stopSessionOK", "utf-8"))
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        elif method == "connectSession":
            connect_session(token, client_socket, client_address)
            client_socket.send(bytes("connectSessionOK", "utf-8"))

        elif method == "disconnectSession":
            disconnect_session(token)
            client_socket.send(bytes("disconnectSessionOK", "utf-8"))
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()

        elif method == "rotate":
            rotate(token, direction, client_socket, client_address)
            client_socket.send(bytes("rotateOK", "utf-8"))

        elif method == SHUTDOWN_MESSAGE:
            server.close()
            exit()

        else:
            print(client_socket, client_address, data)

        client_socket.send(f"Message {data} received by server".encode(FORMAT))

        if method != "startSession":
            client_socket.close()


        data = ''
        method = ''
        token = ''
        ip = ''
        direction = ''

    client_socket.close()


def check_in_dict(key, dictionary):
    if dictionary.get(key, False) != False:
        return True
    else:
        return False


def start_session(token, client_socket, client_address):
    print("start session")
    SESSION_LIST[token] = [client_socket, client_address]
    print('SESSION_LIST: ' + SESSION_LIST)


def stop_session(token):
    print("stop session")
    if check_in_dict(token, SESSION_LIST):
        SESSION_LIST.pop(token, 'bebeka')
    print('SESSION_LIST: ' + SESSION_LIST)


def connect_session(token, client_socket, client_address):
    print("connect session")
    if check_in_dict(token, SESSION_LIST):
        CONNECTION_LIST[token] = [client_socket, client_address]
    print('CONNECTION_LIST: ' + CONNECTION_LIST)


def disconnect_session(token):
    print("disconnect session")
    if check_in_dict(token, CONNECTION_LIST):
        CONNECTION_LIST.pop(token, 'memeka')
    print('CONNECTION_LIST: ' + CONNECTION_LIST)


def rotate(token, direction, client_socket, client_address):
    print("rotate")
    if check_in_dict(token, CONNECTION_LIST) == True:
        print("rotate")


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    server_start()
