---
layout: default
parent: SIKS
nav_order: 7
nav_exclude: true
---

# Digitalni Potpisi i Certifikati

### Digitalni potpisi i provjera integriteta

Digitalni potpisi koriste asimetričnu kriptografiju za potvrdu autentičnosti poruke ili dokumenta.  
-**Integritet:** Digitalnim potpisom se osigurava da sadržaj poruke nije mijenjan nakon što je potpisan.  
-**Autentičnost:** Potpis potvrđuje identitet pošiljatelja, jer samo on posjeduje privatni ključ potreban za generiranje potpisa.

### RSA i ECDSA potpisi

-**RSA potpisi:** Temelje se na RSA algoritmu, gdje se koristi par ključeva (javni i privatni). Poruka se potpisuje privatnim ključem, a provjera se vrši javnim ključem.
-**ECDSA potpisi:** Koriste eliptične krivulje (npr. SECP256R1) za generiranje digitalnih potpisa. ECC (Eliptic Curve Cryptography) nudi sličnu razinu sigurnosti kao RSA, ali s kraćim ključevima, što je pogodno za uređaje s ograničenim resursima.

### SSL/TLS i certifikacijska tijela

-**SSL/TLS:** Protokoli koji omogućuju siguran prijenos podataka preko interneta. Digitalni certifikati, izdani od strane pouzdanih certifikacijskih tijela (CA), služe za potvrdu identiteta poslužitelja i uspostavu sigurne veze.
-**Certifikati:** Sadrže javni ključ i identitet poslužitelja, te su digitalno potpisani od strane CA. Samopotpisani certifikati mogu se koristiti u testnim okruženjima.

### Generiranje samopotpisanih certifikata

Alat **OpenSSL** omogućuje generiranje samopotpisanih certifikata koji se mogu koristiti za razvoj i testiranje sigurnosnih aplikacija.

## 2. Praktični primjeri u Pythonu

### RSA Digitalni potpis s bibliotekom cryptography

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

privatni_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
javni_key = privatni_key.public_key()

poruka = b"Ovo je poruka koja se digitalno potpisuje"

potpis = privatni_key.sign(
    poruka,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print("RSA digitalni potpis:", potpis.hex())

try:
    javni_key.verify(
        potpis,
        poruka,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("RSA potpis je ispravan!")
except Exception as e:
    print("RSA potpis nije ispravan:", e)
```

## 3. Zadaci za samostalnu vježbu

> RSA Digitalni Potpis i Verifikacija:
>
> Napišite skriptu koja generira RSA par ključeva koristeći cryptography, i prima unos poruke od korisnika, a zatim otpisuje poruku privatnim ključem i verificira potpis pomoću javnog ključa.
> Usporedite izlaz potpisa s različitim porukama.

> ECDSA Potpis s mrežnom komunikacijom:
> Kreirajte dvije skripte koje komuniciraju putem socketa. Prva skripta (Pošiljatelj) neka generira ECC par ključeva, potpisuje poruku i šalje poruku zajedno s potpisom i javnim ključem.
> Druga skripta (Primatelj) prima poruku, potpis i javni ključ, te verificira potpis.
