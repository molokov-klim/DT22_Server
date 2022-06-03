import socket


def server_start():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # аналогично socket.create_server(('IP',PORT))
        server_socket.bind(("188.127.239.39", 9700))
        server_socket.listen(500)  # подключений одновременно

        while True:
            print('Working...')
            client_socket, address = server_socket.accept()  # принять подключение, пока его нет код дальше не идет
            print(f"Connection from {address} has been established")
            data = client_socket.recv(1024).decode('utf-8')  # принять 1024 байта
            content = load_page_from_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)

    except KeyboardInterrupt:
        server_socket.close()
        print('shutdown')


def load_page_from_get_request(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 PAGE NOT FOUND\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1]
    response = ''
    try:
        with open('views' + path, 'rb') as file:
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Sorry, bro! No page...').encode('utf-8')


if __name__ == '__main__':
    server_start()

# data = clientSocket.recv(1024).decode('utf-8') #принять 1024 байта
# HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n' #если нужно чтобы браузеры понимали ответ
# content = 'Response'.encode('utf-8')
# clientSocket.send(content)
# clientSocket.send(bytes("Connected", "utf-8"))
# clientSocket.send(HDRS.encode('utf-8') + content)
# clientSocket.close()















