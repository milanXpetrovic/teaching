---
layout: default
parent: SIKS
nav_order: 5
nav_exclude: true
---

# Asimetrična Kriptografija (Javnoključna Kriptografija)

### Koncept parova ključeva

Asimetrična kriptografija temelji se na parovima ključeva:

- **Javni ključ:** Može se slobodno distribuirati i koristi se za enkripciju podataka.
- **Privatni ključ:** Drži se u tajnosti i koristi se za dekripciju podataka ili digitalno potpisivanje.

### RSA algoritam

RSA je jedan od najpoznatijih asimetričnih algoritama. Ključni koraci uključuju:

- **Generiranje ključeva:** Kreiranje para (javni i privatni) na temelju velikih prostih brojeva.
- **Enkripcija:** Podaci se enkriptiraju javnim ključem.
- **Dekripcija:** Samo vlasnik privatnog ključa može dešifrirati podatke.

### Diffie-Hellman razmjena ključeva

Diffie-Hellman omogućava dvije strane da preko nesigurne veze zajednički izračunaju tajnu koja se zatim može koristiti za simetričnu enkripciju. Svaka strana generira svoj privatni ključ te razmjenom javnih ključeva dolazi do zajedničke tajne.

### Osnove eliptične kriptografije (ECC)

Eliptična kriptografija koristi matematička svojstva eliptičnih krivulja za generiranje sigurnih ključeva s manjom duljinom u usporedbi s RSA-om. ECC se često koristi za digitalne potpise i enkripciju u uređajima s ograničenim resursima.

## Praktični primjeri u Pythonu

### RSA s cryptography

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

priv_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
pub_key = priv_key.public_key()

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

### Diffie-Hellman razmjena ključeva

```python
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

parametri = dh.generate_parameters(generator=2, key_size=2048)

priv_key1 = parametri.generate_private_key()
pub_key1 = priv_key1.public_key()

priv_key2 = parametri.generate_private_key()
pub_key2 = priv_key2.public_key()

zajednicka_tajna1 = priv_key1.exchange(pub_key2)
zajednicka_tajna2 = priv_key2.exchange(pub_key1)

print("Zajednička tajna (strana 1):", zajednicka_tajna1.hex())
print("Zajednička tajna (strana 2):", zajednicka_tajna2.hex())
```

### Osnove eliptične kriptografije (ECC)

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

ecc_priv_key = ec.generate_private_key(ec.SECP256R1())
ecc_pub_key = ecc_priv_key.public_key()

poruka = b"Ovo je poruka za potpisivanje"
potpis = ecc_priv_key.sign(poruka, ec.ECDSA(hashes.SHA256()))
print("Digitalni potpis (ECC):", potpis)

try:
    ecc_pub_key.verify(potpis, poruka, ec.ECDSA(hashes.SHA256()))
    print("Potpis je ispravan!")
except Exception as e:
    print("Potpis nije ispravan:", e)

```

## Zadaci za samostalnu vježbu

{: .important-title }
>Implementacija RSA šifriranja i dešifriranja:
>
>Napišite skriptu koja generira RSA par ključeva koristeći pycryptodome i/ili cryptography.
>Skripta prima unos poruke od korisnika a zatim enkriptira poruku koristeći javni ključ.
>Poruka se dekriptira poruku pomoću privatnog ključa.

{: .important-title }
> Simulacija Diffie-Hellman razmjene putem utičnica
>
> Kreirajte dvije skripte:
> Skripta 1 (Strana A): Generira Diffie-Hellman privatni ključ, šalje svoj javni ključ putem socketa.
> Skripta 2 (Strana B): Prima javni ključ, generira svoj par, te vraća svoj javni ključ.
> Obje strane zatim izračunavaju zajedničku tajnu i ispisuju je kako bi potvrdile da su iste.
> Koristite modul socket i cryptography za implementaciju.

{: .important-title }
>ECC Digitalni Potpis i Verifikacija:
>
> Implementirajte skriptu koja generira ECC par ključeva. Potpisuje svaku unesenu poruku koristeći privatni ključ, erificira potpis koristeći javni ključ.
