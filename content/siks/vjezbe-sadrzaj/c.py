import socket

host = '127.0.0.1'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    while True:
        msg = input("Client: ")
        s.sendall(msg.encode())
        data = s.recv(1024)
        if not data:
            break
        print("Server:", data.decode())