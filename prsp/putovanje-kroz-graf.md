---
layout: default
parent: PRSP
nav_order: 9
nav_exclude: true
---

# Putovanje kroz graf

## Zadatak 1: Broj otoka

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađte broj otoka.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava broj otoka.

**Input:**

```console
4 5
1 1 1 1 0
1 1 0 1 0
1 1 0 0 0
0 0 0 0 0
```

**Output:**

```console
1
```

**Input:**

```console
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

**Output:**

```console
3
```

## Zadatak 2: Najveći otok

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađite otok s najvećom površinom, ako nema otoka vratite 0.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava površinu najvećeg otoka.

**Input:**

```console
8 13
0 0 1 0 0 0 0 1 0 0 0 0 0 
0 0 0 0 0 0 0 1 1 1 0 0 0 
0 1 1 0 1 0 0 0 0 0 0 0 0 
0 1 0 0 1 1 0 0 1 0 1 0 0 
0 1 0 0 1 1 0 0 1 1 1 0 0 
0 0 0 0 0 0 0 0 0 0 1 0 0 
0 0 0 0 0 0 0 1 1 1 0 0 0 
0 0 0 0 0 0 0 1 1 0 0 0 0
```

**Output:**

```console
6
```
