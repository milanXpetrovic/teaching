---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Algoritmi na stablima i LCA"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title  -->
# Algoritmi na stablima i LCA

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Osnovni pojmovi i svojstva**
   - Definicija stabla
   - Terminologija
2. **Obilazak stabla i DFS poredak**
   - Linearizacija (entry/exit times)
3. **Promjer stabla (Tree Diameter)**
   - Algoritam s dva DFS-a
4. **Najmanji zajednički predak (LCA)**
   - Binarno podizanje (Binary Lifting)
5. **Upiti nad putovima i podstablima**
   - Udaljenost, sume na putu
   - Flattening + BIT

---

<!-- _class: lead -->
# Osnovni pojmovi

## Što je stablo?

---

# Definicija i svojstva

**Stablo** je povezan graf koji se sastoji od $N$ čvorova i $N-1$ bridova te ne sadrži cikluse.

**Ključna svojstva:**

1. Između bilo koja dva čvora postoji točno jedan jednostavan put.
2. Dodavanjem bilo kojeg brida stvara se ciklus.
3. Micanjem bilo kojeg brida stablo prestaje biti povezano.

**Terminologija:**

- **Korijen (root):** fiksirani čvor od kojeg "visi" stablo.
- **List (leaf):** čvor bez djece (u ukorijenjenom stablu) ili stupnja 1.
- **Dubina (depth):** udaljenost čvora od korijena.
- **Podstablo (subtree):** čvor i svi njegovi potomci.

---

<!-- _class: lead -->
# Obilazak stabla

## DFS poredak i linearizacija

---

# Linearizacija stabla (tree flattening)

Osim samog posjećivanja, korisno je pamtiti **ulazna (entry)** i **izlazna (exit)** vremena za svaki čvor.
To nam omogućuje da stablo preslikamo na ravni niz.

```cpp
vector<int> adj[MAXN];
int tin[MAXN], tout[MAXN], timer;

void dfs(int u, int p) {
    tin[u] = ++timer; // Vrijeme ulaska

    for (int v : adj[u]) {
        if (v != p) dfs(v, u);
    }

    tout[u] = timer;  // Vrijeme izlaska (zadnji tin u podstablu)
}
```

**Svojstvo predaka:**
Čvor $u$ je predak čvora $v$ ako i samo ako vrijedi:
$$ tin[u] \le tin[v] \quad \text{i} \quad tout[u] \ge tout[v] $$

---

<!-- _class: lead -->
# Promjer stabla

## Najdulji put u stablu

---

# Kako pronaći promjer?

**Promjer stabla** je maksimalna udaljenost između bilo koja dva čvora.

**Algoritam s dva DFS-a ($O(N)$)**

1. Odaberemo proizvoljan čvor $A$ (npr. korijen).
2. DFS-om pronađemo čvor najudaljeniji od $A$. Nazovimo ga $B$.
3. Pokrenemo DFS iz čvora $B$ i pronađemo čvor najudaljeniji od njega. Nazovimo ga $C$.
4. Udaljenost između $B$ i $C$ je promjer stabla.

*(Alternativa: dinamičko programiranje na stablu, gdje u svakom čvoru zbrojimo dva najdulja "kraka" prema djeci.)*

---

<!-- _class: lead -->
# Najmanji zajednički predak (LCA)

## Lowest Common Ancestor

---

# Problem LCA

**Definicija:** LCA čvorova $u$ i $v$ je čvor koji je predak i od $u$ i od $v$, a nalazi se na najvećoj dubini (najdalje od korijena).

**Metoda: binarno podizanje (binary lifting)**
Unaprijed izračunamo pretke na udaljenostima $2^0, 2^1, 2^2, \dots$.
Neka je `up[u][i]` predak čvora $u$ na udaljenosti $2^i$.

**Rekurzivna relacija:**
$$ up[u][i] = up[up[u][i-1]][i-1] $$
*(Predak na udaljenosti $2^i$ je predak na udaljenosti $2^{i-1}$ od pretka na udaljenosti $2^{i-1}$.)*

**Složenost:**

- Preprocessing: $O(N \log N)$
- Upit: $O(\log N)$

---

# Implementacija: preprocessing

```cpp
const int LOG = 20;
int up[MAXN][LOG];
int depth[MAXN];

// Poziv: dfs_lca(korijen, 0, 0). Čvor 0 služi kao "iznad korijena".
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

---

# Implementacija: LCA upit

```cpp
int get_lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v); // Sada je u dublji

    // 1. Izjednačimo dubine: podižemo dubljeg u na razinu v
    for (int i = LOG - 1; i >= 0; i--) {
        if (depth[u] - (1 << i) >= depth[v]) {
            u = up[u][i];
        }
    }

    if (u == v) return u;

    // 2. Podižemo oba dok ne budu točno ispod LCA
    for (int i = LOG - 1; i >= 0; i--) {
        if (up[u][i] != up[v][i]) {
            u = up[u][i];
            v = up[v][i];
        }
    }
    return up[u][0]; // Vraćamo roditelja
}
```

---

<!-- _class: lead -->
# Upiti nad putovima

## Udaljenosti i sume

---

# Udaljenost i sume na putu

Jednom kad imamo LCA, lako računamo udaljenosti. Put od $u$ do $v$ ide $u \to LCA \to v$.

**Udaljenost (broj bridova)**
$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

**Suma vrijednosti čvorova na putu**
Koristimo prefiksne sume od korijena do čvora (`P[u]`, uključujući i sam čvor $u$).
$$ PathSum(u, v) = P[u] + P[v] - 2 \cdot P[LCA(u, v)] + Value(LCA(u, v)) $$

*(Dodajemo `Value(LCA)` jer smo ga dvaput oduzeli, a on je dio puta.)*

---

<!-- _class: lead -->
# Upiti nad podstablima

## Subtree Queries

---

# Linearizacija + strukture podataka

Često imamo upite: "promijeni vrijednost čvora $u$" i "daj sumu podstabla $v$".

**Ključna ideja:**
Podstablo čvora $u$ odgovara kontinuiranom rasponu indeksa $[tin[u], tout[u]]$ u DFS obilasku.

**Rješenje:**

1. Vrijednosti čvorova preslikamo u niz na pozicije `tin[u]`.
2. Nad tim nizom izgradimo **Fenwickovo stablo (BIT)** ili **segmentno stablo**.
3. **Update:** ažuriramo indeks `tin[u]` u BIT-u.
4. **Query:** suma raspona $[tin[u], tout[u]]$ u BIT-u.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES Problem Set

---

# Zadaci

1. **[Tree Diameter](https://cses.fi/problemset/task/1131)**
   - Promjer stabla (2x DFS).
2. **[Company Queries I](https://cses.fi/problemset/task/1687) i [II](https://cses.fi/problemset/task/1688)**
   - K-ti predak i LCA (binary lifting).
3. **[Distance Queries](https://cses.fi/problemset/task/1135)**
   - Udaljenost između čvorova pomoću LCA.
4. **[Subtree Queries](https://cses.fi/problemset/task/1137)**
   - Ažuriranje vrijednosti i suma podstabla (linearizacija + BIT).
5. **[Path Queries](https://cses.fi/problemset/task/1138)**
   - Ažuriranje i suma na putu od korijena (malo teže, ali sličan princip).

---

<!-- _class: title -->
# Tree Diameter (CSES)

## Najdulji put u stablu

---

# Analiza: Tree Diameter

**Problem:**
Zadano je stablo od $N$ čvorova. Treba pronaći promjer stabla (maksimalnu udaljenost između dva čvora).
**Ograničenja:** $N \le 2 \cdot 10^5$.

**Intuicija (2x DFS)**
Naivni pristup (BFS iz svakog čvora) je $O(N^2)$, presporo.
Postoji elegantan algoritam u $O(N)$:

1. Odaberemo proizvoljan čvor $x$ (npr. 1).
2. Pronađemo čvor najudaljeniji od $x$. Nazovimo ga $a$.
3. Pronađemo čvor najudaljeniji od $a$. Nazovimo ga $b$.
4. Udaljenost između $a$ i $b$ je promjer.

---

# Implementacija: Tree Diameter

```cpp
void dfs(int u, int p, int d, int &max_d, int &farthest_node) {
    if (d > max_d) {
        max_d = d;
        farthest_node = u;
    }
    for (int v : adj[u]) {
        if (v != p) dfs(v, u, d + 1, max_d, farthest_node);
    }
}

// U main funkciji:
int max_d = -1, node_a = -1, node_b = -1;
dfs(1, 0, 0, max_d, node_a);      // Prvi DFS nalazi node_a
max_d = -1;
dfs(node_a, 0, 0, max_d, node_b); // Drugi DFS nalazi node_b i promjer
cout << max_d << "\n";
```

---

<!-- _class: title -->
# Company Queries I & II (CSES)

## Binary lifting u akciji

---

# Analiza: Company Queries

**Problem I:** tko je $k$-ti šef (predak) zaposlenika $x$? (Ako ne postoji, ispisujemo $-1$.)
**Problem II:** tko je najniži zajednički šef (LCA) zaposlenika $a$ i $b$?

**Intuicija: binary lifting**
Ne možemo skakati po jednog pretka ($O(N)$ po upitu).
Pamtimo pretke na udaljenostima $1, 2, 4, 8, \dots$:
`up[u][i]` = predak čvora $u$ na udaljenosti $2^i$.

Ulaz direktno daje šefa svakog zaposlenika, pa je `up[u][0] = šef[u]`.

**Izgradnja ($O(N \log N)$):**
`up[u][i] = up[up[u][i-1]][i-1]`

---

# Implementacija: k-ti predak

Kako naći $k$-tog pretka u $O(\log N)$?
$k$ zapišemo binarno. Ako je $k = 13$ ($1101_2 = 8 + 4 + 1$), skačemo za 8, pa za 4, pa za 1.

```cpp
int get_kth_ancestor(int node, int k) {
    for (int i = 0; i < LOG; i++) {
        if ((k >> i) & 1) { // Ako je i-ti bit postavljen
            node = up[node][i];
        }
    }
    return node; // 0 ako takav predak ne postoji
}

// Company Queries I: ispis
int r = get_kth_ancestor(x, k);
cout << (r == 0 ? -1 : r) << "\n";
```

Za **Company Queries II** koristimo standardnu LCA funkciju opisanu ranije u prezentaciji.

---

<!-- _class: title -->
# Distance Queries (CSES)

## Primjena LCA

---

# Analiza: Distance Queries

**Problem:**
Zadano je stablo i $Q$ upita. Za svaki par čvorova $(u, v)$ treba ispisati njihovu udaljenost (broj bridova).

**Intuicija**
Put između $u$ i $v$ u stablu je jedinstven. Ide od $u$ gore do $LCA(u, v)$ i zatim dolje do $v$.
Udaljenost je zbroj udaljenosti od $u$ do LCA i od $v$ do LCA.

$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

---

# Implementacija: Distance Queries

```cpp
// Preprocessing: dubine i up[][] tablica (dfs_lca)

while (q--) {
    int u, v;
    cin >> u >> v;
    int lca = get_lca(u, v);
    cout << depth[u] + depth[v] - 2 * depth[lca] << "\n";
}
```

**Napomena:** ovo je standardni obrazac. Ako bridovi imaju težine, umjesto `depth` (broj bridova) koristimo `dist_from_root` (zbroj težina).

---

<!-- _class: title -->
# Subtree Queries (CSES)

## Linearizacija i BIT

---

# Analiza: Subtree Queries

**Problem:**

1. **Update:** vrijednost čvora $u$ postaje $x$.
2. **Query:** suma vrijednosti u cijelom podstablu čvora $u$.

**Intuicija**
Stabla su teška za rasponske upite, a nizovi su laki.
Koristimo **DFS ulazna (tin) i izlazna (tout)** vremena.
Podstablo čvora $u$ odgovara kontinuiranom rasponu $[tin[u], tout[u]]$ u nizu.

Problem svodimo na:

1. **Point update:** promjena vrijednosti na indeksu $tin[u]$.
2. **Range sum:** suma od $tin[u]$ do $tout[u]$.

Rješenje: **Fenwickovo stablo (BIT)**.

---

# Implementacija: Subtree Queries

```cpp
// 1. DFS za tin/tout
void dfs(int u, int p) {
    tin[u] = ++timer;
    // ... rekurzija ...
    tout[u] = timer;
}

// Na početku: bit_update(tin[u], val[u]) za svaki čvor u

// 2. Update (BIT radi s razlikama, pa pamtimo trenutnu vrijednost)
void update_node(int u, int new_val) {
    int diff = new_val - current_val[u];
    current_val[u] = new_val;
    bit_update(tin[u], diff); // Ažuriramo BIT na poziciji tin[u]
}

// 3. Query
long long query_subtree(int u) {
    return bit_query(tout[u]) - bit_query(tin[u] - 1);
}
```

---

<!-- _class: title -->
# Path Queries (CSES)

## Napredna linearizacija

---

# Analiza: Path Queries

**Problem:**

1. **Update:** vrijednost čvora $u$ postaje $x$.
2. **Query:** suma vrijednosti na putu od **korijena** do čvora $u$.

**Intuicija**
Ovo je obrnuto od Subtree Queries.
Kad promijenimo vrijednost čvora $u$, to utječe na sumu puta za $u$ i **sve njegove potomke**.
Dakle, update čvora $u$ zapravo je **range update** na rasponu podstabla $[tin[u], tout[u]]$.
Upit za čvor $u$ je **point query** na indeksu $tin[u]$.

Koristimo BIT za **range update, point query**.

---

# Implementacija: Path Queries

BIT inače podržava point update i range sum.
Za range update i point query koristimo trik s diferencijalnim nizom:

- Dodajemo $val$ na $[L, R]$ $\rightarrow$ `update(L, val)`, `update(R+1, -val)`.
- Vrijednost na $i$ je prefiksna suma do $i$ $\rightarrow$ `query(i)`.

```cpp
// BIT veličine n + 2, jer tout[u] + 1 može biti n + 1

// Update čvora u (dodajemo razliku na cijelo podstablo)
void update_val(int u, int diff) {
    bit_update(tin[u], diff);
    bit_update(tout[u] + 1, -diff);
}

// Query puta do u
long long query_path(int u) {
    return bit_query(tin[u]);
}
```

**Zaključak:** linearizacija stabla moćan je alat koji teške probleme na stablima pretvara u klasične probleme na nizovima.

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Stabla su specifična:**
   - Jedinstveni putovi, $N-1$ bridova, nema ciklusa.
   - Ti uvjeti omogućuju brze algoritme ($O(N)$ ili $O(\log N)$).

2. **Moćni alati:**
   - **Linearizacija (flattening):** pretvara podstabla u raspone na nizu. Ključna je za upite nad podstablima.
   - **Binary lifting (LCA):** omogućuje "skakanje" po stablu i brzo računanje udaljenosti.
   - **Promjer stabla:** dva DFS-a su standardni trik.

---

# Osvrt na tehnike rješavanja

- **Transformacija problema:**
  - Ako zadatak traži sumu/min/max u **podstablu** $\rightarrow$ linearizacija + BIT/segmentno stablo.
  - Ako zadatak traži nešto na **putu** $\rightarrow$ LCA + prefiksne sume (ili HLD za teže slučajeve).

- **Binary lifting je univerzalan:**
  - Ne služi samo za LCA. Koristi se kad god trebate simulirati "kamo ću stići nakon $K$ koraka" u grafu u kojem svaki čvor ima točno jedan izlazni brid.
  