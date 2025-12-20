---
nav_exclude: true
---

# Algoritmi na stablima i LCA

## Sadržaj

1. [Osnovni pojmovi i svojstva](#osnovni-pojmovi-i-svojstva)
2. [Obilazak stabla i DFS poredak](#obilazak-stabla-i-dfs-poredak)
3. [Promjer stabla (Tree Diameter)](#promjer-stabla-tree-diameter)
4. [Najmanji zajednički predak (LCA)](#najmanji-zajednički-predak-lca)
5. [Upiti nad putevima (Udaljenost i Sume)](#upiti-nad-putevima-udaljenost-i-sume)
6. [Upiti nad podstablima (Subtree Queries)](#upiti-nad-podstablima-subtree-queries)
7. [Zadaci za vježbu](#zadaci-za-vježbu)

---

# Preporučena literatura: Algoritmi na stablima

Za dublje razumijevanje algoritama na stablima, LCA i upita:

* **CPH (Competitive Programmer's Handbook):**
  * **Poglavlje 14:** *Tree algorithms* (Osnovni pojmovi, obilazak, promjer, najduži putevi).
  * **Poglavlje 18:** *Tree queries* (LCA, Binary Lifting, spajanje puteva, upiti nad podstablima).
* **CLRS (Introduction to Algorithms):**
  * **Poglavlje 22:** *Elementary Graph Algorithms* (Temelj za DFS/BFS obilaske).
  * **Poglavlje 19:** *Fibonacci Heaps* (Za naprednije grafovske algoritme koji se koriste i na stablima).
* **CP-Algorithms:**
  * Sekcija *Graph Traversal* (LCA, Lowest Common Ancestor).

---

## Osnovni pojmovi i svojstva

Stablo je povezan graf koji se sastoji od $N$ čvorova i $N-1$ bridova te ne sadrži cikluse. Ovo je jedna od najvažnijih struktura u računalnoj znanosti jer se mnoga svojstva mogu izračunati puno efikasnije nego na općenitim grafovima.

**Ključna svojstva:**

* Postoji točno jedan jednostavan put između bilo koja dva čvora.
* Dodavanjem bilo kojeg brida stvara se ciklus.
* Micanjem bilo kojeg brida stablo prestaje biti povezano.

**Terminologija:**

* **Korijen (Root):** Ako fiksiramo jedan čvor kao korijen, stablo postaje *ukorijenjeno*.
* **List (Leaf):** Čvor koji ima samo jednog susjeda (u ukorijenjenom stablu: nema djece).
* **Dubina (Depth):** Udaljenost čvora od korijena.
* **Podstablo (Subtree):** Stablo koje čini čvor i svi njegovi potomci.

---

## Obilazak stabla i DFS poredak

Obilazak stabla najčešće radimo pomoću DFS-a. Osim samog posjećivanja, izuzetno je korisno pamtiti **ulazna (entry)** i **izlazna (exit)** vremena za svaki čvor. Ova tehnika se često naziva **"Tree Flattening"** ili **Linearizacija stabla**.

Pomoću ovih vremena možemo preslikati stablo na ravni niz, gdje svaki podstablo postaje kontinuirani raspon (subarray).

### Implementacija s ulaznim/izlaznim vremenima

```cpp
vector<int> adj[MAXN];
int tin[MAXN], tout[MAXN]; // Entry i Exit vremena
int timer;

void dfs(int u, int p) {
    tin[u] = ++timer; // Bilježimo vrijeme ulaska
    
    for (int v : adj[u]) {
        if (v != p) {
            dfs(v, u);
        }
    }
    
    tout[u] = timer; // Bilježimo vrijeme izlaska (nakon obrade svih potomaka)
}
```

**Svojstvo predaka:**
Čvor $u$ je predak čvora $v$ ako i samo ako vrijedi:
$$ tin[u] \le tin[v] \quad \text{i} \quad tout[u] \ge tout[v] $$

Ovo nam omogućuje provjeru je li neki čvor predak drugome u **O(1)** vremenu.

---

## Promjer stabla (Tree Diameter)

**Promjer stabla** je maksimalna udaljenost između bilo koja dva čvora u stablu.
Postoje dva standardna pristupa za računanje promjera:

### 1. Algoritam pomoću dva DFS-a

Ovaj pristup je jednostavan i radi u $O(N)$ vremenu.

1. Odaberi proizvoljan čvor $A$ i pronađi najudaljeniji čvor od njega (nazovimo ga $B$) koristeći DFS.
2. Pokreni DFS iz čvora $B$ i pronađi najudaljeniji čvor od njega (nazovimo ga $C$).
3. Udaljenost između $B$ i $C$ je promjer stabla.

### 2. Dinamičko programiranje

Za svaki čvor $u$ računamo:

* `toLeaf(u)`: maksimalna dubina u podstablu čvora $u$ (udaljenost do najdaljeg lista).
* `maxLength(u)`: najduži put koji prolazi kroz $u$ i ostaje u potpunosti unutar njegovog podstabla. To je zbroj dvije najveće `toLeaf` vrijednosti njegove djece.

---

## Najmanji zajednički predak (LCA)

Najmanji zajednički predak (**Lowest Common Ancestor - LCA**) čvorova $u$ i $v$ je čvor koji je predak i od $u$ i od $v$, a nalazi se na najvećoj dubini (najdalje od korijena).

Najpopularnija metoda u natjecateljskom programiranju je **Binarno podizanje (Binary Lifting)**.

### Binarno podizanje (Binary Lifting)

Ideja je za svaki čvor unaprijed izračunati njegove pretke na udaljenostima koje su potencije broja 2 ($1, 2, 4, 8, \dots$).
Neka je `up[u][i]` predak čvora $u$ na udaljenosti $2^i$.

**Rekurzivna relacija:**
$$ up[u][i] = up[up[u][i-1]][i-1] $$

**Vremenska složenost:**

* Predračun (Preprocessing): $O(N \log N)$
* Upit (Query): $O(\log N)$

#### Implementacija

**1. Predračun (Preprocessing)**

```cpp
const int LOG = 20; 
int up[MAXN][LOG];  
int depth[MAXN];

void dfs_lca(int u, int p, int d) {
    depth[u] = d;
    up[u][0] = p; // 2^0 = 1. predak je roditelj
    
    for (int i = 1; i < LOG; i++) {
        up[u][i] = up[up[u][i-1]][i-1];
    }
    
    for (int v : adj[u]) {
        if (v != p) dfs_lca(v, u, d + 1);
    }
}
```

**2. Funkcija za LCA upit**

```cpp
int get_lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    
    // 1. Izjednači dubine
    for (int i = LOG - 1; i >= 0; i--) {
        if (depth[u] - (1 << i) >= depth[v]) {
            u = up[u][i];
        }
    }
    
    if (u == v) return u;
    
    // 2. Podiži oba dok ne budu točno ispod LCA
    for (int i = LOG - 1; i >= 0; i--) {
        if (up[u][i] != up[v][i]) {
            u = up[u][i];
            v = up[v][i];
        }
    }
    
    return up[u][0];
}
```

---

## Upiti nad putevima (Udaljenost i Sume)

### Udaljenost između čvorova

Put od $u$ do $v$ ide od $u$ gore do LCA, a zatim dolje do $v$.
Formula za duljinu puta (broj bridova):

$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

### Sume na putu (Path Aggregates)

Ako čvorovi imaju težine/vrijednosti i želimo zbroj vrijednosti na putu od $u$ do $v$, koristimo tehniku **prefiksnih suma na stablu**.
Neka je `P[u]` zbroj vrijednosti od korijena do čvora $u$.

Zbroj vrijednosti na putu između $u$ i $v$ je:
$$ PathSum(u, v) = P[u] + P[v] - 2 \cdot P[LCA(u, v)] + Value(LCA(u, v)) $$

*(Napomena: Dodajemo `Value(LCA)` jer smo ga dvaput oduzeli, a on je dio puta).*

---

## Upiti nad podstablima (Subtree Queries)

Često moramo odgovoriti na upite poput: "Promijeni vrijednost čvora $u$" i "Koliki je zbroj vrijednosti u cijelom podstablu čvora $v$?".

Ovdje koristimo **DFS ulazna i izlazna vremena** (opisana u poglavlju 2).
Svojstvo linearizacije je sljedeće:
> Podstablo čvora $u$ odgovara kontinuiranom rasponu indeksa $[tin[u], tout[u]]$ u DFS obilasku.

Time smo problem na stablu sveli na **problem na nizu** (Range Sum Query).

**Postupak:**

1. Napravimo niz `vals` gdje na poziciju `tin[u]` zapišemo vrijednost čvora $u$.
2. Izgradimo **Fenwickovo stablo (BIT)** ili **Segmentno stablo** nad tim nizom.
3. **Update čvora $u$:** Ažuriramo indeks `tin[u]` u BIT-u.
4. **Upit za podstablo $u$:** Tražimo sumu raspona $[tin[u], tout[u]]$ u BIT-u.

```cpp
// Update vrijednosti čvora u
update_bit(tin[u], new_val - old_val);

// Suma podstabla čvora u
long long sum = query_bit(tout[u]) - query_bit(tin[u] - 1);
```

---

## Zadaci za vježbu

### CSES Problem Set

* **[Tree Diameter](https://cses.fi/problemset/task/1131):** Pronađi promjer stabla.
* **[Tree Distances I](https://cses.fi/problemset/task/1132):** Za svaki čvor nađi maksimalnu udaljenost do nekog drugog čvora (Rerooting tehnika).
* **[Company Queries I](https://cses.fi/problemset/task/1687):** Pronađi $k$-tog pretka (Binary Lifting).
* **[Company Queries II](https://cses.fi/problemset/task/1688):** Pronađi LCA dva čvora.
* **[Distance Queries](https://cses.fi/problemset/task/1135):** Pronađi udaljenost između dva čvora.
* **[Subtree Queries](https://cses.fi/problemset/task/1137):** Ažuriranje čvorova i sume podstabala (Linearizacija + BIT).
* **[Path Queries](https://cses.fi/problemset/task/1138):** Ažuriranje čvorova i sume na putu od korijena do $u$ (Linearizacija + BIT s rasponskim upitima).

### Codeforces

* **[Linova and Kingdom](https://codeforces.com/problemset/problem/1336/A):** Pohlepni pristup na stablu koristeći dubine i veličine podstabala.
* **[Sloth Naptime](https://codeforces.com/gym/102694/problem/C):** LCA i kretanje po stablu.

[Sljedeća lekcija: Algoritmi na stablima (dio 2) - Heavy-Light Decomposition](../content/15-HLD-and-Centroid) *(Opcionalno)*
