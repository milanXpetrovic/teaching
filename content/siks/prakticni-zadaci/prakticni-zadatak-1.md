# Praktični zadatak 1: Uvod u kriptografiju

## Opis zadatka

U ovom zadatku implementirat ćete komunikaciju između dviju Python skripti, klijenta i servera, koje razmjenjuju šifrirane poruke koristeći različite metode simetričnog šifriranja. Klijent unosi poruku, odabire algoritam šifriranja (Caesarova ili Vigenèreova šifra), zatim unosi odgovarajući parametar (pomak ili ključ) te šifrira poruku. Tako šifrirana poruka šalje se serveru putem TCP socket veze, razmjena poruka treba biti višestruka unutar jedne sesije.

Na strani servera, zaprimljena poruka se analizira. Prvo se parsira odabrani algoritam, zatim se prema priloženom parametru provodi dešifriranje. Ako je poruka šifrirana Caesarovom šifrom, server će prikazati sve moguće varijante dešifriranja pomoću brute-force pristupa, a zatim ispravno dešifrirati poruku pomoću dostavljenog pomaka. Ako je korištena Vigenèreova šifra, server će jednostavno upotrijebiti priloženi tekstualni ključ za dešifriranje poruke i ispisati originalni tekst.

Poruka koju klijent šalje serveru mora biti u tekstualnom formatu koji sadrži tri dijela razdvojena znakom `|`, i to redom: naziv algoritma (caesar ili vigenere), parametar (broj za caesar, tekst za vigenere), te šifrirani tekst. Na primjer: `caesar|3|KHOOR`.

Obje skripte moraju koristiti vlastite implementacije algoritama za šifriranje i dešifriranje, bez korištenja vanjskih biblioteka za kriptografiju. Potrebno je omogućiti osnovnu validaciju unosa na strani klijenta (npr. provjera da je pomak broj), kao i jasan ispis rezultata na strani servera (uključujući sve pokušaje brute-force dešifriranja kod Caesarove šifre).
