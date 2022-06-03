import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("188.127.239.39", 9700))

msg = s.recv(1024)
print(msg.decode("utf-8"))

































