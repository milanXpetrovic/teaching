---
layout: default
parent: SIKS
nav_order: 2
---

## Sockets
https://realpython.com/python-sockets/
https://group.miletic.net/hr/nastava/materijali/python-modul-socket/

- uvod sto su socketi
- prakticni primjer kako kreirati sockete
- zadatak: poslati poruku izmedju dvije skripte

**server.py**
```python
import socket

host='127.0.0.1'
port=12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Server listening on {host}:{port}...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data or data.lower() == 'exit':
        print("Client disconnected.")
        break
    print(f"Client: {data}")
    
    response = input("Server: ")
    conn.send(response.encode())

conn.close()
server_socket.close()
```

**client.py**

```python
import socket

host='127.0.0.1'
port=12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"Connected to server {host}:{port}")

while True:
    message = input("Client: ")
    client_socket.send(message.encode())

    if message.lower() == 'exit':
        break

    response = client_socket.recv(1024).decode()
    print(f"Server: {response}")

client_socket.close()
```
