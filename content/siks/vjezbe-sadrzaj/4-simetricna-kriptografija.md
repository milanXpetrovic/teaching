---
layout: default
parent: SIKS
nav_order: 4
---

# Simetrična Enkripcija

### 1.1 Koncept Simetrične Enkripcije

Simetrična (privatna) kriptografija koristi isti ključ za enkripciju i dekripciju podataka. Ovaj pristup je brz i učinkovit, no zahtijeva sigurno dijeljenje ključa između strana koje komuniciraju.

### 1.2 Blokovne Šifre vs. Tok Šifre

- **Blokovne šifre:** Podaci se dijele u fiksne blokove (npr. 64 ili 128 bita) koji se zatim pojedinačno enkriptiraju. Primjeri su DES i AES.
- **Tok šifre:** Podaci se enkriptiraju bit po bit ili byte po byte, često koristeći generator pseudonasumičnih brojeva. Idealne su za enkripciju podataka varijabilne duljine.

### 1.3 Data Encryption Standard (DES)

DES je jedan od prvih široko korištenih algoritama blok enkripcije s fiksnom veličinom bloka (64 bita) i ključem od 56 bita. Iako se danas smatra zastarjelim zbog sigurnosnih nedostataka, dobro je upoznati se s njegovim principima. Za demonstraciju DES enkripcije koristi se modul [pycryptodome](https://pycryptodome.readthedocs.io).

### 1.4 Advanced Encryption Standard (AES)

AES je suvremeni standard za simetričnu enkripciju. Ključ može biti 128, 192 ili 256 bita, a algoritam radi s blokovima od 128 bita. AES se može koristiti u različitim načinima rada:
- **ECB (Electronic Codebook):** Najjednostavniji način, ali osjetljiv na uzorke u podacima.
- **CBC (Cipher Block Chaining):** Svaki blok se kombinira s prethodnim, što povećava sigurnost.
- **CTR (Counter):** Pretvara blokovsku šifru u tok šifru korištenjem brojača.

### 1.5 Padding Schemes

Kod enkripcije blokovskih algoritama potrebno je osigurati da duljina podataka bude višekratnik veličine bloka. Dvije popularne metode su:
- **PKCS#7:** Dodaje se određeni broj bajtova koji označavaju koliko je paddinga dodano.
- **ZeroPadding:** Dodaju se nule, ali ova metoda može biti nepouzdana ako originalni podaci završavaju nulama.

---

## 2. Praktični Primjeri

### 2.1 DES Enkripcija (pycryptodome)

> **Napomena:** Za DES enkripciju koristimo modul `pycryptodome` jer pyca/cryptography ne podržava DES.  

```python
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# DES zahtijeva ključ od 8 bajtova
key = b'8bytekey'
data = b'Sekretna poruka DES'

# Padding: DES koristi blokove od 8 bajtova
data_padded = pad(data, DES.block_size)  # PKCS#7 padding

# Enkripcija u ECB načinu (ne preporuča se za osjetljive podatke)
cipher = DES.new(key, DES.MODE_ECB)
ciphertext = cipher.encrypt(data_padded)
print("DES enkriptirana poruka:", ciphertext)

# Dekripcija
decipher = DES.new(key, DES.MODE_ECB)
decrypted_padded = decipher.decrypt(ciphertext)
decrypted = unpad(decrypted_padded, DES.block_size)
print("DES dekriptirana poruka:", decrypted)
```

### 2.2 AES Enkripcija/Deškripcija (pyca/cryptography)

Koristit ćemo modul pyca/cryptography za implementaciju AES enkripcije u različitim načinima rada.

#### 2.2.1 Priprema i Padding s PKCS#7

```python
from cryptography.hazmat.primitives import padding as aes_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Funkcija za dodavanje PKCS#7 paddinga
def add_pkcs7_padding(data, block_size=128):
    padder = aes_padding.PKCS7(block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

# Funkcija za uklanjanje PKCS#7 paddinga
def remove_pkcs7_padding(padded_data, block_size=128):
    unpadder = aes_padding.PKCS7(block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data
```

#### 2.2.2 AES s ECB Načinom

Napomena: ECB način je jednostavan, ali ne preporuča se za produkcijske sustave zbog ponavljanja uzoraka.

```python
def aes_ecb_encrypt(plaintext, key):
    # Pretpostavljamo da je key duljine 16, 24 ili 32 bajta
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

# Primjer upotrebe:
key = os.urandom(16)  # 128-bitni ključ
plaintext = b"Poruka za AES ECB enkripciju"
ciphertext = aes_ecb_encrypt(plaintext, key)
print("AES ECB enkriptirano:", ciphertext)
print("AES ECB dekriptirano:", aes_ecb_decrypt(ciphertext, key))
```

#### 2.2.3 AES s CBC Načinom

CBC način koristi inicijalizacijski vektor (IV) koji mora biti slučajan i jedinstven za svaku enkripciju.

```python
def aes_cbc_encrypt(plaintext, key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padded_data = add_pkcs7_padding(plaintext, block_size=algorithms.AES.block_size)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext  # IV se dodaje na početak za dekripciju

def aes_cbc_decrypt(ciphertext, key):
    backend = default_backend()
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    plaintext = remove_pkcs7_padding(padded_plaintext, block_size=algorithms.AES.block_size)
    return plaintext

# Primjer upotrebe:
key = os.urandom(16)
plaintext = b"Poruka za AES CBC enkripciju"
ciphertext = aes_cbc_encrypt(plaintext, key)
print("AES CBC enkriptirano:", ciphertext)
print("AES CBC dekriptirano:", aes_cbc_decrypt(ciphertext, key))
```

#### 2.2.4 AES s CTR Načinom

CTR način pretvara blokovsku šifru u tok šifru pomoću brojača.

```python
def aes_ctr_encrypt(plaintext, key):
    backend = default_backend()
    nonce = os.urandom(16)  # Nonce se može koristiti kao početna vrijednost brojača
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

# Primjer upotrebe:
key = os.urandom(16)
plaintext = b"Poruka za AES CTR enkripciju"
ciphertext = aes_ctr_encrypt(plaintext, key)
print("AES CTR enkriptirano:", ciphertext)
print("AES CTR dekriptirano:", aes_ctr_decrypt(ciphertext, key))
```

## 3. Zadaci za Samostalnu Vježbu

Implementacija AES u ECB Načinu:
Napišite skriptu koja:
    Prima unos korisnika (poruku i ključ).
    Enkriptira poruku koristeći AES u ECB načinu s PKCS#7 paddingom.
    Dešifrira šifriranu poruku i uspoređuje je s originalom.

Komunikacija između Skripti (CBC Način):
Izradite dvije skripte:
    Prva skripta generira AES ključ i enkriptira korisnički unesenu poruku u CBC načinu (pazeći na generiranje IV-a) te sprema rezultat u datoteku.
    Druga skripta učitava enkriptirani tekst i ključ, dešifrira poruku te ispisuje originalni tekst.

Usporedba Padding Shema:
Napravite program koji:
    Uspoređuje rezultate enkripcije/dekripcije pomoću PKCS#7 paddinga i ZeroPadding-a (implementirajte ZeroPadding ručno).
    Analizira prednosti i mane svakog pristupa.
