---
layout: default
parent: SIKS
nav_order: 5
---

# Asimetrična Kriptografija (Javnoključna Kriptografija)

Ova skripta je dodatak na kolegiju te pruža uvid u osnove asimetrične kriptografije. U njoj ćemo objasniti temeljne koncepte parova ključeva (javni i privatni ključ), algoritam RSA (generiranje ključeva, enkripcija i dekripcija), Diffie-Hellman razmjenu ključeva, te osnove eliptične kriptografije (ECC). Također, demonstrirat ćemo implementaciju RSA enkripcije koristeći popularne Python biblioteke, kao što su [pycryptodome](https://www.pycryptodome.org) i [cryptography](https://cryptography.io).

---

## 1. Uvod i Teorijski Pregled

### 1.1 Koncept Parova Ključeva

Asimetrična kriptografija temelji se na parovima ključeva:
- **Javni ključ:** Može se slobodno distribuirati i koristi se za enkripciju podataka.
- **Privatni ključ:** Drži se u tajnosti i koristi se za dekripciju podataka ili digitalno potpisivanje.

### 1.2 RSA Algoritam

RSA je jedan od najpoznatijih asimetričnih algoritama. Ključni koraci uključuju:
- **Generiranje ključeva:** Kreiranje para (javni i privatni) na temelju velikih prostih brojeva.
- **Enkripcija:** Podaci se enkriptiraju javnim ključem.
- **Dekripcija:** Samo vlasnik privatnog ključa može dešifrirati podatke.

### 1.3 Diffie-Hellman Razmjena Ključeva

Diffie-Hellman omogućava dvije strane da preko nesigurne veze zajednički izračunaju tajnu koja se zatim može koristiti za simetričnu enkripciju. Svaka strana generira svoj privatni ključ te razmjenom javnih ključeva dolazi do zajedničke tajne.

### 1.4 Osnove Eliptične Kriptografije (ECC)

Eliptična kriptografija koristi matematička svojstva eliptičnih krivulja za generiranje sigurnih ključeva s manjom duljinom u usporedbi s RSA-om. ECC se često koristi za digitalne potpise i enkripciju u uređajima s ograničenim resursima.

### 1.5 Implementacija RSA u Pythonu

Implementacija RSA algoritma može se izvršiti korištenjem različitih biblioteka:
- **pycryptodome:** Pruža jednostavan API za generiranje ključeva, enkripciju i dekripciju.
- **cryptography:** Moderniji pristup s naprednijim sigurnosnim značajkama.

---

## 2. Praktični Primjeri u Pythonu

### 2.1 RSA s pycryptodome

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generiranje RSA ključeva (2048 bita)
key = RSA.generate(2048)
privatni_kljuc = key.export_key()
javni_kljuc = key.publickey().export_key()

print("Javni ključ (pycryptodome):")
print(javni_kljuc.decode())
print("\nPrivatni ključ (pycryptodome):")
print(privatni_kljuc.decode())

# Enkripcija poruke koristeći javni ključ i PKCS#1 OAEP padding
poruka = b"Ovo je tajna poruka"
cipher_rsa = PKCS1_OAEP.new(key.publickey())
sifrirana_poruka = cipher_rsa.encrypt(poruka)
print("\nSifrirana poruka (pycryptodome):", sifrirana_poruka)

# Dekripcija poruke koristeći privatni ključ
decipher_rsa = PKCS1_OAEP.new(key)
desifrirana_poruka = decipher_rsa.decrypt(sifrirana_poruka)
print("Desifrirana poruka (pycryptodome):", desifrirana_poruka)
```

### 2.2 RSA s cryptography

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generiranje RSA ključeva (2048 bita)
priv_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
pub_key = priv_key.public_key()

# Serijalizacija ključeva za ispis
javni_kljuc_bytes = pub_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
privatni_kljuc_bytes = priv_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

print("Javni ključ (cryptography):")
print(javni_kljuc_bytes.decode())
print("\nPrivatni ključ (cryptography):")
print(privatni_kljuc_bytes.decode())

# Enkripcija poruke pomoću javnog ključa
poruka = b"Ovo je tajna poruka"
ciphertext = pub_key.encrypt(
    poruka,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Sifrirana poruka (cryptography):", ciphertext)

# Dekripcija poruke pomoću privatnog ključa
plaintext = priv_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Desifrirana poruka (cryptography):", plaintext)
```

### 2.3 Diffie-Hellman Razmjena Ključeva

```python
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Generiranje parametara za Diffie-Hellman (generator 2, ključ veličine 2048 bita)
parametri = dh.generate_parameters(generator=2, key_size=2048)

# Generiranje privatnih i javnih ključeva za dvije strane
priv_key1 = parametri.generate_private_key()
pub_key1 = priv_key1.public_key()

priv_key2 = parametri.generate_private_key()
pub_key2 = priv_key2.public_key()

# Izračun zajedničke tajne za obje strane
zajednicka_tajna1 = priv_key1.exchange(pub_key2)
zajednicka_tajna2 = priv_key2.exchange(pub_key1)

print("Zajednička tajna (strana 1):", zajednicka_tajna1.hex())
print("Zajednička tajna (strana 2):", zajednicka_tajna2.hex())
```

### 2.4 Osnove Eliptične Kriptografije (ECC)

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# Generiranje ECC ključeva koristeći krivulju SECP256R1
ecc_priv_key = ec.generate_private_key(ec.SECP256R1())
ecc_pub_key = ecc_priv_key.public_key()

# Potpisivanje poruke koristeći ECDSA s SHA256
poruka = b"Ovo je poruka za potpisivanje"
potpis = ecc_priv_key.sign(poruka, ec.ECDSA(hashes.SHA256()))
print("Digitalni potpis (ECC):", potpis)

# Verifikacija potpisa
try:
    ecc_pub_key.verify(potpis, poruka, ec.ECDSA(hashes.SHA256()))
    print("Potpis je ispravan!")
except Exception as e:
    print("Potpis nije ispravan:", e)

```

## 3. Zadaci za Samostalnu Vježbu

    Implementacija RSA Šifriranja i Dešifriranja:
        Napišite skriptu koja:
            Generira RSA par ključeva koristeći pycryptodome i cryptography.
            Prima unos poruke od korisnika.
            Enkriptira poruku koristeći javni ključ.
            Dekriptira poruku pomoću privatnog ključa.
            Uspoređuje rezultate između obje implementacije.

    Simulacija Diffie-Hellman Razmjene putem Socketa:
        Kreirajte dvije skripte:
            Skripta 1 (Strana A): Generira Diffie-Hellman privatni ključ, šalje svoj javni ključ putem socketa.
            Skripta 2 (Strana B): Prima javni ključ, generira svoj par, te vraća svoj javni ključ.
            Obje strane zatim izračunavaju zajedničku tajnu i ispisuju je kako bi potvrdile da su iste.
        Koristite Pythonov modul socket i cryptography za implementaciju.

    ECC Digitalni Potpis i Verifikacija:
        Implementirajte skriptu koja:
            Generira ECC par ključeva.
            Potpisuje unesenu poruku koristeći privatni ključ.
            Verificira potpis koristeći javni ključ.
            Eksperimentirajte mijenjajući poruku te primijetite učinak na verifikaciju.

    Integrirani Mrežni Projekt s RSA:
        Osmislite jednostavnu mrežnu aplikaciju u kojoj:
            Jedna skripta (pošiljatelj) enkriptira poruku pomoću RSA javnog ključa i šalje je putem socketa.
            Druga skripta (primatelj) prima enkriptiranu poruku, dekriptuje je koristeći svoj privatni ključ te ispisuje originalnu poruku.
        Uključite i digitalni potpis (npr. s ECC) za potvrdu autentičnosti poruke.
