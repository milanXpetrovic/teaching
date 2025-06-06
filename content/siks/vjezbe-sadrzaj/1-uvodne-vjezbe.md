---
layout: default
parent: SIKS
nav_order: 1
---

# Kriptografija u Pythonu: Uvod
---

## Uvod

### Kodiranje

- **Bytes:** Osnovna jedinica podataka u računalu. Većina kriptografskih funkcija zahtjeva rad s byteovima.
- **ASCII i UTF-8:** Standardi za kodiranje znakova. ASCII pokriva osnovne znakove, dok UTF-8 omogućava kodiranje većeg broja znakova.
- **Base64:** Algoritam za kodiranje binarnih podataka u tekstualni oblik, često korišten za prijenos podataka.
- **Hexadecimalno kodiranje (Hex):** Predstavlja byteove u obliku heksadecimalnih vrijednosti, što je korisno za ispis binarnih podataka.

### Generiranje nasumičnih brojeva i entropija

- **Nasumični brojevi:** Ključni su u generiranju kriptografskih ključeva i drugih sigurnosnih elemenata.
- **Entropija:** Mjera nepredvidljivosti podataka. Viša entropija znači veću sigurnost.

### Python moduli: `secrets` i `random`

- **`secrets` modul:** Koristi se za generiranje kriptografski sigurnih nasumičnih vrijednosti (npr. tokeni, ključevi).  
- **`random` modul:** Koristi se za opće svrhe nasumičnog odabira, ali nije prikladan za sigurnosne primjene jer nije dizajniran za visoku entropiju.

## Praktični primjeri

### Konverzija stringa

```python
import base64

# Primjer stringa
tekst = "Pozdrav, kriptografijo!"

# Konverzija stringa u byteove koristeći UTF-8
byte_data = tekst.encode("utf-8")
print("Byte podaci:", byte_data)

# Kodiranje u Base64
base64_encoded = base64.b64encode(byte_data)
print("Base64 kodirano:", base64_encoded)

# Vraćanje iz Base64 natrag u byteove
base64_decoded = base64.b64decode(base64_encoded)
print("Dekodirano iz Base64:", base64_decoded.decode("utf-8"))

# Kodiranje u heksadecimalni format
hex_encoded = byte_data.hex()
print("Hex kodirano:", hex_encoded)

# Vraćanje iz Hex nazad u byteove
hex_decoded = bytes.fromhex(hex_encoded)
print("Dekodirano iz Hex:", hex_decoded.decode("utf-8"))
```

Objašnjenje:

- Tekst se prvo konvertira u byteove pomoću UTF-8 kodiranja.
- Zatim se primjenjuju Base64 i heksadecimalno kodiranje, uz demonstraciju povratne konverzije.

### Korištenje modula `random` i `secrets`

```python
import random
import secrets

# Korištenje modula random (nije za kriptografske svrhe)
nasumicni_broj = random.randint(1, 100)
print("Nasumični broj (random):", nasumicni_broj)

# Korištenje modula secrets (kripto sigurno)
siguran_broj = secrets.randbelow(100)
print("Kriptografski siguran broj (secrets):", siguran_broj)

# Generiranje sigurnog tokena
sigurni_token = secrets.token_hex(16)
print("Sigurni token:", sigurni_token)
```

Objašnjenje:

- Modul random se koristi za opće svrhe, dok modul secrets generira vrijednosti prikladne za kriptografske primjene.
- Generiranjem tokena dobivamo jedinstveni identifikator koji se može koristiti kao ključ ili autentikacijski element.

## Zadaci za samostalnu vježbu

{: .important-title }
> Bytes i Kodiranje
>
> Napišite funkciju koja prima tekstualni ulaz, konvertira ga u byteove (UTF-8), kodira u Base64, te zatim vraća dekodirani originalni tekst.
>
> Provjerite ispravnost pomoću `base64.b64encode()` i `base64.b64decode()`.

{: .important-title }
> Nasumični Brojevi:
>
> Napravite skriptu koja generira 10 kriptografski sigurnih nasumičnih brojeva u rasponu od 0 do 999 koristeći modul secrets.

{: .important-title }
> Rad s Modulom secrets:
>
> Kreirajte funkciju `generiraj_token(dužina)` koja vraća siguran token u heksadecimalnom obliku duljine definirane argumentom (koristite `secrets.token_hex()`).
