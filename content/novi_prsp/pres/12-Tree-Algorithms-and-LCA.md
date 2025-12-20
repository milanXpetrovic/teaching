---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Algoritmi na stablima i LCA"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- paginate: false -->
<!-- _class: title  -->
# Algoritmi na stablima i LCA

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Osnovni pojmovi i svojstva**
   - Definicija stabla
   - Terminologija
2. **Obilazak stabla i DFS poredak**
   - Linearizacija (Entry/Exit times)
3. **Promjer stabla (Tree Diameter)**
   - Algoritam s dva DFS-a
4. **Najmanji zajednički predak (LCA)**
   - Binarno podizanje (Binary Lifting)
5. **Upiti nad putevima i podstablima**
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
1. Postoji točno jedan jednostavan put između bilo koja dva čvora.
2. Dodavanjem bilo kojeg brida stvara se ciklus.
3. Micanjem bilo kojeg brida stablo prestaje biti povezano.

**Terminologija:**
- **Korijen (Root):** Fiksirani čvor od kojeg "visi" stablo.
- **List (Leaf):** Čvor bez djece (u ukorijenjenom stablu) ili stupnja 1.
- **Dubina (Depth):** Udaljenost čvora od korijena.
- **Podstablo (Subtree):** Čvor i svi njegovi potomci.

---

<!-- _class: lead -->
# Obilazak stabla

## DFS poredak i linearizacija

---

# Linearizacija stabla (Tree Flattening)

Osim samog posjećivanja, korisno je pamtiti **ulazna (entry)** i **izlazna (exit)** vremena za svaki čvor.
Ovo nam omogućuje da preslikamo stablo na ravni niz.

```cpp
vector<int> adj[MAXN];
int tin[MAXN], tout[MAXN], timer;

void dfs(int u, int p) {
    tin[u] = ++timer; // Vrijeme ulaska
    
    for (int v : adj[u]) {
        if (v != p) dfs(v, u);
    }
    
    tout[u] = timer; // Vrijeme izlaska
}
```

**Svojstvo predaka:**
Čvor $u$ je predak čvora $v$ ako i samo ako:
$$ tin[u] \le tin[v] \quad \text{i} \quad tout[u] \ge tout[v] $$

---

<!-- _class: lead -->
# Promjer stabla

## Najduži put u stablu

---

# Kako pronaći promjer?

**Promjer stabla** je maksimalna udaljenost između bilo koja dva čvora.

### Algoritam s dva DFS-a ($O(N)$)

1. Odaberi proizvoljan čvor $A$ (npr. korijen).
2. Pronađi najudaljeniji čvor od $A$ koristeći DFS. Nazovimo ga $B$.
3. Pokreni DFS iz čvora $B$ i pronađi najudaljeniji čvor od njega. Nazovimo ga $C$.
4. Udaljenost između $B$ i $C$ je promjer stabla.

*(Alternativa: Dinamičko programiranje računajući `toLeaf` i `maxLength` za svaki čvor)*

---

<!-- _class: lead -->
# Najmanji zajednički predak (LCA)

## Lowest Common Ancestor

---

# Problem LCA

**Definicija:** LCA čvorova $u$ i $v$ je čvor koji je predak i od $u$ i od $v$, a nalazi se na najvećoj dubini (najdalje od korijena).

**Metoda: Binarno podizanje (Binary Lifting)**
Unaprijed izračunamo pretke na udaljenostima $2^0, 2^1, 2^2, \dots$.
Neka je `up[u][i]` predak čvora $u$ na udaljenosti $2^i$.

**Rekurzivna relacija:**
$$ up[u][i] = up[up[u][i-1]][i-1] $$
*(Predak na udaljenosti $2^i$ je predak na udaljenost $2^{i-1}$ od pretka na udaljenosti $2^{i-1}$)*.

**Složenost:**
- Preprocessing: $O(N \log N)$
- Upit: $O(\log N)$

---

# Implementacija: Preprocessing

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

---

# Implementacija: LCA Upit

```cpp
int get_lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    
    // 1. Izjednači dubine (podigni dubljeg v na razinu u)
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
    return up[u][0]; // Vrati roditelja
}
```

---

<!-- _class: lead -->
# Upiti nad putevima

## Distance i sume

---

# Udaljenost i sume na putu

Jednom kad imamo LCA, lako računamo udaljenosti. Put od $u$ do $v$ ide $u \to LCA \to v$.

### Udaljenost (broj bridova)
$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

### Suma vrijednosti čvorova na putu
Koristimo prefiksne sume od korijena do čvora (`P[u]`).
$$ PathSum(u, v) = P[u] + P[v] - 2 \cdot P[LCA(u, v)] + Value(LCA(u, v)) $$

*(Dodajemo `Value(LCA)` jer smo ga dvaput oduzeli, a on je dio puta).*

---

<!-- _class: lead -->
# Upiti nad podstablima

## Subtree Queries

---

# Linearizacija + Strukture podataka

Često imamo upite: "Promijeni vrijednost čvora $u$" i "Daj sumu podstabla $v$".

**Ključna ideja:**
Podstablo čvora $u$ odgovara kontinuiranom rasponu indeksa $[tin[u], tout[u]]$ u DFS obilasku.

**Rješenje:**
1. Mapiraj vrijednosti čvorova u niz na pozicije `tin[u]`.
2. Izgradi **Fenwickovo stablo (BIT)** ili **Segmentno stablo** nad tim nizom.
3. **Update:** Ažuriraj indeks `tin[u]` u BIT-u.
4. **Query:** Suma raspona $[tin[u], tout[u]]$ u BIT-u.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES Problem Set

---

# Zadaci

1. **[Tree Diameter](https://cses.fi/problemset/task/1131)**
   - Pronađi promjer stabla (2x DFS).
2. **[Company Queries I & II](https://cses.fi/problemset/task/1687)**
   - K-ti predak i LCA (Binary Lifting).
3. **[Distance Queries](https://cses.fi/problemset/task/1135)**
   - Udaljenost između čvorova pomoću LCA.
4. **[Subtree Queries](https://cses.fi/problemset/task/1137)**
   - Ažuriranje vrijednosti i suma podstabla (Linearizacija + BIT).
5. **[Path Queries](https://cses.fi/problemset/task/1138)**
   - Ažuriranje i suma na putu (malo teže, ali sličan princip).

---

<!-- _class: title -->
# Tree Diameter (CSES)

## Najduži put u stablu

---

# Analiza: Tree Diameter

**Problem:**
Zadano je stablo od $N$ čvorova. Pronađi promjer stabla (maksimalnu udaljenost između dva čvora).
**Ograničenja:** $N \le 2 \cdot 10^5$.

### Intuicija (2x DFS)
Naivni pristup (BFS iz svakog čvora) je $O(N^2)$ - presporo.
Postoji elegantan algoritam u $O(N)$:
1. Odaberi proizvoljan čvor $x$ (npr. 1).
2. Pronađi najudaljeniji čvor od $x$. Nazovimo ga $a$.
3. Pronađi najudaljeniji čvor od $a$. Nazovimo ga $b$.
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
dfs(1, 0, 0, max_d, node_a); // Prvi DFS nalazi node_a
max_d = -1;
dfs(node_a, 0, 0, max_d, node_b); // Drugi DFS nalazi node_b i promjer
cout << max_d << endl;
```

---

<!-- _class: title -->
# Company Queries I & II (CSES)

## Binary Lifting u akciji

---

# Analiza: Company Queries

**Problem I:** Tko je $k$-ti šef (predak) zaposlenika $x$?
**Problem II:** Tko je najniži zajednički šef (LCA) zaposlenika $a$ i $b$?

### Intuicija: Binary Lifting
Ne možemo skakati jednog po jednog pretka ($O(N)$ po upitu).
Pamtimo pretke na udaljenostima $1, 2, 4, 8, \dots$.
`up[u][i]` = predak čvora $u$ na udaljenosti $2^i$.

**Izgradnja ($O(N \log N)$):**
`up[u][i] = up[up[u][i-1]][i-1]`

---

# Implementacija: K-ti predak

Kako naći $k$-tog pretka u $O(\log N)$?
Zapišemo $k$ binarno. Ako je $k = 13$ ($1101_2 = 8 + 4 + 1$), skačemo za 8, pa za 4, pa za 1.

```cpp
int get_kth_ancestor(int node, int k) {
    for (int i = 0; i < LOG; i++) {
        if ((k >> i) & 1) { // Ako je i-ti bit postavljen
            node = up[node][i];
        }
    }
    return node; // Može biti 0 ako ne postoji
}
```

Za **Company Queries II** koristimo standardnu LCA funkciju opisanu ranije u prezentaciji.

---

<!-- _class: title -->
# Distance Queries (CSES)

## Primjena LCA

---

# Analiza: Distance Queries

**Problem:**
Zadano je stablo i $Q$ upita. Za svaki par čvorova $(u, v)$ ispiši njihovu udaljenost (broj bridova).

### Intuicija
Put između $u$ i $v$ u stablu je jedinstven. On ide od $u$ gore do $LCA(u, v)$ i zatim dolje do $v$.
Udaljenost je zbroj udaljenosti od $u$ do LCA i od $v$ do LCA.

$$ dist(u, v) = depth[u] + depth[v] - 2 \cdot depth[LCA(u, v)] $$

---

# Implementacija: Distance Queries

```cpp
// Preprocessing: Izračunaj dubine i up[][] tablicu (DFS)

while (q--) {
    int u, v;
    cin >> u >> v;
    int lca = get_lca(u, v);
    cout << depth[u] + depth[v] - 2 * depth[lca] << "\n";
}
```

**Napomena:** Ovo je standardni obrazac. Ako bridovi imaju težine, umjesto `depth` (broj bridova) koristimo `dist_from_root` (zbroj težina).

---

<!-- _class: title -->
# Subtree Queries (CSES)

## Linearizacija i BIT

---

# Analiza: Subtree Queries

**Problem:**
1. **Update:** Promijeni vrijednost čvora $u$.
2. **Query:** Izračunaj sumu vrijednosti u cijelom podstablu čvora $u$.

### Intuicija
Stabla su teška za rasponske upite. Nizovi su laki.
Koristimo **DFS ulazna (tin) i izlazna (tout)** vremena.
Podstablo čvora $u$ odgovara kontinuiranom rasponu $[tin[u], tout[u]]$ u nizu.

Problem svodimo na:
1. **Point Update:** Promijeni vrijednost na indeksu $tin[u]$.
2. **Range Sum:** Suma od $tin[u]$ do $tout[u]$.
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

// 2. Update (pazi: BIT radi s razlikama ili postavi novu vrijednost)
void update_node(int u, int new_val) {
    int diff = new_val - current_val[u];
    current_val[u] = new_val;
    bit_update(tin[u], diff); // Ažuriraj BIT na poziciji tin[u]
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
1. **Update:** Promijeni vrijednost čvora $u$.
2. **Query:** Suma vrijednosti na putu od **korijena** do čvora $u$.

### Intuicija
Ovo je obrnuto od Subtree Queries.
Kad promijenimo vrijednost čvora $u$, to utječe na sumu puta za $u$ i **sve njegove potomke**.
Dakle, update čvora $u$ je zapravo **Range Update** na rasponu podstabla $[tin[u], tout[u]]$.
Upit za čvor $u$ je **Point Query** na indeksu $tin[u]$.

Koristimo BIT za **Range Update, Point Query**.

---

# Implementacija: Path Queries

BIT inače podržava Point Update, Range Sum.
Za Range Update, Point Query koristimo trik s diferencijalnim nizom:
- Dodaj $val$ na $[L, R] \rightarrow$ `update(L, val)`, `update(R+1, -val)`.
- Vrijednost na $i$ je prefiksna suma do $i$ $\rightarrow$ `query(i)`.

```cpp
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

**Zaključak:** Linearizacija stabla je moćan alat koji teške probleme na stablima pretvara u klasične probleme na nizovima.

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Stabla su specifična:**
   - Jedinstveni putevi, $N-1$ bridova, nema ciklusa.
   - Ovi uvjeti omogućuju brze algoritme ($O(N)$ ili $O(\log N)$).

2. **Moćni alati:**
   - **Linearizacija (Flattening):** Pretvara podstabla u raspone na nizu. Ključno za rješavanje upita nad podstablima.
   - **Binary Lifting (LCA):** Omogućuje "skakanje" po stablu i brzo računanje udaljenosti.
   - **Promjer stabla:** Dva DFS-a su standardni trik.

---

# Osvrt na tehnike rješavanja

- **Transformacija problema:**
  - Ako zadatak traži sumu/min/max u **podstablu** $\rightarrow$ Linearizacija + BIT/Segmentno stablo.
  - Ako zadatak traži nešto na **putu** $\rightarrow$ LCA + Prefiksne sume (ili HLD za teže slučajeve).

- **Binary Lifting je univerzalan:**
  - Ne služi samo za LCA. Koristi se kad god trebaš simulirati kretanje "kamo ću stići nakon $K$ koraka" u grafu gdje svaki čvor ima točno jedan izlazni brid.

---
