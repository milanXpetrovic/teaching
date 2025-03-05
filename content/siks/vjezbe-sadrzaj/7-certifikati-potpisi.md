---
layout: default
parent: SIKS
nav_order: 7
nav_exclude: true
---

# Digitalni Potpisi i Certifikati

Ova skripta je dodatak na kolegiju te obrađuje osnove digitalnih potpisa i certifikata. U njoj ćete se upoznati s konceptom digitalnih potpisa kao mehanizma za provjeru integriteta i autentičnosti podataka, te s načinima njihove implementacije korištenjem asimetrične kriptografije. Obradit ćemo RSA i ECDSA potpise, osnove SSL/TLS protokola i ulogu certifikacijskih tijela (Certificate Authorities), a također ćemo pokazati kako generirati samopotpisane certifikate pomoću OpenSSL alata.

---

## 1. Uvod i Teorijski Pregled

### 1.1 Digitalni Potpisi i Provjera Integriteta

Digitalni potpisi koriste asimetričnu kriptografiju za potvrdu autentičnosti poruke ili dokumenta.  
-**Integritet:** Digitalnim potpisom se osigurava da sadržaj poruke nije mijenjan nakon što je potpisan.  
-**Autentičnost:** Potpis potvrđuje identitet pošiljatelja, jer samo on posjeduje privatni ključ potreban za generiranje potpisa.

### 1.2 RSA i ECDSA Potpisi
-**RSA potpisi:** Temelje se na RSA algoritmu, gdje se koristi par ključeva (javni i privatni). Poruka se potpisuje privatnim ključem, a provjera se vrši javnim ključem.
-**ECDSA potpisi:** Koriste eliptične krivulje (npr. SECP256R1) za generiranje digitalnih potpisa. ECC (Eliptic Curve Cryptography) nudi sličnu razinu sigurnosti kao RSA, ali s kraćim ključevima, što je pogodno za uređaje s ograničenim resursima.

### 1.3 SSL/TLS i Certifikacijska Tijela

-**SSL/TLS:** Protokoli koji omogućuju siguran prijenos podataka preko interneta. Digitalni certifikati, izdani od strane pouzdanih certifikacijskih tijela (CA), služe za potvrdu identiteta poslužitelja i uspostavu sigurne veze.
-**Certifikati:** Sadrže javni ključ i identitet poslužitelja, te su digitalno potpisani od strane CA. Samopotpisani certifikati mogu se koristiti u testnim okruženjima.

### 1.4 Generiranje Samopotpisanih Certifikata

Alat **OpenSSL** omogućuje generiranje samopotpisanih certifikata koji se mogu koristiti za razvoj i testiranje sigurnosnih aplikacija.

---

## 2. Praktični Primjeri u Pythonu

### 2.1 RSA Digitalni Potpis s Bibliotekom cryptography

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generiranje RSA ključeva
privatni_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
javni_key = privatni_key.public_key()

# Poruka za potpisivanje
poruka = b"Ovo je poruka koja se digitalno potpisuje"

# Potpisivanje poruke koristeći privatni ključ
potpis = privatni_key.sign(
    poruka,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print("RSA digitalni potpis:", potpis.hex())

# Verifikacija potpisa koristeći javni ključ
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

## 3. Zadaci za Samostalnu Vježbu

    RSA Digitalni Potpis i Verifikacija:
        Napišite skriptu koja:
            Generira RSA par ključeva koristeći cryptography.
            Prima unos poruke od korisnika.
            Potpisuje poruku privatnim ključem.
            Verificira potpis pomoću javnog ključa.
        Usporedite izlaz potpisa s različitim porukama.

    ECDSA Potpis s Mrežnom Komunikacijom:
        Kreirajte dvije skripte koje komuniciraju putem socketa:
            Skripta 1 (Pošiljatelj): Generira ECC par ključeva, potpisuje poruku i šalje poruku zajedno s potpisom i javnim ključem.
            Skripta 2 (Primatelj): Prima poruku, potpis i javni ključ, te verificira potpis.
        Osigurajte da se primljena poruka može provjeriti u realnom vremenu.

    SSL/TLS Simulacija s Samopotpisanim Certifikatom:
        Koristeći OpenSSL, generirajte samopotpisani certifikat.
        Implementirajte jednostavnu HTTPS poslužiteljsku skriptu u Pythonu (npr. koristeći modul http.server s SSL podrškom) koja koristi generirani certifikat.
        Kreirajte klijentsku skriptu koja se spaja na poslužitelja putem HTTPS-a i provjerava valjanost certifikata.

    Integrirani Projekt – Digitalni Potpisi u Sigurnoj Komunikaciji:
        Osmislite mrežnu aplikaciju u kojoj se koristi digitalni potpis za autentikaciju poruka:
            Pošiljatelj enkriptira i potpisuje poruku (koristeći RSA ili ECDSA) te je šalje putem socketa.
            Primatelj dekriptuje i verificira potpis poruke.
        Analizirajte slučajeve kada potpis nije ispravan i implementirajte odgovarajuće obavijesti.
