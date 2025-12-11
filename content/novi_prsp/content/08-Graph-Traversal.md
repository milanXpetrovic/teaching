---
nav_exclude: true
---

# Tjedan 8: Pretraživanje Grafova

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Modeliranje Problema Grafovima](#modeliranje-problema-grafovima)
    * [Strukture za Reprezentaciju Grafa](#strukture-za-reprezentaciju-grafa)
    * [DFS vs. BFS: Dvije Osnovne Strategije](#dfs-vs-bfs-dvije-osnovne-strategije)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Najkraći put u labirintu (BFS)](#problem-1-najkraći-put-u-labirintu-bfs)
    * [Problem 2: Brojanje povezanih komponenata (DFS)](#problem-2-brojanje-povezanih-komponenata-dfs)
    * [Problem 3: Detekcija ciklusa (DFS)](#problem-3-detekcija-ciklusa-dfs)
3. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Modeliranje Problema Grafovima

Grafovi su jedna od najmoćnijih apstraktnih struktura u računarstvu. Mnogi stvarni problemi mogu se modelirati kao grafovi, gdje su čvorovi objekti, a bridovi predstavljaju veze među njima. Primjeri uključuju:
* **Mreže cesta:** gradovi su čvorovi, ceste su bridovi.
* **Društvene mreže:** ljudi su čvorovi, prijateljstva su bridovi.
* **Ovisnosti:** zadaci su čvorovi, brid `A -> B` znači da se zadatak A mora izvršiti prije B.

Pretraživanje grafa je temeljni postupak koji nam omogućuje da otkrijemo strukturu grafa i odnose među čvorovima. Gotovo svaki složeniji algoritam na grafovima započinje nekom vrstom pretraživanja.

### Strukture za Reprezentaciju Grafa

Prije nego što možemo pretraživati graf, moramo ga spremiti u memoriju. Najčešći pristup u natjecateljskom programiranju je **lista susjedstva**.

**Lista Susjedstva (Adjacency List):** Za svaki čvor, pamtimo listu njegovih susjeda. U C++-u, ovo se najčešće implementira kao polje `vector`-a.

```cpp
const int N = 1e5 + 5; // Maksimalan broj čvorova
vector<int> adj[N];

// Dodavanje brida između čvorova a i b (za neusmjereni graf)
adj[a].push_back(b);
adj[b].push_back(a);```
Ova reprezentacija je efikasna za rijetke grafove (gdje je broj bridova `m` puno manji od `n²`), što je čest slučaj na natjecanjima.

### DFS vs. BFS: Dvije Osnovne Strategije

1.  **Pretraživanje u dubinu (Depth-First Search - DFS):**
    *   **Intuicija:** Istražuj jedan put što je dublje moguće prije nego što se vratiš natrag (backtrack). Zamislite da istražujete labirint tako da uvijek skrećete desno dok ne dođete do slijepe ulice, a onda se vraćate i probate druga skretanja.
    *   **Implementacija:** Prirodno se implementira rekurzijom (koristi implicitni stog poziva).
    *   **Primjene:** Detekcija ciklusa, topološko sortiranje, pronalaženje povezanih komponenata.

2.  **Pretraživanje u širinu (Breadth-First Search - BFS):**
    *   **Intuicija:** Prvo posjeti sve susjede, zatim susjede susjeda, i tako dalje, šireći se u slojevima. Zamislite valove koji se šire iz točke gdje je bačen kamen u vodu.
    *   **Implementacija:** Koristi red (queue) za praćenje čvorova koje treba posjetiti.
    *   **Primjene:** Pronalaženje **najkraćeg puta** u ne-težinskom grafu (grafu gdje su svi bridovi jednake duljine).

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 11: *Basics of graphs*
    *   Poglavlje 12: *Graph traversal*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 22: *Elementary Graph Algorithms*

---

## Primjeri Zadataka i Objašnjenja

### Problem 1: Najkraći put u labirintu (BFS)

**Zadatak:** Zadan je labirint u obliku 2D mreže. Neka polja su zidovi (`#`), a neka su slobodna (`.`). Zadane su početna (`A`) i završna (`B`) točka. Pronađi duljinu najkraćeg puta od `A` do `B`.

**Rješenje:** Ovo je klasičan problem za BFS. Graf modeliramo tako da je svako slobodno polje čvor, a bridovi postoje između susjednih slobodnih polja.

**Algoritam:**
1.  Inicijaliziraj 2D polje `distance` na beskonačno za sva polja.
2.  Kreiraj red i u njega stavi početnu poziciju `A`. Postavi `distance[A] = 0`.
3.  Dok red nije prazan:
    *   Izvadi trenutnu poziciju `(r, c)` iz reda.
    *   Ako je `(r, c)` završna pozicija `B`, algoritam je gotov.
    *   Za svakog susjeda `(nr, nc)` od `(r, c)`:
        *   Ako je susjed unutar mreže, nije zid i još nije posjećen (`distance` je beskonačno):
            *   Postavi `distance[nr][nc] = distance[r][c] + 1`.
            *   Dodaj `(nr, nc)` u red.

**Kod:**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <utility>

int main() {
    int n, m; // Dimenzije mreže
    cin >> n >> m;
    vector<string> grid(n);
    pair<int, int> start, end;
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
        for (int j = 0; j < m; ++j) {
            if (grid[i][j] == 'A') start = {i, j};
            if (grid[i][j] == 'B') end = {i, j};
        }
    }

    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int, int>> q;

    dist[start.first][start.second] = 0;
    q.push(start);

    int dr[] = {-1, 1, 0, 0}; // Mogući pomaci (gore, dolje, lijevo, desno)
    int dc[] = {0, 0, -1, 1};

    while (!q.empty()) {
        pair<int, int> curr = q.front();
        q.pop();

        if (curr == end) break;

        for (int i = 0; i < 4; ++i) {
            int nr = curr.first + dr[i];
            int nc = curr.second + dc[i];

            if (nr >= 0 && nr < n && nc >= 0 && nc < m && grid[nr][nc] != '#' && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[curr.first][curr.second] + 1;
                q.push({nr, nc});
            }
        }
    }

    if (dist[end.first][end.second] != -1) {
        cout << "YES\n" << dist[end.first][end.second] << '\n';
    } else {
        cout << "NO\n";
    }
    return 0;
}
```

**Složenost:** **O(n * m)**, jer svaki čvor (polje) posjećujemo i stavljamo u red točno jednom.

### Problem 2: Brojanje povezanih komponenata (DFS)

**Zadatak:** Zadan je neusmjeren graf (npr. `n` soba i `m` vrata koja ih povezuju). Koliko ima odvojenih skupina soba?

**Rješenje:** Ovo je problem brojanja povezanih komponenata.

**Algoritam:**

1. Inicijaliziraj polje `visited` za sve čvorove na `false`.
2. Inicijaliziraj brojač komponenata na 0.
3. Iteriraj kroz sve čvorove od 1 do `n`.
4. Ako čvor `i` još nije posjećen:
    * Povećaj brojač komponenata.
    * Pokreni DFS (ili BFS) iz čvora `i`. Traverza će posjetiti sve čvorove u istoj komponenti.

**Kod:**

```cpp
#include <iostream>
#include <vector>

const int MAXN = 1e5 + 5;
vector<int> adj[MAXN];
bool visited[MAXN];

void dfs(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

int main() {
    // ... Brzi I/O i učitavanje grafa ...
    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    
    int components = 0;
    for (int i = 1; i <= n; ++i) {
        if (!visited[i]) {
            dfs(i);
            components++;
        }
    }
    cout << components << '\n';
    return 0;
}
```

**Složenost:** **O(n + m)**, jer DFS posjećuje svaki čvor i svaki brid točno jednom.

### Problem 3: Detekcija ciklusa (DFS)

**Zadatak:** Zadan je neusmjereni graf. Odredi postoji li ciklus u grafu.

**Rješenje:** Ciklus postoji ako tijekom DFS pretraživanja naiđemo na već posjećeni čvor koji nije naš direktni roditelj u DFS stablu.

**Algoritam:**

1. Modificiraj DFS da prima dva argumenta: `dfs(u, parent)`.
2. Kada iz čvora `u` istražujemo susjeda `v`:
    * Ako je `v` **direktni roditelj** `p`, ignoriraj ga i nastavi.
    * Ako je `v` već posjećen (a nije `p`), pronašli smo **povratni brid** (back edge), što znači da postoji ciklus.
    * Ako `v` nije posjećen, rekurzivno pozovi `dfs(v, u)`.

**Kod:**

```cpp
// ... adj i visited polja ...
bool has_cycle = false;

void dfs_cycle(int u, int p) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (v == p) continue; // Ne vraćaj se odmah natrag
        if (visited[v]) {
            has_cycle = true; // Pronađen povratni brid -> ciklus
            return;
        } else {
            dfs_cycle(v, u);
        }
    }
}

// U main funkciji, za svaku komponentu
for (int i = 1; i <= n; ++i) {
    if (!visited[i]) {
        dfs_cycle(i, 0); // Početni roditelj je 0 (ili bilo koji nepostojeći čvor)
    }
}

if (has_cycle) cout << "IMA CIKLUS\n";
else cout << "NEMA CIKLUS\n";
```

**Složenost:** **O(n + m)**, jer je ovo samo modifikacija standardnog DFS-a.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* **Counting Rooms:** Točan problem brojanja povezanih komponenata.
* **Labyrinth:** Točan problem najkraćeg puta u mreži. Dodatno zahtijeva ispis puta, što se može postići pamćenjem roditelja svakog polja.
* **Building Teams:** Provjera je li graf bipartitan. Rješava se bojenjem grafa s dvije boje pomoću BFS-a ili DFS-a.
* **Message Route:** Klasičan problem najkraćeg puta u ne-težinskom grafu, idealan za BFS.

### Codeforces

* **Kefa and Park** (Problem 580C): Zanimljiv zadatak na stablu (specijalnom grafu) koji zahtijeva DFS ili BFS pretraživanje uz praćenje dodatnih informacija (broj uzastopnih mačaka na putu).
* **Party** (Problem 115A): Zadan je hijerarhijski odnos zaposlenika, što formira šumu (skup stabala). Potrebno je pronaći maksimalnu dubinu bilo kojeg stabla, što je klasična primjena DFS-a.
* **Ice Cave** (Problem 540C): Malo složeniji problem pretraživanja mreže. Zahtijeva provjeru uvjeta nakon što BFS/DFS završi, a ne samo tijekom pretrage.


### Sljedeća lekcija: []()

[Sljedeća lekcija: ](){: .btn .btn-purple .float-right}