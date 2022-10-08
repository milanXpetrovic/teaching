---
parent: PRSP
nav_order: 3
---

# Vježbe 3: Potpuna pretraga

Potpuna pretraga (*eng. Complete search*) opća je metoda koja se može koristiti za rješavanje gotovo svakog algoritamskog problema. Ideja je generirati sva moguća rješenja problema korištenjem grube sile (*eng. brute force*), a zatim odabrati najbolje rješenje ili prebrojati rješenja, ovisno o problemu.
Potpuna pretraga dobra je tehnika ako ima dovoljno vremena za prolazak kroz sva rješenja, jer je pretragu obično lako provesti i uvijek daje rješenje. Ako je potpuna pretraga prespora, možda će biti potrebne druge tehnike, poput pohlepnih algoritama ili dinamičkog programiranja.

## Uvod 1: Generiranje permutacija

Zadan je skup $\{0, 1, 2, ..., n\}$, pomoću rekurzije generirajte sve podskupove od zadanoga skupa.
Prilikom ispisa ne treba voditi računa o redoslijedu ispisa podskupova.

### Primjer

**Input:**
```
0 1 2
```

**Output:**
```
[]
[2]
[1]
[1, 2]
[0]
[0, 2]
[0, 1]
[0, 1, 2]
```

{: .highlight }
`[]` označava prazan skup $\emptyset$.


## Uvod 2

Kreirajte program koji pogađa lozinku koja se sastoji od 6, 7 i 8 nasumično zadanih cijelih brojeva.

Ispišite vrijeme koje je bilo potrebno za pogoditi lozinke.


## Zadatak 1

Kreirajte program koji za zadani broj godine, pronađite minimalni broj godine koji je strogo veći od zadanog i ima sve različite znamenke.

Napišite program koji na za zadanu godinu traži prvu sljedeću godinu koja sadrži sve različite znamenke.

**Input:**
Cijeli broj $y$ $(1000 ≤ y ≤ 9000)$ koji označava broj godine.

**Output:**

Cijeli broj - minimalna vrijednost godine koja je striktno veća od $y$ i sve znamenke su različite.

### Primjer

**Input:**
```
1987
```
**Output:**
```
2013
```

**Input:**
```
2013
```
**Output:**
```
2014
```

## Backtracking 

Backtracking algoritam počinje s praznim rješenjem i proširuje rješenje korak po korak. Pretraživanje rekurzivno prolazi kroz sve različite načine na koje se rješenje može konstruirati.


## Zadatak 2: Problem $n$ kraljica 

Zadatak je postaviti $n$ kraljica na šahovsku ploču dimenzija $n x n$ tako da se kraljice međusobno ne napadaju.

Na koliko je načina moguće postaviti kraljice na zadanu ploču?

U primjeru gdje je $n = 4$, postoje 2 načina za rasporediti krlajice.

```
-  Q  –  –
-  –  –  Q
Q  –  –  –
-  –  Q  –
```

```
-  -  Q  –
Q  –  –  -
-  –  –  Q
-  Q  -  –
```


**Primjer jednog od ispravnih načina postavljanja kraljica:**

```
Q  –  –  –  –  –  –  –
–  –  –  –  Q  –  –  –
–  –  –  –  –  –  –  Q
–  –  –  –  –  Q  –  –
–  –  Q  –  –  –  –  –
–  –  –  –  –  –  Q  –
–  Q  –  –  –  –  –  –
–  –  –  Q  –  –  –  –
```


**Input:**

The input has eight lines, and each of them has eight characters. Each square is either free (.) or reserved (*).

**Output:**

Print one integer: the number of ways you can place the queens.

Example

Input:
........
........
..*.....
........
........
.....**.
...*....
........

Output:
65


https://www.techiedelight.com/print-possible-solutions-n-queens-problem/


**Input:**

**Output:**

### Primjer

**Input:**
```
```

**Output:**
```
```


## Zadatak 3: Kombinacije brojeva od 1 do $n$

https://www.techiedelight.com/print-all-combination-numbers-from-1-to-n/


**Input:**

**Output:**

### Primjer

**Input:**
```
```

**Output:**
```
```


## Zadatak 4: Pruning the search