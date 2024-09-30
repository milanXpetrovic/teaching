---
layout: default
title: Staze i ciklusi
parent: Grafovi
grand_parent: PRSP
nav_order: 6
---

# [Staze i ciklusi](https://cses.fi/book/book.pdf#chapter.19)


## Zadatak 7: Ciklus

Dobili ste usmjereni graf, a vaš zadatak je otkriti sadrži li negativan ciklus te dati primjer takvog ciklusa.

**Input:**
Prvi ulazni red ima dva cijela broja $n$ i $m$: broj čvorova i bridova. Čvorovi su označeni brojevima $1,2,…,n$.

Nakon toga, ulaz ima $m$ redaka koji opisuju veze. Svaki redak ima tri cijela broja $a$, $b$ i $c$ koji oynačuju da postoji brid od čvora $a$ do čvora $b$ čija je duljina $c$.

**Output:**
Ako graf sadrži negativan ciklus, ispišite prvo "YES", a zatim čvorove u ciklusu ispravnim redoslijedom. Ako postoji više negativnih ciklusa, možete ispisati bilo koji od njih. Ako nema negativnih ciklusa, ispišite "NE".

**Input:**

```text
4 5
1 2 1
2 4 1
3 1 1
4 1 -3
4 3 -2
```

**Output:**

```text
YES
1 2 4 1
```
