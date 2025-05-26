---
layout: default
parent: SIKS
nav_order: 6
nav_exclude: true
---

# Hashiranje i autentikacija poruka

### 1.1 Jednosmjerno hashiranje

Jednosmjerno hashiranje je proces pretvaranja ulaznih podataka u fiksnu duljinu (hash) na način da je gotovo nemoguće rekonstruirati originalne podatke iz hash vrijednosti. Koristi se za provjeru integriteta podataka, pohranu lozinki i druge sigurnosne primjene.

### 1.2 Hash funkcije

Primjeri hash funkcija:

- **MD5:** Brza, ali danas se smatra nesigurnom zbog mogućnosti kolizija.
- **SHA-1:** Bolja od MD5, no više nije preporučena za sigurnosne primjene.
- **SHA-256:** Dio SHA-2 obitelji, široko korištena zbog visoke sigurnosti.
- **SHA-3:** Najnovija obitelj hash funkcija, nudi alternativu SHA-2 s drugačijom strukturom.

**HMAC (Hash-based Message Authentication Code)**

HMAC kombinira hash funkciju s tajnim ključem kako bi se osigurao integritet i autentičnost poruka. Samo strane koje posjeduju tajni ključ mogu generirati ispravan HMAC, čime se sprječava manipulacija podacima.

**Salting**

- **Salting:** Dodavanje slučajnog niza (salt) originalnim podacima prije hashiranja kako bi se spriječili napadi unaprijed izračunatih hash vrijednosti.

### Implementacija u Pythonu

Biblioteka [pyca/cryptography](https://cryptography.io) omogućuje implementaciju hash funkcija, HMAC-a i derivaciju ključeva (npr. PBKDF2) u Pythonu.

### Hash funkcije

Primjer korištenja hash funkcija pomoću modula `cryptography.hazmat.primitives.hashes`:

```python
from cryptography.hazmat.primitives import hashes

def hash_poruke(poruka, algorithm):
    digest = hashes.Hash(algorithm)
    digest.update(poruka)
    return digest.finalize().hex()

poruka = b"Ovo je primjer poruke"

md5_hash = hash_poruke(poruka, hashes.MD5())
print("MD5:", md5_hash)

sha1_hash = hash_poruke(poruka, hashes.SHA1())
print("SHA-1:", sha1_hash)

sha256_hash = hash_poruke(poruka, hashes.SHA256())
print("SHA-256:", sha256_hash)

sha3_hash = hash_poruke(poruka, hashes.SHA3_256())
print("SHA3-256:", sha3_hash)
```

### Implementacija HMAC-a

Primjer generiranja HMAC-a koristeći cryptography.hazmat.primitives.hmac:

```python
from cryptography.hazmat.primitives import hmac, hashes

tajni_kljuc = b"mojatajnakljuc"
poruka = b"Ovo je poruka za HMAC"

def generiraj_hmac(tajni_kljuc, poruka):
    h = hmac.HMAC(tajni_kljuc, hashes.SHA256())
    h.update(poruka)
    return h.finalize().hex()

hmac_hash = generiraj_hmac(tajni_kljuc, poruka)
print("HMAC (SHA-256):", hmac_hash)
```

### 2.3 Salting

Primjer korištenja PBKDF2HMAC iz cryptography.hazmat.primitives.kdf.pbkdf2:

```python
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

lozinka = b"mojalozinka"
salt = os.urandom(16)
iteracije = 100000

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=iteracije,
    backend=default_backend()
)

hashed_lozinka = kdf.derive(lozinka)
print("PBKDF2 hash lozinke:", hashed_lozinka.hex())
```

## 3. Zadaci za Samostalnu Vježbu

{: .important-title }
>Hashiranje i Verifikacija Poruke
>
> Napišite skriptu koja prima unos poruke od korisnika i izračunava hash poruke koristeći SHA-256 i SHA3-256.
> Uspoređuje izračunate hash vrijednosti s unaprijed definiranim hashom (simulirajte provjeru integriteta poruke).

{: .important-title }
>Implementacija HMAC-a s Komunikacijom Preko Socketa
>
> Kreirajte dvije skripte, skripta 1 (Pošiljatelj) neka prima unos poruke od korisnika, generira HMAC pomoću tajnog ključa te šalje poruku i HMAC preko socketa. Skripta 2 (Primatelj): Prima poruku i HMAC, izračunava HMAC za primljenu poruku te provjerava podudarnost kako bi osigurao integritet poruke.
> Koristite Pythonov modul socket i pyca/cryptography za implementaciju.

{: .important-title }
> Salting i Key-Stretching za Sigurno Pohranjivanje Lozinki
>
> Implementirajte program koj pPrima lozinku od korisnika, a zatim generira salt i koristi PBKDF2HMAC za derivaciju ključa. Spremite salt i hash lozinke u datoteku te implementirajte funkciju koja provjerava ispravnost unesene lozinke uspoređujući hash.
