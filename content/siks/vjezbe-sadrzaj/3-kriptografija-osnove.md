# Osnovni Kriptografski Algoritmi u Pythonu


Ova skripta pruža pregled klasičnih kriptografskih algoritama implementiranih u Pythonu. Namijenjena je informatičarima koji su upoznati s Pythonom, ali nemaju iskustva u području kriptografije. U ovoj skripti obrađuju se dvije glavne skupine algoritama:

- **Substitucijski algoritmi:**  
  - *Caesarov šifriranje:* Svakoj poruci se primjenjuje fiksni pomak abecedom.  
  - *Vigenèreov šifriranje:* Koristi se ključ koji određuje pomak za svaki znak u poruci.

- **Transpozicijski algoritmi:**  
  - *Rail Fence šifra:* Poruka se zapisuje u obliku cikličnog obrasca (željeznica), a zatim se čitaju redak po redak.  
  - *Columnar šifra:* Poruka se zapisuje u matricu, a zatim se čitaju stupci prema unaprijed određenom redoslijedu (ključu).

Također ćemo ukratko dotaknuti osnove kriptanalize klasičnih šifri, poput frekvencijske analize i brute-force pristupa, koji su važni alati za dešifriranje bez poznavanja tajnog ključa.

---

## 1. Uvod i Teorijski Pregled

### 1.1 Substitucijski Algoritmi

**Caesarov algoritam:**  
- Svakoj poruci se primjenjuje fiksni pomak (n).  
- Jednostavan za implementaciju, ali relativno lako razbijljiv brute-force metodom.

**Vigenèreov algoritam:**  
- Koristi se ključ (riječ ili niz znakova) čiji se znakovi ciklički primjenjuju kao pomaci.  
- Pruža veću sigurnost od Caesarove šifre, ali je podložan frekvencijskoj analizi.

### 1.2 Transpozicijski Algoritmi

**Rail Fence šifra:**  
- Poruka se "piše" u obliku cik-cak obrasca preko nekoliko "pruga" (redova).  
- Čitanjem redaka dobiva se šifrirani tekst.

**Columnar (stupčasta) šifra:**  
- Poruka se zapisuje u matricu širine definirane ključem.  
- Zatim se stupci čitaju u određenom redoslijedu kako bi se dobio šifrirani tekst.

### 1.3 Kriptanaliza

**Frekvencijska analiza:**  
- Analiza učestalosti pojavljivanja znakova u šifriranom tekstu.  
- Kod jezika s poznatom distribucijom znakova, ova metoda može otkriti moguće pomake ili ključeve.

**Brute-force pristup:**  
- Isprobavanje svih mogućih ključeva (npr. svih 26 pomaka u Caesarovoj šifri).  
- Jednostavan, ali zahtjevan kod složenijih algoritama.

---

## 2. Praktični Primjeri u Pythonu

### 2.1 Caesarov Šifriranje

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

### 2.2 Vigenèreov Šifriranje

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
poruka = "SkriptaKriptografije"
kljuc = "ključ"
sifrirana = vigenere_encrypt(poruka, kljuc)
desifrirana = vigenere_decrypt(sifrirana, kljuc)

print("Originalna poruka:", poruka)
print("Sifrirana poruka:", sifrirana)
print("Desifrirana poruka:", desifrirana)
```

### 2.3 Rail Fence Šifra

```python
def rail_fence_encrypt(plaintext, num_rails):
    # Inicijaliziraj pruge kao prazan niz stringova
    rails = [''] * num_rails
    rail = 0
    direction = 1  # 1 = prema dolje, -1 = prema gore
    for char in plaintext:
        rails[rail] += char
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1
    return ''.join(rails)

def rail_fence_decrypt(ciphertext, num_rails):
    # Prvo odredimo raspodjelu znakova po prugama
    rail_pattern = [None] * len(ciphertext)
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        rail_pattern[i] = rail
        rail += direction
        if rail == 0 or rail == num_rails - 1:
            direction *= -1

    # Prebroji znakove u svakoj pruzi
    rail_counts = [rail_pattern.count(r) for r in range(num_rails)]
    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(ciphertext[index:index+count]))
        index += count

    # Sastavi originalni tekst
    plaintext = ""
    for r in rail_pattern:
        plaintext += rails[r].pop(0)
    return plaintext

# Primjer korištenja:
poruka = "KlasicanKriptografskiAlgoritam"
num_rails = 3
sifrirana = rail_fence_encrypt(poruka, num_rails)
desifrirana = rail_fence_decrypt(sifrirana, num_rails)

print("Originalna poruka:", poruka)
print("Sifrirana (Rail Fence):", sifrirana)
print("Desifrirana poruka:", desifrirana)
```

## 3. Zadaci za Samostalnu Vježbu

Zadatak: Implementacija Caesarove Šifre
Napišite skriptu koja:
    Prima korisnički unos poruke i pomaka (n).
    Šifrira poruku koristeći Caesarov algoritam.
    Dešifrira šifriranu poruku i uspoređuje je s originalom.

Zadatak: Komunikacija između Skripti
Kreirajte dvije odvojene skripte:
    Prva skripta šifrira poruku koristeći Vigenèreov algoritam i sprema šifrirani tekst u datoteku.
    Druga skripta učitava tu datoteku, dešifrira poruku koristeći isti ključ i ispisuje originalni tekst.

Zadatak: Automatska Dešifriranje
Napravite program koji:
    Prima šifrirani tekst (pretpostavite da je šifriran Caesarovom šifrom).
    Primjenjuje brute-force pristup (ili frekvencijsku analizu kao dodatak) kako bi pronašao ispravan pomak i dešifrirao poruku.
    Opcionalno, implementirajte jednostavnu funkciju koja računa učestalost znakova u tekstu i pomaže u prepoznavanju ispravnog dešifriranog teksta.