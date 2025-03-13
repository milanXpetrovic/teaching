#%%

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