---
layout: default
title: Najkraci put
parent: Grafovi
grand_parent: PRSP
nav_order: 2
---

# [Najkraći put](https://cses.fi/book/book.pdf#chapter.13)

Pronalaženje najkraćeg puta između dva čvora grafa važan je problem koji ima mnogo praktičnih primjena. Na primjer, pronaći najkraću moguću duljinu rute između dva grada u cestovnoj mreži, s obzirom na duljine cesta.

U grafu koji nema težine, odnosno svaka veza ima težinu $1$, duljina puta između dva vrha jednaka je broju bridova, možemo jednostavno upotrijebiti pretraživanje u širinu kako bismo pronašli najkraći put. Međutim, u težinskim grafovima kompleksniji algoritmi su potrebni za pronalaženje najkraćih puteva, stoga su u ovom poglavlju prikazani algoritmi za traženje najkraćih puteva u težinskim grafovima.

## [Bellman-Fordov algoritam](https://cses.fi/book/book.pdf#chapter.13.1)

Bellman-Ford algoritam pronalazi duljinu najkraćeg puta od nekog početnog vrha do svih ostalih vrhova u grafu. Algoritam radi na svim tipovima grafova pod uvjetom da nemaju ciklus s negativnom sumom težina. Ako u grafu postoji ciklus s negativnom težinom, ovaj algoritam to može detektirati.

## [Dijkstrin algoritam](https://cses.fi/book/book.pdf#chapter.13.2)

Dijkstrin algoritam, kao i Bellman-Ford, pronalazi duljine najkraćih puteva od početnog vrha do svih ostalih. Prednost ovog algoritma je što je brži od Bellman-Forda pa ga možemo koristiti i na većim grafovima. Njegov nedostatak je što zahtijeva da graf nema bridove negativne težine što nije bio uvjet za Bellman-Ford.

Ideja algoritma je slična BFS-u jer u svakom koraku obrađujemo jedan vrh i dodajemo u red njegove susjede koji još nisu obrađeni. Razlika je u tome što će ovoga puta vrh koji idući obrađujemo uvijek biti onaj koji trenutno ima najmanju udaljenost od početnog.

## [Floyd-Warshallov algoritam](https://cses.fi/book/book.pdf#chapter.13.3)

Floyd-Warshall algoritam za razliku od prethodna dva traži najkraći put između svaka dva vrha grafa. Iz tog razloga ovoga puta koristimo 2D matricu distance u kojoj su zapisane udaljenosti među vrhovima. Na početku zaisujemo samo udaljenosti vrhova između kojih postoji brid, a ostale postavljamo na beskonačno. Kasnije kombinacijom bridova se izračunavaju i ostale udaljenosti.

## Zadata 1: BFS Uvod

Iskoristite funkcije za generiranje grafa koji nema težine iz cjeline [Grafovi: uvod](../grafovi-uvod.md) i stvorit graf koji se sastioji od 100 vrhova. Pronađite udaljenost između vrhova $1$ i $100$.

## Zadatak 2: Vrijeme putovanja

Matrica $m \times m$ prikazuje vrijeme putovanja između gradova. Za zadani grad $n$ potrebno je pronaći najkraće vrijeme putovanja do svih ostalih, ako se svi gradovi u grafu ne mogu posjetiti, ispišite $-1$.

**Input:**
$n$ oznaka grada, $m$ ukupan broj gradova.
Slijedi $m$ redaka s $m$ cjelobrojnih vrijednosti.

**Output:**
Ispis udaljenosti do svih gradova ili $-1$ ako to nije moguće.

**Input:**

```text
3 5
0 5 3 2 5 
9 0 4 0 0 
7 6 0 2 8 
2 0 1 0 3 
0 7 5 5 0 
```

<!-- [Sljedeća lekcija: Najkraći put](../najkraci-put){: .btn .btn-purple .float-right} -->
