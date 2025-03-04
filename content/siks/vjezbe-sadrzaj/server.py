# server.py
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

if __name__ == "__main__":
    start_server()