---
layout: default
parent: PRSP
nav_order: 20
nav_exclude: true
---

# Vježbe 8: Priprema - Kolokvij

{: .highlight }
Bonus zadaci se nalaze ovdje

## Zadatak 1

``` python

## https://codeforces.com/problemset/problem/352/A
## Zadano je n karti na svakoj karti nalazi se broj 0 ili 5. 
## pronadite najveci broj koji mozete generirati od dobivenih karti da je djeljiv sa 90.

from itertools import permutations

l = [x for x in input().split(" ")]
len_l = len(l)

max_n = -1

p = list(set(list(permutations(l, len_l))))
p = [int(n) for n in p]

for n in p:

    if len_l > len(n):
        continue

    if int(n) % 90 == 0:
        max_n = max(max_n, n)

print(max_n)
```

## Zadatak 2

U prostoriji dimenzija a x b potrebno je smjestiti n učenika. Oko svakog učenika potrebno je ostaviti jedno polje razmaka.

**Input:**
a b, dimenzije prostorije
n broj studenata

**Output:**
Ispiši 1 ako je moguće u zadanu prostoriju smjestiti n učenika inače -1.

Input
4, 4
3
Output
1

## Zadatak 3

Meet in the middle

Pronađi ako je moguće iz zadane liste brojeva l, zbrajanjem njenih članova dobiti broj x.

## Zadatak 4

https://www.techiedelight.com/find-all-paths-from-source-to-destination-in-matrix/

## Zadatak 
https://www.techiedelight.com/print-possible-solutions-n-queens-problem/

## Zadatak 2: Problem $n$ kraljica 
Problem $n$ kraljica je problem postavljanja $n$ kraljica na šahovsku ploču dimenzija $n \times n$ tako da se kraljice međusobno ne napadaju. Cilj je odrediti ukupan broj načina postavljanja kraljica na ploču.

{: .highlight-title}
> Kako kraljica napada?
>
> Prikaz ploče dimenzija 8 x 8 i polja koja kraljica (Q) napada (\*).
>
> ```
> -  –  *  –  –  –  *  –
> –  –  *  –  -  *  –  –
> *  –  *  –  *  –  –  -
> –  *  *  *  –  -  –  –
> *  *  Q  *  *  *  *  *
> –  *  *  *  –  –  -  –
> *  -  *  –  *  –  –  –
> –  –  *  -  –  *  –  –
> ```

U primjeru gdje je $n = 4$, postoje 2 načina za rasporediti kraljice.

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

Zadatak je napisati program koji ispisuje ukupan broj mogućnosti za postavljanje kraljica na ploču.

**Input:**
Broj $n$ označava broj kraljica i dimenzije ploče $n \times n$ $(4 \le n \le 8)$. 

**Output:**
Broj $m$ načina na koje možete postaviti kraljice.

### Primjer

**Input:**
```
4
```

**Output:**

```
2
```

**Input:**

```
8
```

**Output:**

```
92
```

## Zadatak 3: Kombinacije brojeva od 1 do $n$

Za dan pozitivan cijeli broj $n$ $(2 \le n \le 1000)$, ispišite sve kombinacije brojeva između 1 i $n$, gdje njihov zbroj iznosi $n$.

**Input:**
Cijeli broj $n$ $(1 <= n <= 1000)$ koji označava traženu sumu.

**Output:**


### Primjer
**Input:**
```
4
```

**Output:**
```
4
1 3
2 2
1 1 2
1 1 1 1
```

**Input:**
```
5
```

**Output:**
```
5
1 4
2 3
1 1 3
1 2 2
1 1 1 2
1 1 1 1 1
```

Različite znamenke 
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