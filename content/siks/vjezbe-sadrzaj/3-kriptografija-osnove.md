---
layout: default
parent: SIKS
nav_order: 3
nav_exclude: false
---

# Osnovni kriptografski algoritmi

- **Substitucijski algoritmi:**  
  - *Caesarovo šifriranje:* Svakoj poruci se primjenjuje fiksni pomak abecedom.  
  - *Vigenèreovo šifriranje:* Koristi se ključ koji određuje pomak za svaki znak u poruci.

- **Transpozicijski algoritmi:**  
  - *Rail Fence šifra:* Poruka se zapisuje u obliku cikličnog obrasca (željeznica), a zatim se čitaju redak po redak.  
  - *Columnar šifra:* Poruka se zapisuje u matricu, a zatim se čitaju stupci prema unaprijed određenom redoslijedu (ključu).

Također ćemo se ukratko dotaknuti osnove kriptanalize klasičnih šifri, poput frekvencijske analize i brute-force pristupa, koji su važni alati za dešifriranje bez poznavanja tajnog ključa.

---

## 1. Uvod i teorijski pregled

### 1.1 Substitucijski algoritmi

**Caesarov algoritam:**

- Svakoj poruci se primjenjuje fiksni pomak (n).  
- Jednostavan za implementaciju, ali relativno lako za dešifrirati brute-force metodom.

**Vigenèreov algoritam:**

- Koristi se ključ (riječ ili niz znakova) čiji se znakovi ciklički primjenjuju kao pomaci.  
- Pruža veću sigurnost od Caesarove šifre, ali je podložan frekvencijskoj analizi.

### 1.2 Transpozicijski algoritmi

**Rail Fence šifra:**  

- Poruka se "piše" u obliku cik-cak obrasca preko nekoliko "pruga" (redova).  
- Čitanjem redaka dobiva se šifrirani tekst.

**Columnar (stupčasta) šifra:**  

- Poruka se zapisuje u matricu širine definirane ključem.  
- Zatim se stupci čitaju u određenom redoslijedu kako bi se dobio šifrirani tekst.

### 1.3 Kripto analiza

**Frekvencijska analiza:**

- Analiza učestalosti pojavljivanja znakova u šifriranom tekstu.  
- Kod jezika s poznatom distribucijom znakova, ova metoda može otkriti moguće pomake ili ključeve.

**Brute-force pristup:**

- Isprobavanje svih mogućih ključeva (npr. svih 26 pomaka u Caesarovoj šifri).  
- Jednostavan, ali zahtjevan kod složenijih algoritama.

---

## 2. Praktični primjeri u Pythonu

### 2.1 Caesarov šifriranje

```python
def caesar_encrypt(plaintext, shift):
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Pomakni znak i vrati ga u abecedni raspon
            encrypted += chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted += char
    return encrypted

def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)

# Primjer korištenja:
poruka = "PozdravSvijete"
shift = 3
sifrirana = caesar_encrypt(poruka, shift)
desifrirana = caesar_decrypt(sifrirana, shift)

print("Originalna poruka:", poruka)
print("Sifrirana poruka (pomak =", shift, "):", sifrirana)
print("Desifrirana poruka:", desifrirana)
```

---

### 2.2 Vigenèreov šifriranje

```python
def vigenere_encrypt(plaintext, key):
    encrypted = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            encrypted += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            encrypted += char
    return encrypted

def vigenere_decrypt(ciphertext, key):
    decrypted = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)].lower()) - ord('a')
            decrypted += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            decrypted += char
    return decrypted

# Primjer korištenja:
poruka = "PozdravSvijete"
kljuc = "ključ"
sifrirana = vigenere_encrypt(poruka, kljuc)
desifrirana = vigenere_decrypt(sifrirana, kljuc)

print("Originalna poruka:", poruka)
print("Sifrirana poruka:", sifrirana)
print("Desifrirana poruka:", desifrirana)
```

### 2.3 Rail Fence šifriranje

```python
def rail_fence_encrypt(plaintext, num_rails):
    rails = [''] * num_rails
    rail = 0
    direction = 1
    for char in plaintext:
        rails[rail] += char
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    return ''.join(rails)

def rail_fence_decrypt(ciphertext, num_rails):
    rail_pattern = [None] * len(ciphertext)
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        rail_pattern[i] = rail
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    rail_counts = [rail_pattern.count(r) for r in range(num_rails)]
    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(ciphertext[index:index+count]))
        index += count

    plaintext = ""
    for r in rail_pattern:
        plaintext += rails[r].pop(0)
    return plaintext

poruka = "KlasicanKriptografskiAlgoritam"
num_rails = 3
sifrirana = rail_fence_encrypt(poruka, num_rails)
desifrirana = rail_fence_decrypt(sifrirana, num_rails)

print("Originalna poruka:", poruka)
print("Sifrirana (Rail Fence):", sifrirana)
print("Desifrirana poruka:", desifrirana)
```

## 3. Zadaci za samostalnu vježbu

{: .important-title }
> Implementacija Caesarove šifre
>
> Napišite skriptu koja:
>    Prima korisnički unos poruke i pomaka (n).
>    Šifrira poruku koristeći Caesarov algoritam.
>    Dešifrira šifriranu poruku i uspoređuje je s originalom.

{: .important-title }
> Komunikacija između skripti
>
> Kreirajte dvije odvojene skripte:
>     Prva skripta šifrira poruku koristeći Caesarove algoritam i šalje šifrirani tekst drugoj skripti.
>     Druga skripta prima poruku, dešifrira poruku koristeći isti ključ i ispisuje originalni tekst.

{: .important-title }
> Automatsko dešifriranje
>
> Napravite program koji:
>     Prima šifrirani tekst (pretpostavite da je šifriran Caesarovom šifrom).
>     Primjenjuje brute-force pristup (ili frekvencijsku analizu kao dodatak) kako bi pronašao ispravan pomak i dešifrirao poruku.
