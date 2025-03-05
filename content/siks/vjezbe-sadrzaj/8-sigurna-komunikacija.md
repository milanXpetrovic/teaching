---
layout: default
parent: SIKS
nav_order: 8
---

##  Secure Communication and Protocols

    Overview of secure communication (TLS, HTTPS)
    Implementing a secure chat system with symmetric and asymmetric encryption
    Secure email encryption with PGP/GPG
    Steganography basics and implementation

## 1. Uvod i Teorijski Pregled

### 1.1 Sigurna komunikacija (TLS, HTTPS)  
- **TLS (Transport Layer Security)** i **HTTPS** osiguravaju da su podaci koji se razmjenjuju između klijenta i servera zaštićeni enkripcijom, integritetom i autentikacijom.  
- Digitalni certifikati i protokoli verifikacije identiteta omogućuju provjeru autentičnosti komunikacijskih strana.

### 1.2 Secure Chat System  
- **Simetrična enkripcija (npr. AES):** Koristi se za enkripciju poruka zbog brzine i efikasnosti.  
- **Asimetrična enkripcija (npr. RSA):** Koristi se za sigurno dijeljenje ključeva.  
- Kombinacija ovih tehnika omogućava siguran prijenos poruka u realnom vremenu.

### 1.3 Sigurna e-mail enkripcija (PGP/GPG)  
- PGP/GPG koristi hibridni pristup: asimetrična enkripcija za razmjenu simetričnog ključa te simetrična enkripcija za enkripciju sadržaja e-maila.  
- Digitalni potpisi osiguravaju integritet i autentičnost poslanih poruka.

### 1.4 Steganografija  
- Steganografija je tehnika skrivanja informacija unutar drugih medija (npr. slike, audio zapisi) bez vidljivih promjena.  
- Osnovni principi uključuju skrivanje podataka u najmanje značajne bitove (LSB) medijskih datoteka.

---

## 2. Praktični Primjeri

### 2.1 TLS/HTTPS Pregled  
Iako potpuna implementacija TLS/HTTPS zahtijeva konfiguraciju servera i certifikata, osnovni koncepti se mogu demonstrirati pomoću Pythona. Primjer korištenja modula `ssl` (ugrađenog u Python) za kreiranje sigurnog servera i klijenta:

```python
# ssl_server.py
import socket, ssl

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8443))
server_socket.listen(5)

# Kreiramo SSL kontekst (koristite odgovarajući certifikat i ključ)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')

print("SSL server pokrenut na portu 8443...")
while True:
    client_socket, addr = server_socket.accept()
    ssl_conn = context.wrap_socket(client_socket, server_side=True)
    data = ssl_conn.recv(1024)
    print("Primljeno:", data.decode())
    ssl_conn.send(b"Poruka primljena!")
    ssl_conn.close()
```

```python
# ssl_client.py
import socket, ssl

context = ssl.create_default_context()
conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
conn.connect(('localhost', 8443))
conn.send(b"Pozdrav od klijenta!")
print("Odgovor servera:", conn.recv(1024).decode())
conn.close()
```

Napomena: Za pokretanje primjera potrebno je generirati certifikat i ključ.

### 2.2 Secure Chat System s Simetričnom i Asimetričnom Enkripcijom

U ovom primjeru, klijent generira AES ključ za enkripciju poruka, a zatim taj ključ enkriptira koristeći serverov RSA javni ključ. Server dešifrira AES ključ koristeći svoj privatni ključ, a zatim koristi taj AES ključ za dekripciju primljenih poruka.

**Server (secure_chat_server.py):**

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, socket

# Generiranje RSA ključeva (samo jednom i pohraniti na sigurno mjesto)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Spremanje javnog ključa (za klijenta)
with open("server_public.pem", "wb") as f:
    f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PublicFormat.SubjectPublicKeyInfo))

def aes_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Jednostavni socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9000))
server_socket.listen(1)
print("Secure chat server pokrenut na portu 9000...")

client_conn, addr = server_socket.accept()
print("Povezan s:", addr)

# Primanje enkriptiranog AES ključa
enc_aes_key = client_conn.recv(256)
aes_key = private_key.decrypt(enc_aes_key,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None))
# Primanje IV-a za AES
iv = client_conn.recv(16)

# Primanje enkriptirane poruke
enc_message = client_conn.recv(1024)
decrypted_message = aes_decrypt(enc_message, aes_key, iv)
print("Dešifrirana poruka:", decrypted_message.decode())

client_conn.close()
server_socket.close()
```

**Klijent (secure_chat_client.py):**

```python
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, socket

# Učitavanje serverovog javnog ključa
with open("server_public.pem", "rb") as f:
    server_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

# Generiranje AES ključa i IV-a
aes_key = os.urandom(16)  # 128-bitni ključ
iv = os.urandom(16)

def aes_encrypt(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Dodavanje jednostavnog paddinga (za potrebe primjera)
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length
    return encryptor.update(plaintext) + encryptor.finalize()

# Enkripcija AES ključa RSA enkripcijom
enc_aes_key = server_public_key.encrypt(
    aes_key,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

# Poruka za enkripciju
message = b"Hello, secure world!"
enc_message = aes_encrypt(message, aes_key, iv)

# Socket klijent
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9000))
client_socket.send(enc_aes_key)
client_socket.send(iv)
client_socket.send(enc_message)
client_socket.close()
```

Napomena: Ovi primjeri služe kao ilustracija osnovnih principa. U produkcijskim rješenjima potrebno je implementirati dodatne sigurnosne provjere, autentikaciju i rukovanje pogreškama.

### 2.3 Sigurna e-mail enkripcija s PGP/GPG (Simulacija)

Ovdje ćemo prikazati pojednostavljeni primjer enkripcije poruke koristeći asimetričnu enkripciju, što je temelj PGP sustava.

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

# Generiramo RSA par ključeva za "pošiljatelja" i "primatelja"
sender_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
sender_public = sender_private.public_key()

recipient_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
recipient_public = recipient_private.public_key()

# Pošiljatelj enkriptira poruku koristeći primateljev javni ključ
message = b"Secret email content"
encrypted_message = recipient_public.encrypt(
    message,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

# Pošiljatelj digitalno potpisuje poruku svojim privatnim ključem
signature = sender_private.sign(
    message,
    asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()),
                     salt_length=asym_padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# Primatelj dekriptiraj poruku i verificira potpis
decrypted_message = recipient_private.decrypt(
    encrypted_message,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

# Verifikacija potpisa
try:
    sender_public.verify(
        signature,
        decrypted_message,
        asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()),
                         salt_length=asym_padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    print("Poruka je uspješno dešifrirana i potpis je ispravan.")
except Exception as e:
    print("Došlo je do greške u verifikaciji potpisa:", e)
```

### 2.4 Osnove Steganografije

Jednostavan primjer skrivenog upisivanja tekstualne poruke unutar slike pomoću manipulacije najmanje značajnih bitova (LSB). Za ovaj primjer koristit ćemo biblioteku Pillow.

```python
from PIL import Image

def encode_message(image_path, output_path, message):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Dodajemo terminator za kraj poruke
    message_bin = ''.join([format(ord(i), '08b') for i in message])
    msg_len = len(message_bin)
    
    pixel_iter = iter(encoded.getdata())
    for i in range(0, msg_len, 3):
        pixels = [list(next(pixel_iter)) for _ in range(1)]
        for j in range(3):
            if i+j < msg_len:
                # Zamjena najmanje značajnog bita
                pixels[0][j] = pixels[0][j] & ~1 | int(message_bin[i+j])
        encoded.putpixel((i % width, i // width), tuple(pixels[0]))
    
    encoded.save(output_path)
    print("Poruka uspješno skrivena u slici.")

def decode_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    bits = ""
    for pixel in pixels:
        for color in pixel[:3]:
            bits += str(color & 1)
    # Grupiramo u bajtove
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ""
    for char in chars:
        message += chr(int(char, 2))
        if message[-1] == chr(0):  # Terminator
            break
    return message[:-1]

# Primjer upotrebe:
encode_message("ulaz.png", "output.png", "Skrivena poruka")
print("Dekodirana poruka:", decode_message("output.png"))
```

Napomena: Ovaj primjer je pojednostavljen i prikazuje osnovnu tehniku skrivanja podataka unutar slike. Za robusniju implementaciju potrebno je obratiti pozornost na veličinu poruke i manipulaciju većim brojem piksela.

## 3. Zadaci za Samostalnu Vježbu

    Secure Chat aplikacija:
        Izradite dvije skripte (server i klijent) koje koriste socket programiranje.
        Implementirajte sigurnu razmjenu poruka: klijent treba generirati AES ključ, enkriptirati ga RSA enkripcijom koristeći serverov javni ključ te potom slati AES-enkriptirane poruke.
        Server dešifrira AES ključ i poruke te ispisuje originalne poruke.

    Simulacija PGP/GPG enkripcije:
        Napišite skriptu koja generira RSA parove za "pošiljatelja" i "primatelja".
        Pošiljatelj enkriptira poruku koristeći primateljev javni ključ i digitalno je potpisuje.
        Primatelj dešifrira poruku i verificira potpis.

    Steganografija:
        Kreirajte program koji skriva tekstualnu poruku unutar slike (koristeći LSB metodu) te potom izdvoji skrivenu poruku.
        Eksperimentirajte s različitim veličinama poruka i slikovnim formatima.

    TLS komunikacija:
        Izradite sigurni server koristeći Pythonov ssl modul i odgovarajući certifikat.
        Napišite klijentsku skriptu koja se povezuje s serverom i razmjenjuje šifrirane poruke.