---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pretraživanje grafova"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!--
Prijedlozi za slike (dodati ručno u prezentaciju):
1. Slajd "Dvije osnovne strategije": slika koja uspoređuje BFS (koncentrični slojevi) i DFS (put koji ide do kraja pa se vraća).
2. Slajd "Problem 1: Najkraći put u labirintu": 2D mreža sa crnim zidovima i obojenim putem.
3. Slajd "Problem 2: Povezane komponente": graf s 3 odvojena "otoka" čvorova.
-->

<!-- _paginate: false -->
<!-- _class: title -->

# Pretraživanje grafova

## DFS, BFS i primjene

---

# Sadržaj

1. **Uvod i reprezentacija grafa**
   * Modeliranje i lista susjedstva
2. **Osnovne strategije**
   * DFS (Depth-First Search)
   * BFS (Breadth-First Search)
3. **Primjeri i algoritmi**
   * Najkraći put u labirintu (BFS)
   * Povezane komponente (DFS)
   * Detekcija ciklusa (DFS)
4. **Zadaci za vježbu**

---

# Uvod: modeliranje problema

Grafovi su moćna apstrakcija. Čvorovi su objekti, bridovi su veze.

**Primjeri iz stvarnog svijeta:**

* **Mreže cesta:** gradovi (čvorovi) i ceste (bridovi).
* **Društvene mreže:** ljudi (čvorovi) i prijateljstva (bridovi).
* **Ovisnosti:** zadaci (čvorovi) i redoslijed izvršavanja (usmjereni bridovi).

> Pretraživanje grafa je temelj za otkrivanje strukture i odnosa.

---

# Reprezentacija: lista susjedstva

Za natjecateljsko programiranje **lista susjedstva** (adjacency list) je standard.
Efikasna je za **rijetke grafove** ($M \ll N^2$).

```cpp
const int MAXN = 1e5 + 5;
vector<int> adj[MAXN]; // Polje vektora

int main() {
    int n, m; cin >> n >> m;

    // Učitavanje m bridova neusmjerenog grafa
    for (int i = 0; i < m; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); // v je susjed od u
        adj[v].push_back(u); // u je susjed od v
    }
}
```

---

# Dvije osnovne strategije

**1. DFS (Depth-First Search): dubina**

* **Intuicija:** istražujemo jedan put do kraja ("udarimo u zid"), pa se vraćamo (backtrack).
* **Implementacija:** rekurzija (stog).
* **Primjene:** povezane komponente, detekcija ciklusa, topološko sortiranje.

**2. BFS (Breadth-First Search): širina**

* **Intuicija:** širimo se u slojevima (valovi u vodi). Prvo posjetimo sve susjede, pa susjede susjeda.
* **Implementacija:** red (queue).
* **Primjene:** **najkraći put** u grafu bez težina.

---

# Problem 1: Najkraći put u labirintu (BFS)

**Zadatak:**
Zadan je labirint (2D mreža, `#` zidovi, `.` prolaz). Treba naći duljinu najkraćeg puta od `A` do `B`.

**Zašto BFS?**
Graf je bez težina (svaki korak košta 1). BFS jamči pronalazak najkraćeg puta jer se širi koncentrično.

**Algoritam:**

1. Stavimo početak `A` u red (`queue`), uz `dist[A] = 0`.
2. Dok red nije prazan:
   * Uzmemo polje `(r, c)`.
   * Za svakog susjeda (gore, dolje, lijevo, desno):
     * Ako je slobodan i neposjećen: `dist[novi] = dist[stari] + 1` i dodamo ga u red.

---

# BFS implementacija (ključni dio)

```cpp
// dist[n][m] inicijaliziran na -1; start (sr, sc), cilj (er, ec)
queue<pair<int, int>> q;
q.push({sr, sc});
dist[sr][sc] = 0;

int dr[] = {-1, 1, 0, 0}; // Smjerovi redaka
int dc[] = {0, 0, -1, 1}; // Smjerovi stupaca

while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    if (r == er && c == ec) break; // Nađen cilj

    for (int i = 0; i < 4; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];

        // isValid provjerava granice mreže
        if (isValid(nr, nc) && grid[nr][nc] != '#' && dist[nr][nc] == -1) {
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
}
```

**Složenost:** $O(N \cdot M)$. (Ne zovite varijablu `end`: sudara se sa `std::end`.)

---

# Problem 2: Povezane komponente (DFS)

**Zadatak:**
Koliko ima povezanih komponenata u grafu?

**Algoritam:**

1. Postavimo sve `visited` na false i `brojac = 0`.
2. Za svaki `i` od 1 do $N$:
   * Ako `i` nije posjećen:
     * `brojac++`
     * Pokrenemo `dfs(i)` $\to$ to će označiti cijelu komponentu kao posjećenu.

---

# DFS implementacija

```cpp
vector<int> adj[MAXN];
bool visited[MAXN];

void dfs(int u) {
    visited[u] = true;
    // Rekurzivno posjećujemo sve susjede
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

// U main funkciji:
int components = 0;
for (int i = 1; i <= n; ++i) {
    if (!visited[i]) {
        dfs(i);
        components++;
    }
}
```

**Složenost:** $O(V + E)$ (svaki čvor i brid jednom).

---

# Problem 3: Detekcija ciklusa (DFS)

**Zadatak:**
Sadrži li neusmjereni graf ciklus?

**Ideja:**
Ako tijekom DFS-a naiđemo na susjeda `v` koji je **već posjećen**, a **nije** naš direktni roditelj `p` (iz kojeg smo došli), pronašli smo **povratni brid** (back-edge).

To znači da postoji drugi put do `v`, što zatvara ciklus.

---

# Detekcija ciklusa: kod

Modificiramo DFS da prati roditelja `p`.

```cpp
bool has_cycle = false;

void dfs_cycle(int u, int p) {
    visited[u] = true;

    for (int v : adj[u]) {
        if (v == p) continue; // Ignoriramo brid kojim smo došli

        if (visited[v]) {
            has_cycle = true; // Već viđen susjed -> CIKLUS!
            return;
        } else {
            dfs_cycle(v, u);
        }
    }
}
```

Kao i kod komponenata, `dfs_cycle` pokrećemo iz svakog neposjećenog čvora.

---

# Zadaci za vježbu (CSES)

1. **[Counting Rooms](https://cses.fi/problemset/task/1192)**
   * Primjena DFS/BFS na 2D mreži za brojanje komponenata.
2. **[Labyrinth](https://cses.fi/problemset/task/1193)**
   * BFS za najkraći put + rekonstrukcija puta (pamtimo `parent` polje).
3. **[Building Teams](https://cses.fi/problemset/task/1668)**
   * Provjera je li graf bipartitan (2-bojanje grafa).
4. **[Message Route](https://cses.fi/problemset/task/1667)**
   * Klasičan BFS na grafu (ne na mreži).
5. **[Round Trip](https://cses.fi/problemset/task/1669)**
   * Detekcija ciklusa iz Problema 3, uz ispis samog ciklusa.

---

<!-- _class: title -->
# 1. Counting Rooms (CSES)

## Brojanje povezanih komponenata na mreži

---

# Analiza: Counting Rooms

**Problem:**
Zadan je tlocrt zgrade veličine $N \times M$. Neka polja su zidovi (`#`), a neka pod (`.`).
Želimo prebrojati koliko ima "soba". Soba je skup podnih polja povezanih horizontalno ili vertikalno.

**Intuicija:**
Ovo je klasičan problem **brojanja povezanih komponenata**, ali na implicitnom grafu (mreži).
Svako polje `.` je čvor, a susjedna polja `.` povezana su bridom.

**Algoritam:**
Prolazimo kroz svako polje $(i, j)$ u mreži:

1. Ako je polje zid (`#`) ili već posjećeno $\to$ preskačemo ga.
2. Ako je polje pod (`.`) i nije posjećeno $\to$ pronašli smo novu sobu!
   - Povećamo brojač soba.
   - Pokrenemo DFS/BFS od tog polja da označimo cijelu sobu kao posjećenu.

---

# Implementacija: Counting Rooms

```cpp
int n, m;
vector<string> grid;
vector<vector<bool>> visited;
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

void dfs(int x, int y) {
    visited[x][y] = true;
    for (int i = 0; i < 4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        if (nx >= 0 && nx < n && ny >= 0 && ny < m &&
            grid[nx][ny] == '.' && !visited[nx][ny]) {
            dfs(nx, ny);
        }
    }
}

// U main-u:
int rooms = 0;
for (int i = 0; i < n; ++i)
    for (int j = 0; j < m; ++j)
        if (grid[i][j] == '.' && !visited[i][j]) { rooms++; dfs(i, j); }
```

**Oprez:** rekurzija na mreži $1000 \times 1000$ može ići u dubinu do $10^6$. Lokalno (posebno na Windowsima) to može srušiti program zbog malog stacka, pa je BFS sigurniji izbor.

---

<!-- _class: title -->
# 2. Labyrinth (CSES)

## Najkraći put i rekonstrukcija

---

# Analiza: Labyrinth

**Problem:**
Treba naći najkraći put od `A` do `B` u labirintu. Ako postoji, ispisujemo `YES`, duljinu i sam put (niz znakova `L`, `R`, `U`, `D`).

**Intuicija:**
Najkraći put u grafu bez težina $\to$ **BFS**.
Da bismo ispisali put, nije dovoljno pamtiti samo udaljenost. Moramo pamtiti **odakle smo došli**.

**Struktura za rekonstrukciju:**
Koristimo 2D polje `parent[N][M]` koje za svako polje pamti smjer kojim smo došli do njega.
Kada BFS dođe do `B`, krećemo od `B` i pratimo `parent` unatrag sve do `A`.

---

# Implementacija: Labyrinth (BFS)

```cpp
// Smjerovi: 0 = U, 1 = D, 2 = L, 3 = R
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

queue<pair<int, int>> q;
q.push({sr, sc});
visited[sr][sc] = true;

while (!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    if (x == er && y == ec) break; // Našli smo B

    for (int i = 0; i < 4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        // isValid provjerava granice i zid
        if (isValid(nx, ny) && !visited[nx][ny]) {
            visited[nx][ny] = true;
            parent[nx][ny] = i; // Pamtimo indeks smjera
            q.push({nx, ny});
        }
    }
}
```

---

# Labyrinth: rekonstrukcija puta

Ako je `visited[er][ec]` true, idemo od `B` unatrag prema `A`:

```cpp
string path;
int x = er, y = ec;
while (x != sr || y != sc) {
    int d = parent[x][y];
    path += "UDLR"[d];   // Slovo za smjer kojim smo došli
    x -= dx[d];          // Pomak u suprotnom smjeru
    y -= dy[d];
}
reverse(path.begin(), path.end()); // Išli smo od kraja prema početku

cout << "YES\n" << path.size() << "\n" << path << "\n";
```

Ako `B` nije posjećen, ispisujemo `NO`.

---

<!-- _class: title -->
# 3. Building Teams (CSES)

## Bipartitnost grafa (2-bojanje)

---

# Analiza: Building Teams

**Problem:**
Treba podijeliti učenike u dva tima tako da nijedan par prijatelja nije u istom timu.

**Intuicija:**
Ovo je problem provjere je li graf **bipartitan**.
Graf je bipartitan ako se njegovi čvorovi mogu obojiti s 2 boje tako da svaki brid spaja čvorove različitih boja.

**Algoritam (BFS ili DFS):**

1. Prvi neobojani čvor obojimo bojom 1.
2. Sve njegove susjede obojimo bojom 2.
3. Sve susjede susjeda obojimo bojom 1...
4. Ako naiđemo na susjeda koji je već obojan **istom** bojom kao trenutni čvor $\to$ **IMPOSSIBLE** (postoji neparan ciklus).

---

# Implementacija: Building Teams

```cpp
vector<int> color(n + 1, 0); // 0: neobojano, 1: tim 1, 2: tim 2
bool possible = true;

for (int i = 1; i <= n; ++i) {
    if (color[i] == 0) { // Nova komponenta
        queue<int> q;
        q.push(i);
        color[i] = 1;

        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == 0) {
                    color[v] = (color[u] == 1) ? 2 : 1; // Suprotna boja
                    q.push(v);
                } else if (color[v] == color[u]) {
                    possible = false; // Konflikt!
                }
            }
        }
    }
}
if (!possible) cout << "IMPOSSIBLE\n";
else { for (int i = 1; i <= n; ++i) cout << color[i] << " "; cout << "\n"; }
```

---

<!-- _class: title -->
# 4. Message Route (CSES)

## Najkraći put u općem grafu

---

# Analiza: Message Route

**Problem:**
Mreža računala. Treba naći najkraći put (minimalan broj konekcija) od računala 1 do računala $N$.

**Sličnost s Labyrinthom:**
Isti princip (BFS za najkraći put + rekonstrukcija), ali struktura je **graf** (lista susjedstva), a ne 2D mreža.

**Struktura:**

- `adj[N]`: lista susjedstva.
- `dist[N]`: udaljenost od izvora (inicijalno $-1$, tj. neposjećen).
- `parent[N]`: prethodni čvor na putu (za rekonstrukciju).

---

# Implementacija: Message Route

```cpp
vector<int> dist(n + 1, -1), parent(n + 1, 0);
queue<int> q;
q.push(1);
dist[1] = 0;

while (!q.empty()) {
    int u = q.front(); q.pop();
    if (u == n) break; // Stigli smo do cilja

    for (int v : adj[u]) {
        if (dist[v] == -1) { // Ako nije posjećen
            dist[v] = dist[u] + 1;
            parent[v] = u;   // Pamtimo odakle smo došli
            q.push(v);
        }
    }
}

if (dist[n] == -1) { cout << "IMPOSSIBLE\n"; return 0; }

// Rekonstrukcija od n do 1 (parent[1] = 0 označava početak)
vector<int> path;
for (int curr = n; curr != 0; curr = parent[curr]) path.push_back(curr);
reverse(path.begin(), path.end());

cout << path.size() << "\n";
for (int x : path) cout << x << " ";
cout << "\n";
```

---

# Zadaci za vježbu (Codeforces)

Preporuka: filtrirajte zadatke s tagom `graphs` i težinom `800-1200`.

[Codeforces Graph Problems](https://codeforces.com/problemset?order=BY_RATING_ASC&tags=graphs)