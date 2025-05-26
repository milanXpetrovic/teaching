---
layout: default
parent: SIKS
nav_order: 4
nav_exclude: false
---

# Simetrična kriptografija

### Koncept simetrične kriptografija

Simetrična (privatna) kriptografija koristi isti ključ za enkripciju i dekripciju podataka. Ovaj pristup je brz i učinkovit, no zahtijeva sigurno dijeljenje ključa između strana koje komuniciraju.

Šifriranje sa simetričnim ključem može koristiti šifre toka ili šifre blokova:

- **Šifre blokova:** Podaci se dijele u fiksne blokove (npr. 64 ili 128 bita) koji se zatim pojedinačno enkriptiraju. Primjeri su DES i AES.
- **Šifre toka:** Podaci se enkriptiraju bit po bit ili byte po byte, često koristeći generator pseudonasumičnih brojeva. Idealne su za enkripciju podataka varijabilne duljine.

### Data Encryption Standard (DES)

DES je jedan od prvih široko korištenih algoritama šifre blokova s fiksnom veličinom bloka (64 bita) i ključem od 56 bita. Iako se danas smatra zastarjelim zbog sigurnosnih nedostataka, dobro je upoznati se s njegovim principima.

### Advanced Encryption Standard (AES)

AES je suvremeni standard za simetričnu enkripciju. Ključ može biti 128, 192 ili 256 bita, a algoritam radi s blokovima od 128 bita. AES se može koristiti u različitim načinima rada:

- **ECB (Electronic Codebook):** Najjednostavniji način, ali osjetljiv na uzorke u podacima.
- **CBC (Cipher Block Chaining):** Svaki blok se kombinira s prethodnim, što povećava sigurnost.
- **CTR (Counter):** Pretvara blokovsku šifru u tok šifru korištenjem brojača.

## Praktični primjeri

### DES enkripcija (pycryptodome)

**Napomena:** Za DES enkripciju koristimo modul `pycryptodome` jer pyca/cryptography ne podržava DES. Modul `pycryptodome` instaliramo naredbom `pip install pycryptodome`

```python
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = b'kljuc123'  ## kljuc mora imati duljinu 8 bytova
data = b'Moja tajna poruka'

data_padded = pad(data, DES.block_size) 

cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(data_padded)
print("DES kriptirana poruka:", ciphertext)

decipher = DES.new(key, DES.MODE_ECB)
decrypted_padded = decipher.decrypt(ciphertext)
decrypted = unpad(decrypted_padded, DES.block_size)
print("DES dekriptirana poruka:", decrypted)
```

### AES enkripcija/dekripcija (pyca/cryptography)

Koristit ćemo modul pyca/cryptography za implementaciju AES enkripcije u različitim načinima rada.

#### Priprema i padding s PKCS#7

```python
from cryptography.hazmat.primitives import padding as aes_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def add_pkcs7_padding(data, block_size=128):
    padder = aes_padding.PKCS7(block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def remove_pkcs7_padding(padded_data, block_size=128):
    unpadder = aes_padding.PKCS7(block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data
```

#### AES s ECB načinom

Napomena: ECB način je jednostavan, ali ne preporuča se za produkcijske sustave zbog ponavljanja uzoraka.

```python
def aes_ecb_encrypt(plaintext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padded_data = add_pkcs7_padding(plaintext, block_size=algorithms.AES.block_size)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext

def aes_ecb_decrypt(ciphertext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = remove_pkcs7_padding(padded_plaintext, block_size=algorithms.AES.block_size)
    return plaintext

key = os.urandom(16)
plaintext = b"Poruka za AES ECB enkripciju"
ciphertext = aes_ecb_encrypt(plaintext, key)
print("AES ECB enkriptirano:", ciphertext)
print("AES ECB dekriptirano:", aes_ecb_decrypt(ciphertext, key))
```

#### AES s CBC načinom

CBC način koristi inicijalizacijski vektor (IV) koji mora biti slučajan i jedinstven za svaku enkripciju.

```python
def aes_cbc_encrypt(plaintext, key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padded_data = add_pkcs7_padding(plaintext, block_size=algorithms.AES.block_size)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def aes_cbc_decrypt(ciphertext, key):
    backend = default_backend()
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    plaintext = remove_pkcs7_padding(padded_plaintext, block_size=algorithms.AES.block_size)
    return plaintext

key = os.urandom(16)
plaintext = b"Poruka za AES CBC enkripciju"
ciphertext = aes_cbc_encrypt(plaintext, key)
print("AES CBC enkriptirano:", ciphertext)
print("AES CBC dekriptirano:", aes_cbc_decrypt(ciphertext, key))
```

#### AES s CTR načinom

CTR način pretvara blokovsku šifru u tok šifru pomoću brojača.

```python
def aes_ctr_encrypt(plaintext, key):
    backend = default_backend()
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return nonce + ciphertext

def aes_ctr_decrypt(ciphertext, key):
    backend = default_backend()
    nonce = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    return plaintext

key = os.urandom(16)
plaintext = b"Poruka za AES CTR enkripciju"
ciphertext = aes_ctr_encrypt(plaintext, key)
print("AES CTR enkriptirano:", ciphertext)
print("AES CTR dekriptirano:", aes_ctr_decrypt(ciphertext, key))
```

## Zadaci za samostalnu vježbu

{: .important-title }
> Implementacija AES u ECB Načinu
>
>Napišite skriptu koja prima unos korisnika (poruku i ključ), zatim enkriptira poruku koristeći AES u ECB načinu s PKCS#7 paddingom. A zatim dešifrira šifriranu poruku i uspoređuje je s originalom.

{: .important-title }
> Komunikacija među skriptama (CBC način):
>
>Izradite dvije skripte:
> Prva skripta generira AES ključ i enkriptira korisnički unesenu poruku u CBC načinu (pazeći na generiranje IV-a) te šalje enkriptiranu poruku drugoj skripti.
> Druga skripta učitava enkriptirani tekst i ključ (za razmjenu ključeva koristite datoteku za pohranu), dešifrira poruku te ispisuje originalni tekst.
