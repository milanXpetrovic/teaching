---
layout: default
parent: PRSP
nav_order: 9
nav_exclude: false
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

## Zadatak 3: Okružene regije

S obzirom na $m \times m$ matricu koja sadrži "X" i "O", osvojite sve regije koje su u 4 smjera okružene s "X".

Regija se osvaja pretvaranjem svih 'O' u 'X' u toj okruženoj regiji.

**Input:**

```console
X X X X
X O O X
X X O X
X O X X
```

**Output:**

```console
X X X X
X X X X
X X X X
X O X X
```

**Objašnjenje**:
Primijetite da se 'O' ne smije osvojiti jedino ako:

- Nalazi se na rubu matrice
- Nalazi se uz "O" koji se ne može osvojiti.

**Input:**

```console
X X X X X X X 
X O O O X X O 
X X X X X O O 
X X O X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

**Output:**

```console
X X X X X X X 
X X X X X X O 
X X X X X O O 
X X X X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

## Zadatak 4: Vrijeme putovanja

Martica $m \times m$ prikazuje vrijeme putovanja između gradova. Za zadani grad $n$ potrebno je pronaći najkraće vrijeme putovanja do svih ostalih, ako se svi gradovi u grafu ne mogu posjetiti, ispišite $-1$.

**Input:**
$n$ oznaka grada, $m$ ukupan broj gradova.
Slijedi $m$ redaka s $m$ cjelobrojnih vrijednosti.

**Output:**
Ispis udaljenosti do svih gradova ili $-1$ ako to nije moguće.

**Input:**

```console
3 5
0 5 3 2 5 
9 0 4 0 0 
7 6 0 2 8 
2 0 1 0 3 
0 7 5 5 0 
```
