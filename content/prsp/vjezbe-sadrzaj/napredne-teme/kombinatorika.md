---
layout: default
parent: PRSP
nav_order: 12
nav_exclude: true
---

# Vježbe 12: Kombinatorika

## Zadatak 5: Niz

Razmotrimo znakovni niz koji se sastoji od svih pozitivnih cijelih brojeva u rastućem redoslijedu:

```text
12345678910111213141516171819202122232425...
```

Zadatak je pronaći u $q$ upita koja znamenka se nalazi na poziciji $k$.

Polje kreće od indeksa 1, tako će primjerice upit za broj 6, vratiti broj 6 a ne 7.

**Input:**
Prva linija sadrži broj $q$ koji nam govori koliko imamo upita.
Nakon toga slijedi $q$ linija gdje se nalazi $k$, odnosno indeks broja kojeg tražimo.

**Output:**
Za svaki upit ispišite pronađenu znamenku na indeksu $k$.

**Input:**

```text
3
7
19
12
```

**Output:**

```text
7
4
1
```