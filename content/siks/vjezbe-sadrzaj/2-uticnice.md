---
layout: default
parent: SIKS
nav_order: 2
---

## Utičnice

### 1.1 Što su utičnice?

- **Socket** predstavlja krajnju točku komunikacije između dva procesa.  
- Omogućuju slanje i primanje podataka putem mreže koristeći standardne protokole poput TCP/IP.  
- Socket programiranje je temelj za razvoj mrežnih aplikacija, uključujući chat aplikacije, web servere, igre i dr.

### 1.2 Funkcionalnosti i primjena

- **Server socket:** Čeka dolazne konekcije na određenom portu i prihvaća klijentske zahtjeve.
- **Client socket:** Povezuje se na server socket kako bi razmijenio podatke.
- Socketi se mogu koristiti za jednostavnu razmjenu poruka ili za složeniju komunikaciju koja uključuje sigurnosne mehanizme poput enkripcije.

### 1.3 Sigurna komunikacija uz enkripciju

- Uz korištenje osnovnih socketa, moguće je osigurati sigurnost komunikacije kombiniranjem simetrične enkripcije (npr. Fernet) iz modula [pyca/cryptography](https://cryptography.io).
- Enkripcija osigurava da samo ovlaštene strane mogu čitati prenesene podatke.

---

## 2. Praktični Primjeri

### 2.1 Osnovna komunikacija pomoću utičnica

#### Server (server.py)

```python
import socket

# Kreiramo socket i postavljamo adresu i port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(1)
print("Server pokrenut na portu 8000, čekam konekciju...")

# Prihvaćamo konekciju od klijenta
client_socket, addr = server_socket.accept()
print("Povezan s:", addr)

# Primamo poruku (do 1024 bajta)
poruka = client_socket.recv(1024).decode('utf-8')
print("Primljena poruka:", poruka)

# Odgovaramo klijentu
client_socket.send("Poruka primljena!".encode('utf-8'))

client_socket.close()
server_socket.close()
```

#### Klijent (client.py)

```python
import socket

# Kreiramo socket i povezujemo se na server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Šaljemo poruku serveru
client_socket.send("Pozdrav od klijenta!".encode('utf-8'))

# Primamo odgovor od servera
odgovor = client_socket.recv(1024).decode('utf-8')
print("Odgovor servera:", odgovor)

client_socket.close()
```

### 2.2 Sigurna komunikacija putem uti;nice (Integracija s pyca/cryptography)

Ovdje ćemo demonstrirati kako integrirati simetričnu enkripciju pomoću Fernet algoritma u socket komunikaciju. Oba skripta (server i klijent) moraju koristiti isti tajni ključ. Za potrebe primjera, ključ ćemo ručno definirati.

#### Sigurni server (secure_server.py)

```python
import socket
from cryptography.fernet import Fernet

# Definiramo fiksni ključ (u stvarnom okruženju, ključ treba sigurno distribuirati)
key = b'XxMGKXnFPNMzq6R44rZMsWmCbU7K3sc_2gW29zQj9RA='  # Primjer ključ; obavezno koristite isti ključ na klijentskoj strani
fernet = Fernet(key)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9000))
server_socket.listen(1)
print("Secure server pokrenut na portu 9000, čekam konekciju...")

client_socket, addr = server_socket.accept()
print("Povezan s:", addr)

# Primamo enkriptiranu poruku
encrypted_message = client_socket.recv(1024)
decrypted_message = fernet.decrypt(encrypted_message)
print("Dešifrirana poruka:", decrypted_message.decode('utf-8'))

# Šaljemo enkriptirani odgovor
response = fernet.encrypt(b"Poruka primljena sigurno!")
client_socket.send(response)

client_socket.close()
server_socket.close()
```

#### Sigurni klijent (secure_client.py)

```python
import socket
from cryptography.fernet import Fernet

# Koristimo isti ključ kao i server
key = b'XxMGKXnFPNMzq6R44rZMsWmCbU7K3sc_2gW29zQj9RA='
fernet = Fernet(key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 9000))

# Enkriptiramo poruku prije slanja
encrypted_message = fernet.encrypt(b"Pozdrav, sigurna komunikacija!")
client_socket.send(encrypted_message)

# Primamo enkriptirani odgovor
encrypted_response = client_socket.recv(1024)
decrypted_response = fernet.decrypt(encrypted_response)
print("Odgovor servera:", decrypted_response.decode('utf-8'))

client_socket.close()
```

## 3. Zadaci za Samostalnu Vježbu
{: .important-title }
> Osnovna Socket Komunikacija:
>
> Napišite vlastite verzije server i klijent skripti koje razmjenjuju tekstualne poruke.
> Proširite funkcionalnost tako da server može obraditi više poruka u jednoj sesiji (petlja za primanje/odgovaranje).

{: .important-title }
> Sigurna Socket Komunikacija:
>
>Koristeći pyca/cryptography, implementirajte enkripciju poruka u komunikaciji između servera i klijenta.
>Osigurajte da obje strane koriste isti tajni ključ (hardkodiran ili učitan iz datoteke) i da se poruke ispravno enkriptuju i dešifriraju.

{: .important-title }
> Dodatna Sigurnosna Provjera:
>
> Implementirajte jednostavan mehanizam autentikacije gdje klijent šalje predefiniranu lozinku prilikom uspostavljanja veze.
> Server provjerava lozinku prije nego što nastavi s komunikacijom.