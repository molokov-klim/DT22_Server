import socket

session_list = {}  # лист сессий
connection_list = {}  # лист с подключениями
data = ''  # сообщение от клиента
method = ''  # первая часть сообщения - метод
token = ''  # вторая часть сообщения - токен
ip = ''  # третья часть сообщения - IP
direction = ''  # четвертая часть сообщения - направление




def server_start():
    try:
        server_socket = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)  # аналогично socket.create_server(('IP',PORT))
        server_socket.bind(("188.127.239.39", 9700))
        server_socket.listen(500)  # подключений одновременно

        while True:
            print('Working...')
            client_socket, address = server_socket.accept()  # принять подключение, пока его нет код дальше не идет
            print(f"Connection from {address} has been established")
            data = client_socket.recv(1024).decode('utf-8')  # принять 1024 байта
            try:
                method = data.split()[0]
            except:
                print('No have data[0]')
            try:
                token = data.split()[1]
            except:
                print('No have data[1]')
            try:
                ip = data.split()[2]
            except:
                print('No have data[2]')
            try:
                direction = data.split()[3]
            except:
                print('No have data[3]')

            if method == "startSession":
                start_session(token, ip)
                client_socket.send(bytes("startSessionOK", "utf-8"))

            if method == "stopSession":
                stop_session(token, ip)
                client_socket.send(bytes("stopSessionOK", "utf-8"))
                client_socket.shutdown(socket.SHUT_WR)

            if method == "connectSession":
                connect_session(token, ip)
                client_socket.send(bytes("connectSessionOK", "utf-8"))

            if method == "disconnectSession":
                disconnect_session(token, ip)
                client_socket.send(bytes("disconnectSessionOK", "utf-8"))

            if method == "rotate":
                rotate(token, ip, direction)
                client_socket.send(bytes("rotateOK", "utf-8"))

            data = ''
            method = ''
            token = ''
            ip = ''
            direction = ''

            if method != "startSession":
                client_socket.shutdown(socket.SHUT_WR)

    except KeyboardInterrupt:
        server_socket.close()
        print('shutdown')


def check_in_dict(key, dictionary):
    if dictionary.get(key, False) != False:
        return True
    else:
        return False


def start_session(token, ip):
    print("start session")
    session_list[token] = [ip]


def stop_session(token, ip):
    print("stop session")
    session_list.pop(token, 'bebeka')


def connect_session(token, ip):
    print("connect session")
    if check_in_dict(token, session_list) == True:
        connection_list[token] = [ip]


def disconnect_session(token, ip):
    print("disconnect session")
    if check_in_dict(token, connection_list) == True:
        connection_list.pop(token, 'memeka')


def rotate(token, ip, direction):
    print("rotate")
    # if check_in_dict(token, connection_list) == True:


if __name__ == '__main__':
    server_start()

# data = clientSocket.recv(1024).decode('utf-8') #принять 1024 байта
# HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n' #если нужно чтобы браузеры понимали ответ
# content = 'Response'.encode('utf-8')
# clientSocket.send(content)
# clientSocket.send(bytes("Connected", "utf-8"))
# clientSocket.send(HDRS.encode('utf-8') + content)
# clientSocket.close()

# dict.pop('value1', defaultResponce)
# [dict.pop(key) for key in ['value1', 'value2']]
