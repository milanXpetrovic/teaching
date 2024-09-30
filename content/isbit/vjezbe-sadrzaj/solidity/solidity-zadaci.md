---
layout: default
parent: Solidity
grand_parent: ISBiT
nav_exclude: true
---

# Zadaci

## Omiljeni broj

Stvorite novi file `SimpleStorage.sol` u kojem ćete napisati vaš ugovor. Cilj vašeg ugovora je omogućiti unos i ispis omiljenog broja. Stvorite varijablu `favNum` u koju pohranjujete omiljeni broj, za pohranu kreirajte funkciju `store`, a za dohvaćanje vrijednosti kreirajte funkciju `retrieve`.

## Mapping

Kreirajte pametni ugovor koji omnogućuje unos imena osobe i broj godina. Za pohranu imena i broja godine koristite strukturu naziva Osoba. Omogućite pohranu proizvoljnog broja osoba u polje i omogućite nalaženje broja godina pomoću imena osobe.

## ToDo lista

Kreirajte ugovor koji sadrži funkcionalnosti rada sa poljem u kojem su pohranjene strukture, cilj je omogućiti umetanje, ažuriranje i čitanje iz polja.

Definirajte strukturu Zadatak koja sadrži varijable `opis` (`string`) i `obavljen` (`bool`).

Definirajte polje za pohranu naiva `zadaci`.

Definirajte funkcije:

- `stvori()`
- `azurirajTekst()`
- `get()`
- `obavljeno()`

## Event

Stvorite 2 eventa, prvi bilježi adresu pozivatelja i poruku, a drugi ne prima parametre. Zatim kreirajte funkciju koja izvšava 2 poziva eventa sa argumentima i jedan poziv eventa bez argumenata.

## Novčanik

Kreirajte ugovor koji ima ulogu jednostavnog novčanika. Svatko može slati Eth, a samo ga vlasnik može podići.

## FundMe

Stvorite ugovor koji omogućuje vlasniku da prima uplate od bilo koga, dok samo vlasnik ugovora može povući sredstva na svoj novčanik.

Na ugovoru se sve transakcije odvijaju u Etheru no potrebno je pretvoriti ETH -> USD, jer je potrebno imati uvid u stanje u USD.

U ugovoru omogućite ova svojstva:

- evidenciju koja svota novca nam je pristigla s koje adrese.
- minimalan iznos koji je potreban da bi se uplata ostvarila.
