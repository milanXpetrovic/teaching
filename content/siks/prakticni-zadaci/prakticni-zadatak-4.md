---
layout: default
parent: SIKS
nav_exclude: true
---

# Praktični zadatak 4: Dvofaktorska autentifikacija i jednokratne zaporke

## Opis zadatka

U ovom zadatku potrebno je implementirati jednostavan sustav za provjeru identiteta korisnika koristeći dvofaktorsku autentifikaciju (2FA) uz jednokratne zaporke (OTP). Sustav se sastoji od dvije Python skripte – klijenta i servera – koje međusobno komuniciraju putem TCP socket veze.

Korisnik se prvo prijavljuje unosom korisničkog imena i lozinke u klijentsku skriptu. Ove vjerodajnice se šalju serveru, koji ih provjerava prema unaprijed definiranoj listi korisnika spremljenoj u lokalnoj datoteci ili u rječniku unutar skripte. Ako su vjerodajnice točne, server generira jednokratnu zaporku temeljenu na vremenu i tajnom ključu (preporučuje se korištenje TOTP metode), te ju šalje klijentu kao simulaciju drugog faktora (umjesto stvarnog slanja putem SMS-a ili e-maila).

Klijent prikazuje primljenu jednokratnu zaporku korisniku (ili ju generira lokalno koristeći isti tajni ključ i prikazuje korisniku), a korisnik mora unijeti tu zaporku kako bi dovršio autentifikaciju. Server tada provjerava unesenu zaporku uspoređujući je s vlastitom generiranom vrijednošću i odlučuje je li pristup dozvoljen.

Autentifikacija je uspješna samo ako su oba faktora točna – korisničko ime i lozinka, te OTP kod. Komunikacija između klijenta i servera mora se odvijati preko TCP veze, a svi koraci moraju biti jasno ispisani u terminalu korisnika i operatora servera.

Preporučuje se korištenje biblioteka `hmac`, `hashlib`, `time` i po potrebi `base64`, dok je implementacija TOTP algoritma moguća i ručno (na temelju vremenskih intervala i HMAC-SHA1).

## Napomena

Za naprednije korisnike, zadatak se može proširiti dodavanjem vremenskih ograničenja za važenje OTP koda, brojačima neuspjelih pokušaja, ili povezivanjem s datotekom u kojoj se pohranjuju korisnički računi i tajni ključevi.
