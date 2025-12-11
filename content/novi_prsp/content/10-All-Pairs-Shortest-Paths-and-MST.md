---
nav_exclude: true
---

# Tjedan 10: Najkraći Putevi Svi-Svim i Minimalno Razapinjuće Stablo (MST)

## Sadržaj
1.  [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Proširenje Problema Najkraćeg Puta](#proširenje-problema-najkraćeg-puta)
    *   [Problem Minimalnog Razapinjućeg Stabla](#problem-minimalnog-razapinjućeg-stabla)
    *   [Preporučena Literatura](#preporučena-literatura)
2.  [Najkraći Putevi Svi-Svim: Floyd-Warshall Algoritam](#najkraći-putevi-svi-svim-floyd-warshall-algoritam)
    *   [Intuicija: Postupno Dodavanje Međukoraka](#intuicija-postupno-dodavanje-međukoraka)
    *   [Implementacija](#implementacija)
    *   [Analiza Složenosti i Primjene](#analiza-složenosti-i-primjene)
3.  [Minimalno Razapinjuće Stablo (MST)](#minimalno-razapinjuće-stablo-mst)
    *   [Problem 1: Kruskalov Algoritam](#problem-1-kruskalov-algoritam)
        *   [Pohlepna Strategija i Dokaz](#pohlepna-strategija-i-dokaz)
        *   [Union-Find Struktura](#union-find-struktura)
        *   [Implementacija Kruskalovog Algoritma](#implementacija-kruskalovog-algoritma)
    *   [Problem 2: Primov Algoritam](#problem-2-primov-algoritam)
        *   [Pohlepna Strategija i Usporedba s Dijkstrom](#pohlepna-strategija-i-usporedba-s-dijkstrom)
        *   [Implementacija Primovog Algoritma](#implementacija-primovog-algoritma)
4.  [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Proširenje Problema Najkraćeg Puta
Prošli tjedan bavili smo se problemom najkraćeg puta od jednog početnog čvora (*single-source*). Što ako nas zanimaju najkraći putevi između **svih parova** čvorova u grafu?
-   **Naivni pristup:** Pokreni Dijkstrin algoritam `n` puta, jednom za svaki čvor kao početni. Ako su sve težine ne-negativne, ovo daje ukupnu složenost `O(n * m log n)`.
-   **Naivni pristup (s negativnim težinama):** Pokreni Bellman-Ford `n` puta. Ukupna složenost je `O(n² * m)`.

Ovi pristupi mogu biti prespori. Danas ćemo naučiti **Floyd-Warshall** algoritam, koji rješava problem u `O(n³)` vremenu. Iako asimptotski nije uvijek bolji, izuzetno je jednostavan za implementaciju i efikasan za guste grafove.

### Problem Minimalnog Razapinjućeg Stabla
Zamislite da trebate povezati `n` gradova električnom mrežom. Znate cijenu postavljanja kabela između bilo koja dva grada. Cilj je povezati sve gradove (direktno ili indirektno) uz **minimalan ukupan trošak**.

Ovo je problem **minimalnog razapinjućeg stabla (MST)**. Zadan je neusmjeren, težinski graf. Razapinjuće stablo je podgraf koji povezuje sve čvorove originalnog grafa i ne sadrži cikluse. Minimalno razapinjuće stablo je ono čiji je zbroj težina bridova najmanji moguć.

Danas ćemo obraditi dva klasična pohlepna algoritma za MST:
1.  **Kruskalov algoritam:** Gradi stablo dodavanjem bridova s najmanjom težinom koji ne stvaraju ciklus.
2.  **Primov algoritam:** Gradi stablo počevši od jednog čvora i postupno dodajući najbliže susjedne čvorove.

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 13.3: *Floyd-Warshall algorithm*
    *   Poglavlje 15: *Spanning trees*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 25: *All-Pairs Shortest Paths*
    *   Poglavlje 23: *Minimum Spanning Trees*
    *   Poglavlje 21: *Data Structures for Disjoint Sets* (za Union-Find)

---

## Najkraći Putevi Svi-Svim: Floyd-Warshall Algoritam

### Intuicija: Postupno Dodavanje Međukoraka
Floyd-Warshall je algoritam temeljen na dinamičkom programiranju. Ideja je postupno poboljšavati procjene udaljenosti između svih parova čvorova `(i, j)`.

1.  **Stanje:** `dist[i][j]` = duljina najkraćeg puta od `i` do `j`.
2.  **Inicijalizacija:**
    *   `dist[i][i] = 0` za sve `i`.
    *   `dist[i][j] = w(i, j)` ako postoji brid od `i` do `j`.
    *   `dist[i][j] = ∞` ako nema direktnog brida.
3.  **Prijelaz (Iteracija):** Algoritam iterira kroz sve čvorove `k = 1...n` i razmatra ih kao moguće **međučvorove** na putu između `i` i `j`.
    Za svaki par `(i, j)`, provjerava je li put `i -> k -> j` kraći od trenutno poznatog puta `i -> j`.
    `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`

Nakon `n` iteracija, `dist[i][j]` će sadržavati duljinu najkraćeg puta jer smo isprobali sve moguće međučvorove.

### Implementacija
Floyd-Warshall se implementira s tri ugniježđene petlje.
```cpp
const int INF = 1e9;
int dist[N][N]; // Matrica udaljenosti

// Inicijalizacija matrice
for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
        if (i == j) dist[i][j] = 0;
        else if (adj[i][j]) dist[i][j] = adj[i][j]; // Ako postoji brid
        else dist[i][j] = INF;
    }
}

// Glavni dio algoritma
for (int k = 1; k <= n; ++k) {
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
        }
    }
}
```

### Analiza Složenosti i Primjene
-   **Složenost:** **O(n³)**. Zbog tri ugniježđene petlje, algoritam je pogodan samo za male grafove (obično `n <= 400`).
-   **Negativne težine:** Radi ispravno s negativnim težinama, ali ne i s negativnim ciklusima.
-   **Detekcija negativnih ciklusa:** Nakon izvršenja algoritma, ako je `dist[i][i] < 0` za bilo koji `i`, u grafu postoji negativni ciklus.
-   **Tranzitivno zatvaranje:** Modificirani algoritam može provjeriti postoji li put između bilo koja dva čvora.

---

## Minimalno Razapinjuće Stablo (MST)

### Problem 1: Kruskalov Algoritam

#### Pohlepna Strategija i Dokaz
Kruskalov algoritam slijedi jednostavnu i intuitivnu pohlepnu strategiju:
**"Na svakom koraku, dodaj najlakši brid koji ne stvara ciklus."**

**Algoritam:**
1.  Stvori šumu `F` gdje je svaki čvor u grafu zasebno stablo.
2.  Sortiraj sve bridove grafa po težini, od najmanje do najveće.
3.  Iteriraj kroz sortirane bridove `(u, v)`:
    *   Ako čvorovi `u` i `v` već pripadaju istom stablu u šumi `F`, dodavanje ovog brida stvorilo bi ciklus. Ignoriraj ga.
    *   Inače, dodaj brid `(u, v)` u `F`, spajajući dva stabla.
4.  Ponavljaj dok `F` ne postane jedno stablo (tj. dok se ne doda `n-1` bridova).

**Zašto ovo radi?** Dokaz se temelji na "cut" svojstvu. U bilo kojem koraku, ako uzmemo bilo koji podskup čvorova `S`, najlakši brid koji povezuje `S` s ostatkom grafa mora biti dio nekog MST-a. Kruskalov algoritam implicitno slijedi ovo pravilo.

#### Union-Find Struktura
Kako efikasno provjeriti jesu li dva čvora u istom stablu i kako spojiti dva stabla? Za to koristimo **Union-Find** (ili Disjoint Set Union - DSU) strukturu podataka.

-   **`find(i)`:** Vraća "predstavnika" (korijen) komponente kojoj pripada čvor `i`.
-   **`unite(i, j)`:** Spaja komponente kojima pripadaju `i` i `j`.

S optimizacijama (unija po veličini/rangu i kompresija putanje), ove operacije su gotovo konstantne u prosjeku (amortizirano vrijeme `O(α(n))`, gdje je `α` izuzetno sporo rastuća inverzna Ackermannova funkcija).

#### Implementacija Kruskalovog Algoritma
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>

struct Edge {
    int u, v, weight;
};

bool compareEdges(const Edge& a, const Edge& b) {
    return a.weight < b.weight;
}

vector<int> parent;
int find_set(int v) {
    if (v == parent[v]) return v;
    return parent[v] = find_set(parent[v]); // Path compression
}

void unite_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) parent[b] = a;
}

int main() {
    // ... Brzi I/O ...
    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for (int i = 0; i < m; ++i) {
        cin >> edges[i].u >> edges[i].v >> edges[i].weight;
    }

    sort(edges.begin(), edges.end(), compareEdges);

    parent.resize(n + 1);
    for (int i = 1; i <= n; ++i) parent[i] = i;

    long long total_weight = 0;
    for (Edge e : edges) {
        if (find_set(e.u) != find_set(e.v)) {
            total_weight += e.weight;
            unite_sets(e.u, e.v);
        }
    }

    cout << total_weight << '\n';
    return 0;
}
```
**Složenost:** **O(m log m)**, dominirana sortiranjem bridova.

### Problem 2: Primov Algoritam

#### Pohlepna Strategija i Usporedba s Dijkstrom
Primov algoritam također koristi pohlepnu strategiju, ali na drugačiji način:
**"Gradi stablo počevši od jednog čvora, na svakom koraku dodajući najlakši brid koji povezuje stablo s čvorom izvan stabla."**

**Algoritam:**
1.  Počni s proizvoljnim čvorom `s` i dodaj ga u stablo.
2.  Održavaj prioritetni red koji sadrži bridove koji povezuju čvorove u stablu s onima izvan.
3.  Dok stablo ne obuhvati sve čvorove:
    *   Izvadi najlakši brid `(u, v)` iz prioritetnog reda, gdje je `u` u stablu, a `v` nije.
    *   Dodaj `v` u stablo i brid `(u, v)` u MST.
    *   Dodaj sve bridove iz `v` prema čvorovima koji još nisu u stablu u prioritetni red.

**Usporedba s Dijkstrom:** Oba algoritma su strukturno vrlo slična. Obojica koriste prioritetni red za odabir sljedećeg čvora. Razlika je u ključu za prioritet:
-   **Dijkstra:** Ključ je ukupna udaljenost od izvora `s`.
-   **Prim:** Ključ je težina **samo jednog brida** koji povezuje čvor s trenutnim stablom.

#### Implementacija Primovog Algoritma
```cpp
// ... adj, n, m ...
vector<long long> dist(n + 1, INF);
vector<bool> visited(n + 1, false);
priority_queue<pair<long long, int>> q;

dist = 0;
q.push({0, 1});
long long total_weight = 0;

while (!q.empty()) {
    int u = q.top().second;
    long long d = -q.top().first;
    q.pop();

    if (visited[u]) continue;
    
    visited[u] = true;
    total_weight += d;

    for (auto edge : adj[u]) {
        int v = edge.first;
        int w = edge.second;
        if (!visited[v] && w < dist[v]) {
            dist[v] = w;
            q.push({-dist[v], v});
        }
    }
}
cout << total_weight << '\n';
```
**Složenost:** **O(m log n)**, identično Dijkstrinom algoritmu.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Road Reparation:** Klasičan MST problem. Može se riješiti Kruskalovim ili Primovim algoritmom.
*   **Road Construction:** Zahtijeva praćenje povezanih komponenata. Union-Find je idealan za ovo.
*   **Flight Routes Check:** Problem provjere jake povezanosti, ali se može riješiti i s dva prolaza DFS/BFS-a. Razmislite kako se MST koncepti mogu (ili ne mogu) primijeniti.

### Codeforces

*   **DZY Loves Bridges** (Problem 445B): Brojanje povezanih komponenata i primjena Kruskalovog principa za spajanje uz minimalan trošak.
*   **Edgy Trees** (Problem 1131C): Ne radi se direktno o MST-u, ali ideja spajanja komponenata i brojanja je slična.
*   **Minimum spanning tree for each edge?** (Problem 609E): Napredniji problem koji zahtijeva razumijevanje svojstava MST-a. Nakon što se nađe jedan MST, za svaki brid koji nije u njemu, treba pronaći najteži brid na ciklusu koji bi taj brid stvorio.

### Ostali Klasični Problemi
*   **Transitivno zatvaranje:** Nakon što ste naučili Floyd-Warshall, pokušajte riješiti problem "postoji li put između bilo koja dva čvora" koristeći sličnu logiku, ali s Booleovim vrijednostima.
*   **Problem s negativnim ciklusima:** Koristite Bellman-Ford ili Floyd-Warshall da detektirate negativni ciklus u grafu.

### Sljedeća lekcija: []()

[Sljedeća lekcija: ](){: .btn .btn-purple .float-right}