---
layout: default
title: Putovanje kroz graf
parent: Grafovi
grand_parent: PRSP
nav_order: 1
---

# [Putovanje kroz graf](https://cses.fi/book/book.pdf#chapter.11)



## Depth first search (DFS) – pretraživanje u dubinu
DFS (Depth-First Search) je algoritam obilaska grafa koji se temelji na ideji putovanja u dubinu iz odabranog početnog čvora (granu po granu). Počevši od korijena, ovaj algoritam istražuje što dublje u grafu prije nego se vrati unatrag kako bi istražio druge grane. Često se koristi stog (stack) kao memorijska struktura za praćenje puta i čvorova. DFS je koristan za pronalaženje rješenja problema kao što su topološko sortiranje, pretraga rute u mrežama ili pronalazak putanja u grafu.

```python
def dfs(graph, start):
    visited, stack = [], [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            stack.extend([i for i in graph[vertex] if i not in visited])
    return visited
```

## Breadth first search (BFS) – pretraživanje u širinu

BFS (Breadth-First Search) je algoritam obilaska grafa, koji radi na principu širenja u dubinu od zadanog početnog čvora. Počevši od korijena, ovaj algoritam istražuje sve čvorove na jednoj razini dubine prije nego što prijeđe na čvorove na sljedećoj razini. Često se korišti reda (queue) kao memorijska struktura za pamćenje čvorova koje treba posjetiti. Ovaj algoritam je koristan kada se traži put s najmanje koraka od početnog do odredišnog čvora i provjeri povezanosti u mrežama.

U nastavku je prikazan kod koji implementira BFS (Breadth-First Search) algoritam za obilazak grafa počevši od odabranog čvora `start`. Funkcija `bfs` koristi skup `visited` za praćenje posjećenih čvorova i red `queue` za provjeru susjednih čvorova. Petlja se izvršava dok god postoji čvor u redu `queue`. Funkcija vraća skup posjećenih čvorova `visited`.

```python
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend([i for i in graph[vertex] if i not in list(visited)])

    return visited
```

## Zadatak 1: Broj otoka

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađite broj otoka.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava broj otoka.

**Input:**

```text
4 5
1 1 1 1 0
1 1 0 1 0
1 1 0 0 0
0 0 0 0 0
```

**Output:**

```text
1
```

**Input:**

```text
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

**Output:**

```text
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

```text
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

```text
6
```

## Zadatak 3: Okružene regije

S obzirom na $m \times m$ matricu koja sadrži "X" i "O", osvojite sve regije koje su u 4 smjera okružene s "X".

Regija se osvaja pretvaranjem svih 'O' u 'X' u toj okruženoj regiji.

**Input:**

```text
X X X X
X O O X
X X O X
X O X X
```

**Output:**

```text
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

```text
X X X X X X X 
X O O O X X O 
X X X X X O O 
X X O X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

**Output:**

```text
X X X X X X X 
X X X X X X O 
X X X X X O O 
X X X X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

## Zadatak 4: Timovi

U razredu ima $n$ učenika i $m$ prijateljstava među njima. Vaš zadatak je podijeliti učenike u dva tima na način da dva učenika u timu nisu prijatelji. Možete slobodno odabrati veličinu timova.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj učenika i prijateljstava. Zjenice su označene brojevima $1,2,…,n$.

Zatim sljedi $m$ redaka koji opisuju prijateljstva. Svaki red ima dva cijela broja $a$ i $b$: učenici $a$ i $b$ su prijatelji.

Svako prijateljstvo je između dva različita učenika i postoji najviše jedno prijateljstvo između ta dva učenika.

**Output:**
Ispišite primjer kako sastaviti timove. Za svakog učenika ispišite "1" ili "2" ovisno u koju će ekipu učenik biti dodijeljen.

Ako nema rješenja ispisati "NEMA".

**Input:**

```text
5 3
1 2
1 3
4 5
```

**Output:**

```text
1 2 2 1 2
```

[Sljedeća lekcija: Najkraći put](../najkraci-put){: .btn .btn-purple .float-right}
