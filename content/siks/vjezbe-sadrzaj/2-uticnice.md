---
layout: default
parent: SIKS
nav_order: 2
---

## Utičnice

Programiranje utičnica ključno je za mrežnu komunikaciju, omogućujući razmjenu podataka između različitih uređaja. U Pythonu, utičnice omogućuju međuprocesnu komunikaciju preko mreže.

Pythonov `socket` modul pruža sučelje za Berkeley socket API. 

Primarne API funkcije i metode utičnice u ovom modulu su:

```python
socket()
.bind()
.listen()
.accept()
.connect()
.connect_ex()
.send()
.recv()
.close()
```

Python pruža praktičan i dosljedan API koji se preslikava izravno na sistemske pozive. Kao dio svoje standardne biblioteke. Dostupni su i mnogi moduli koji implementiraju internetske protokole više razine kao što su HTTP i SMTP. Za pregled pogledajte [Internetski protokoli i podrška](https://docs.python.org/3/library/internet.html).

---

## Praktični Primjeri

### Osnovna komunikacija pomoću utičnica

#### Server (server.py)

```python
import socket

HOST = "127.0.0.1"  
PORT = 65432 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

`socket.socket()` stvara socket objekt koji podržava tip upravitelja konteksta, tako da ga možete koristiti u naredbi `with`. Nema potrebe pozivati `​​s.close()`:

Metoda `.bind()` koristi se za povezivanje utičnice s određenim mrežnim sučeljem i brojem priključka:

U primjeru poslužitelja, `.listen()` omogućuje poslužitelju prihvaćanje veza. To poslužitelj čini utičnicom za slušanje.

Metoda `.accept()` blokira izvršenje i čeka dolaznu vezu. Kada se klijent poveže, vraća novi socket objekt koji predstavlja vezu i tuple koja sadrži adresu klijenta. Tuple će sadržavati `(host, port)` za IPv4 veze ili `(host, port, flowinfo, scopeid)` za IPv6.

Nakon što `.accept()` pruži klijentski socket objekt `conn`, koristi se beskonačna `while` petlja za prelazak preko blokirajućih poziva na `conn.recv()`. Čitaju se svi podaci koje klijent šalje i vraćaju se natrag koristeći `conn.sendall()`.

Ako `conn.recv()` vrati prazan objekt bajtova, `b''`, to signalizira da je klijent zatvorio vezu i da je petlja prekinuta. `with` se koristi s `conn` za automatsko zatvaranje utičnice na kraju bloka.

#### Klijent (client.py)

```python
import socket

HOST = "127.0.0.1" 
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")
```

U usporedbi s poslužiteljem, klijent je prilično jednostavan. Stvara socket objekt, koristi `.connect()` za povezivanje s poslužiteljem i poziva `s.sendall()` za slanje svoje poruke. Na kraju, poziva `s.recv()` da pročita odgovor poslužitelja i zatim ga ispisuje.

## 3. Zadaci za Samostalnu Vježbu

{: .important-title }
> Osnovna Socket Komunikacija:
>
> Napišite vlastite verzije server i klijent skripti koje međusobno razmjenjuju tekstualne poruke.

{: .important-title }
> Dodatna Sigurnosna Provjera:
>
> Implementirajte jednostavan mehanizam autentikacije gdje klijent šalje predefiniranu lozinku prilikom uspostavljanja veze.
> Server provjerava lozinku prije nego što nastavi s komunikacijom.
