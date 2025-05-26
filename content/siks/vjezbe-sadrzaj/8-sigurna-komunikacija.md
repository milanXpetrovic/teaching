---
layout: default
parent: SIKS
nav_order: 8
nav_exclude: true
---

##  Sigurna komunikacija

### Sigurna komunikacija (TLS, HTTPS)

- **TLS (Transport Layer Security)** i **HTTPS** osiguravaju da su podaci koji se razmjenjuju između klijenta i servera zaštićeni enkripcijom, integritetom i autentikacijom.  
- Digitalni certifikati i protokoli verifikacije identiteta omogućuju provjeru autentičnosti komunikacijskih strana.

### Secure chat system

- **Simetrična enkripcija (npr. AES):** Koristi se za enkripciju poruka zbog brzine i efikasnosti.  
- **Asimetrična enkripcija (npr. RSA):** Koristi se za sigurno dijeljenje ključeva.  
- Kombinacija ovih tehnika omogućava siguran prijenos poruka u realnom vremenu.

### Sigurna e-mail enkripcija (PGP/GPG)

- PGP/GPG koristi hibridni pristup: asimetrična enkripcija za razmjenu simetričnog ključa te simetrična enkripcija za enkripciju sadržaja e-maila.  
- Digitalni potpisi osiguravaju integritet i autentičnost poslanih poruka.

### Steganografija  

- Steganografija je tehnika skrivanja informacija unutar drugih medija (npr. slike, audio zapisi) bez vidljivih promjena.  
- Osnovni principi uključuju skrivanje podataka u najmanje značajne bitove (LSB) medijskih datoteka.

## Praktični Primjeri

### TLS/HTTPS Pregled

Iako potpuna implementacija TLS/HTTPS zahtijeva konfiguraciju servera i certifikata, osnovni koncepti se mogu demonstrirati pomoću Pythona. Primjer korištenja modula `ssl` (ugrađenog u Python) za kreiranje sigurnog servera i klijenta:

```python
# ssl_server.py
import socket, ssl

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8443))
server_socket.listen(5)

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

###  Secure chat system s simetričnom i asimetričnom enkripcijom

U ovom primjeru, klijent generira AES ključ za enkripciju poruka, a zatim taj ključ enkriptira koristeći serverov RSA javni ključ. Server dešifrira AES ključ koristeći svoj privatni ključ, a zatim koristi taj AES ključ za dekripciju primljenih poruka.

**Server (secure_chat_server.py):**

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, socket

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

with open("server_public.pem", "wb") as f:
    f.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PublicFormat.SubjectPublicKeyInfo))

def aes_decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9000))
server_socket.listen(1)
print("Secure chat server pokrenut na portu 9000...")

client_conn, addr = server_socket.accept()
print("Povezan s:", addr)

enc_aes_key = client_conn.recv(256)
aes_key = private_key.decrypt(enc_aes_key,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None))

iv = client_conn.recv(16)

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

with open("server_public.pem", "rb") as f:
    server_public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

aes_key = os.urandom(16)
iv = os.urandom(16)

def aes_encrypt(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length
    return encryptor.update(plaintext) + encryptor.finalize()

enc_aes_key = server_public_key.encrypt(
    aes_key,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

message = b"Hello, secure world!"
enc_message = aes_encrypt(message, aes_key, iv)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9000))
client_socket.send(enc_aes_key)
client_socket.send(iv)
client_socket.send(enc_message)
client_socket.close()
```

### Sigurna e-mail enkripcija s PGP/GPG (Simulacija)

Ovdje ćemo prikazati pojednostavljeni primjer enkripcije poruke koristeći asimetričnu enkripciju, što je temelj PGP sustava.

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

sender_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
sender_public = sender_private.public_key()

recipient_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
recipient_public = recipient_private.public_key()

message = b"Secret email content"
encrypted_message = recipient_public.encrypt(
    message,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

signature = sender_private.sign(
    message,
    asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()),
                     salt_length=asym_padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

decrypted_message = recipient_private.decrypt(
    encrypted_message,
    asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                      algorithm=hashes.SHA256(),
                      label=None)
)

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

### 2.4 Osnove steganografije

Jednostavan primjer skrivenog upisivanja tekstualne poruke unutar slike pomoću manipulacije najmanje značajnih bitova (LSB). Za ovaj primjer koristit ćemo biblioteku Pillow.

```python
from PIL import Image

def encode_message(image_path, output_path, message):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += chr(0)
    message_bin = ''.join([format(ord(i), '08b') for i in message])
    msg_len = len(message_bin)
    
    pixel_iter = iter(encoded.getdata())
    for i in range(0, msg_len, 3):
        pixels = [list(next(pixel_iter)) for _ in range(1)]
        for j in range(3):
            if i+j < msg_len:
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

    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ""
    for char in chars:
        message += chr(int(char, 2))
        if message[-1] == chr(0):
            break
    return message[:-1]

encode_message("ulaz.png", "output.png", "Skrivena poruka")
print("Dekodirana poruka:", decode_message("output.png"))
```

Napomena: Ovaj primjer je pojednostavljen i prikazuje osnovnu tehniku skrivanja podataka unutar slike. Za robusniju implementaciju potrebno je obratiti pozornost na veličinu poruke i manipulaciju većim brojem piksela.

## 3. Zadaci za Samostalnu Vježbu

> Secure Chat aplikacija
>
> Kreirajte dvije skripte (server i klijent) koje koriste socket komunikaciju. Implementirajte sigurnu razmjenu poruka: klijent treba generirati AES ključ, enkriptirati ga RSA enkripcijom koristeći serverov javni ključ te potom slati AES-enkriptirane poruke.
> Server dešifrira AES ključ i poruke te ispisuje originalne poruke.

> Simulacija PGP/GPG enkripcije
>
> Napišite skriptu koja generira RSA parove za "pošiljatelja" i "primatelja". Pošiljatelj neka enkriptira poruku koristeći primateljev javni ključ i digitalno je potpisuje, a zatim neka primatelj dešifrira poruku i verificira potpis.

> Steganografija
>
> Kreirajte program koji skriva tekstualnu poruku unutar slike (koristeći LSB metodu) te potom izdvoji skrivenu poruku.
> Napravite tri primjera s različitim veličinama poruka i slikovnim formatima.
