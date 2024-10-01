---
layout: default
parent: PRSP
nav_order: 2
---

# [Vremenska složenost](https://cses.fi/book/book.pdf#chapter.2)

## [Najveći zbroj podniza](https://en.wikipedia.org/wiki/Maximum_subarray_problem)

Zadan je niz od $n$ brojeva, naš zadatak je izračunati najveći zbroj podniza, tj. najveći mogući zbroj niza uzastopnih vrijednosti u nizu.

U zadanom nizu:

```text
2, -3, 1, 5, -2, 3, 5, -2
```

Najveći zbroj podniza iznosi **12**:

```text
1, 5, -2, 3, 5
```

## Zadatak 1: $O(n^3)$ složenost

Pomoću prethodnog primjera danog u C++ napišite Python kod koji traži vrijednost najvećeg zbroja podniza i ima složenost od $O(n^3)$.

**Input:**
Lista $l$ koja sadržava $n$ cijelih brojeva $k$, $( -\infty < k < \infty)$

**Output:**
Broj $z$ koji je iznos maksimalnog zbroja podniza.

### Primjer 1

**Input:**

```text
-1 2 4 -3 5 2 -5 2
```

**Output:**

```text
10
```

## Zadatak 2: $O(n^2)$ složenost

Optimizirajte prethodni algoritam tako da njegova složenost iznosi $O(n^2)$.

## Zadatak 3: $O(n)$ složenost

Napišite Python kod koji traži najveći zbroj podniza s vremenskom složenosti $O(n)$.

{: .highlight }
Ovaj problem moguće je riješiti samo jednom iteracijom kroz listu, odnosno sa složenosti $O(n)$ pomoću [Kadane algoritma](https://en.wikipedia.org/wiki/Joseph_Born_Kadane).

Ideja je izračunati, za svaku poziciju niza, maksimalni zbroj podniza koji završava na toj poziciji. Nakon ovoga potrebno je pronaći maksimalnu vrijednost od tih zbrojeva. Ako razmotrimo podproblem pronalaženja podniza maksimalnog zbroja koji završava na položaju $k$.

Postoje dvije mogućnosti:

1. Podniz sadrži samo element na poziciji $k$.
2. Podniz se sastoji od podniza koji završava na poziciji $k-1$, nakon čega slijedi
element na poziciji $k$.

U drugom slučaju, budući da želimo pronaći podniz s maksimalnim zbrojem, podniz koji završava na poziciji $k-1$ također treba imati maksimalni zbroj. Tako, problem možemo učinkovito riješiti izračunavanjem maksimalnog zbroja podniza za svaku krajnju poziciju s lijeva na desno.

**Implementacije navedenog algoritma:**

```cpp
int best = 0, sum = 0;
for (int k = 0; k < n; k++) {
    sum = max(array[k], sum+array[k]);
    best = max(best, sum);
}
cout << best << "endl";
```

## Zadatak 4: Lista nasumičnih brojeva

Kreirajte funkciju koja generira listu $l$ čiji su elementi nasumično odabrani cijeli brojevi $k$ $( - 10 < k < 10)$.

**Input**
Duljina liste $n$, određuje broj elemenata u listi.

**Output**
Lista $l$ koja sadržava $n$ elemenata.

### Primjer 2

**Input:**

```text
15
```

**Output:**

```text
-1, 4, -9, -2, -1, 3, -6, 5, 8, 0, 3, -8, 6, 7, 3
```

## Zadatak 5: Mjerenje brzine izvođenja

Iskoristite prethodno definirane funkcije u prethodnim zadacima i usporedite brzinu izvođenja algoritama.

**Input**
Duljina liste $n$, određuje broj elemenata u listi, za generiranje liste iskoristite funkciju iz prethodnog zadatka.

**Output**
Vremena $t_1$, $t_2$ i $t_3$ koja označavaju vrijeme izvođenja algoritama.

### Primjer 3

**Input:**

```text
1000
```

**Output:**

```text
9.2702
0.0670
0.0010
```

## Zadaci za vježbu

- [CSES: Repetitions](https://cses.fi/problemset/task/1069)

[Sljedeća lekcija: Potpuno pretraživanje](../potpuna-pretraga){: .btn .btn-purple .float-right}