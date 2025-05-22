---
layout: default
parent: SIKS
nav_exclude: true
---

# Praktični zadatak 2: Simetrična i asimetrična kriptografija

## Opis zadatka

U ovom zadatku potrebno je implementirati komunikaciju između klijenta i servera tako da uključuje i osnovne primjene simetrične i asimetrične kriptografije. Cilj je implementirati razmjenu tajnih poruka na siguran način koristeći oba pristupa i razumjeti njihovu ulogu u stvarnim sustavima.

Klijent i server međusobno komuniciraju pomoću TCP socket veze. Prilikom uspostave veze, server prvo generira par javnog i privatnog ključa koristeći RSA algoritam, a zatim šalje javni ključ klijentu. Klijent, nakon što primi javni ključ, koristi ga za šifriranje sesijskog (simetričnog) ključa koji sam generira. Ovaj sesijski ključ se zatim koristi za šifriranje poruka pomoću algoritma AES (ili jednostavnije implementacije vlastite simetrične šifre, ako nije dostupna biblioteka za AES).

Server, nakon što primi šifrirani sesijski ključ, dešifrira ga koristeći svoj privatni RSA ključ. Time dobiva sesijski ključ koji dalje koristi za dešifriranje poruka koje prima od klijenta.

Na temelju ove infrastrukture, klijent zatim šifrira poruku koristeći simetričnu šifru s prethodno generiranim sesijskim ključem i šalje je serveru. Server dešifrira poruku i ispisuje originalni tekst.

Razmjena ključeva i podataka mora se odvijati u jasno definiranim koracima. Preporučuje se korištenje vlastitih funkcija za RSA i simetrične šifre, osim ako se izričito koristi standardna biblioteka poput `cryptography` ili `pycryptodome`.
