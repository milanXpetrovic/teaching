---
layout: default
parent: SIKS
nav_exclude: true
---

# Praktični zadatak 3: Autentifikacija i sažeci poruka

## Opis zadatka

U ovom zadatku potrebno je implementirati mehanizme za provjeru autentičnosti i integriteta poruka između dvije Python skripte: klijenta i servera. Cilj je da klijent pošalje poruku zajedno s digitalnim potpisom temeljenim na sažetku poruke i zajedničkom tajnom ključu. Server mora provjeriti autentičnost i integritet poruke analizom sažetka i upotrebom vlastitog ključa.

Klijent i server koriste unaprijed dogovoreni tajni ključ koji nije potrebno slati tijekom komunikacije. Klijent prvo unosi poruku i pomoću HMAC mehanizma generira autentifikacijski kod koristeći tajni ključ i jedan od algoritama sažimanja (npr. SHA-256). Dobiveni HMAC i originalna poruka šalju se serveru putem TCP veze.

Server po primitku poruke i HMAC-a izračunava vlastiti HMAC koristeći istu hash funkciju i poznati tajni ključ. Ako je generirani HMAC jednak primljenom, poruka se smatra autentičnom i neizmijenjenom, te se ispisuje. U suprotnom, server mora ispisati upozorenje da je došlo do izmjene poruke ili da je poruka neautorizirana.

Tijekom implementacije morate koristiti socket vezu za komunikaciju između klijenta i servera, te funkcije iz standardne biblioteke (modul `hmac` i `hashlib`). Algoritam hashiranja mora biti jasno naznačen u kodu i mora se koristiti dosljedno na obje strane.

## Napomena

Za dodatni izazov, proširite zadatak tako da se prilikom pokretanja klijenta bira algoritam sažimanja (npr. SHA-1, SHA-256 ili SHA-512), a server mora obraditi poruku ovisno o tom izboru.
