import socket
import threading

HEADER = 1024  # Длина сообщения в байтах
PORT = 9700  # Порт сервера
# SERVER = '127.0.0.1'
SERVER = socket.gethostbyname(socket.gethostname())  # IP адрес сервера
SERVER_ADDRESS = (SERVER, PORT)  # Адрес сервера в виде tuple IP, порт
FORMAT = 'utf-8'  # формат преобразования текста по умолчанию
SHUTDOWN_MESSAGE = '0P9o8I7u6Y5t'  # сообщение для удаленного выключения сервера

SESSION_LIST = {}  # лист открытых сессий
CONNECTION_LIST = {}  # лист с открытыми подключениями

#data, method, token, ip, direction = ('' for _ in range(5))

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # overcome the "Address already in use"
    server.bind(SERVER_ADDRESS)
    server.listen(500)  # подключений одновременно
except KeyboardInterrupt:
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
        except IndexError:
            print('No have data[0]')
        try:
            token = data.split()[1]
        except IndexError:
            print('No have data[1]')
        try:
            direction = data.split()[2]
        except IndexError:
            print('No have data[2]')

        if method == "startSession":
            start_session(token, client_socket, client_address)

        elif method == "stopSession":
            stop_session(token, client_socket)
            connected = False

        elif method == "connectSession":
            connect_session(token, client_socket, client_address)

        elif method == "disconnectSession":
            disconnect_session(token, client_socket)

        elif method == "rotate":
            rotate(token, direction, client_socket)

        elif method == SHUTDOWN_MESSAGE:
            server.shutdown(socket.SHUT_WR)
            server.close()
            exit()

        else:
            client_socket.send(bytes("unknown", "utf-8"))

        # client_socket.send(f"Message {data} received by server".encode(FORMAT))

        data, method, token, ip, direction = ('' for _ in range(5))

    client_socket.close()


def check_in_dict(key, dictionary):
    if dictionary.get(key, False):
        return True
    else:
        return False


def start_session(arg_token, arg_client_socket, arg_client_address):
    SESSION_LIST[arg_token] = [arg_client_socket, arg_client_address]
    arg_client_socket.send(bytes("startSessionOK", "utf-8"))
    print("start session")
    print('SESSION_LIST: ')
    print(SESSION_LIST)


def stop_session(arg_token, arg_client_socket):
    arg_client_socket.send(bytes("stopSessionOK", "utf-8"))
    if check_in_dict(arg_token, SESSION_LIST):
        SESSION_LIST.pop(arg_token, 'exception')
    arg_client_socket.shutdown(socket.SHUT_WR)
    arg_client_socket.close()
    print("stop session")
    print('SESSION_LIST: ')
    print(SESSION_LIST)


def connect_session(arg_token, arg_client_socket, arg_client_address):
    arg_client_socket.send(bytes("connectSessionOK", "utf-8"))
    if check_in_dict(arg_token, SESSION_LIST):
        CONNECTION_LIST[arg_token] = [arg_client_socket, arg_client_address]
    send_to(SESSION_LIST[arg_token][0], f"MESSAGE Client {arg_client_socket} : {arg_client_address} connected")
    print("connect session")
    print('CONNECTION_LIST: ')
    print(CONNECTION_LIST)


def disconnect_session(arg_token, arg_client_socket):
    arg_client_socket.send(bytes("disconnectSessionOK", "utf-8"))
    if check_in_dict(arg_token, CONNECTION_LIST):
        CONNECTION_LIST.pop(arg_token, 'exception')
    arg_client_socket.shutdown(socket.SHUT_WR)
    arg_client_socket.close()
    print("disconnect session")
    print('CONNECTION_LIST: ')
    print(CONNECTION_LIST)


def rotate(arg_token, arg_direction, arg_client_socket):
    arg_client_socket.send(bytes("rotateOK", "utf-8"))
    if check_in_dict(arg_token, CONNECTION_LIST):
        send_to(SESSION_LIST[arg_token][0], f"rotate {arg_direction}")
    print("rotate")


def send_to(arg_socket, arg_message):
    arg_socket.send(bytes(arg_message, "utf-8"))


if __name__ == '__main__':
    print("[STARTING] server is starting...")
    server_start()
