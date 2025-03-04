## Uvod 

**Izvori:**
    - Practical Cryptography in Python: Learning Correct Cryptography by Example, Seth James Nielson, Christopher K. Monson
    - Implementing Cryptography Using Python, Shannon W. Bray
    - https://cryptobook.nakov.com/

## Kriptografija u pythonu: uvod
Python Fundamentals for Cryptography
    Working with bytes and encoding (ASCII, UTF-8, Base64, Hex)
    Random number generation and entropy
    Working with Python’s secrets and random modules

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



## Classical Cryptography

    Substitution ciphers (Caesar, Vigenère)
    Transposition ciphers (Rail Fence, Columnar)
    Implementation of classical ciphers in Python
    Cryptanalysis of classical ciphers (frequency analysis, brute-force)

- uvod u caesar sifriranje
- zadatak: stvoriti skriptu koja sifrira za odredjeni n
- zadatak: poslati poruku izmedju 2 skripte i desifrirati ju
- zadatak: narpaviti program koji desifrira zadanu poruku

## Simetricna kriptografija

Symmetric Cryptography (Private Key Cryptography)

    Concept of symmetric encryption
    Block ciphers vs. stream ciphers
    Data Encryption Standard (DES) (with pycryptodome)
    Advanced Encryption Standard (AES) (ECB, CBC, CTR modes)
    Padding schemes (PKCS#7, ZeroPadding)
    Implementation of AES encryption/decryption in Python

## Asymmetric Cryptography (Public Key Cryptography)

    Concept of key pairs (public and private keys)
    RSA algorithm (key generation, encryption, decryption)
    Diffie-Hellman key exchange
    Elliptic Curve Cryptography (ECC) basics
    Implementing RSA with Python (pycryptodome, cryptography)

## Hashing and Message Authentication

    Concept of one-way hashing
    Hash functions (MD5, SHA-1, SHA-256, SHA-3)
    HMAC (Hash-based Message Authentication Code)
    Salting and key-stretching (PBKDF2, bcrypt, Argon2)
    Implementing hashing and HMAC in Python


## Digital Signatures and Certificates

    Concept of digital signatures and integrity verification
    RSA and ECDSA signatures
    Implementing digital signatures in Python
    Understanding SSL/TLS and certificate authorities
    Generating self-signed certificates with OpenSSL


##  Secure Communication and Protocols

    Overview of secure communication (TLS, HTTPS)
    Implementing a secure chat system with symmetric and asymmetric encryption
    Secure email encryption with PGP/GPG
    Steganography basics and implementation
