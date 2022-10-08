---
layout: default
parent: PRSP
nav_order: 8
nav_exclude: true
---

# Vježbe 8: Priprema - Kolokvij 1


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

