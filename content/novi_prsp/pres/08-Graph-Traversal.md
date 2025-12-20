---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pretraživanje grafova"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

### Prijedlozi za slike (dodati ručno u prezentaciju):

1. **Slajd "Dvije osnovne strategije":**
    * Dodati sliku koja uspoređuje BFS (koncentrični krugovi/slojevi) i DFS (dugačka vijugava zmija koja ide do kraja pa se vraća).
2. **Slajd "Problem 1: Labirint":**
    * Slika 2D mreže (grid) gdje su zidovi crni, a putanja označena bojom.
3. **Slajd "Problem 2: Povezane komponente":**
    * Slika grafa s 3 odvojena "otoka" (klastera) čvorova kako bi pojam komponente bio jasan.

---
<!-- _class: title -->

# Pretraživanje grafova

## DFS, BFS i primjene

---

# Sadržaj

1. **Uvod i reprezentacija grafa**
   * Modeliranje i Lista susjedstva
2. **Osnovne strategije**
   * DFS (Depth-First Search)
   * BFS (Breadth-First Search)
3. **Primjeri i Algoritmi**
   * Najkraći put u labirintu (BFS)
   * Povezane komponente (DFS)
   * Detekcija ciklusa (DFS)
4. **Zadaci za vježbu**

---

# Uvod: Modeliranje problema

Grafovi su moćna apstrakcija. Čvorovi su objekti, bridovi su veze.

**Primjeri iz stvarnog svijeta:**
* **Mreže cesta:** Gradovi (čvorovi) i ceste (bridovi).
* **Društvene mreže:** Ljudi (čvorovi) i prijateljstva (bridovi).
* **Ovisnosti:** Zadaci (čvorovi) i redoslijed izvršavanja (usmjereni bridovi).

> Pretraživanje grafa je temelj za otkrivanje strukture i odnosa.

---

# Reprezentacija: Lista Susjedstva

Za natjecateljsko programiranje, **Lista Susjedstva** (Adjacency List) je standard.
Efikasna je za **rijetke grafove** ($M \ll N^2$).

```cpp
const int N = 1e5 + 5;
vector<int> adj[N]; // Polje vektora

int main() {
    int u, v;
    // Učitavanje brida za neusmjereni graf
    cin >> u >> v;
    
    adj[u].push_back(v); // Dodaj v u listu susjeda od u
    adj[v].push_back(u); // Dodaj u u listu susjeda od v
}
```

---

# Dvije osnovne strategije

### 1. DFS (Depth-First Search) - Dubina
* **Intuicija:** Istražuj jedan put do kraja ("udari u zid"), pa se vrati (backtrack).
* **Implementacija:** Rekurzija (stog).
* **Primjene:** Povezane komponente, detekcija ciklusa, topološko sortiranje.

### 2. BFS (Breadth-First Search) - Širina
* **Intuicija:** Širi se u slojevima (valovi u vodi). Prvo posjeti sve susjede, pa susjede susjeda.
* **Implementacija:** Red (Queue).
* **Primjene:** **Najkraći put** u ne-težinskom grafu.

---

# Problem 1: Najkraći put u labirintu (BFS)

**Zadatak:**
Zadan je labirint (2D mreža, `#` zidovi, `.` prolaz). Nađi duljinu najkraćeg puta od `A` do `B`.

**Zašto BFS?**
Graf je ne-težinski (svaki korak košta 1). BFS garantira pronalazak najkraćeg puta jer se širi koncentrično.

**Algoritam:**
1. Stavi početak `A` u red (`queue`). `dist[A] = 0`.
2. Dok red nije prazan:
   * Uzmi polje `(r, c)`.
   * Za svakog susjeda (gore, dolje, lijevo, desno):
     * Ako je slobodan i neposjećen: `dist[novi] = dist[stari] + 1`, dodaj u red.

---

# BFS Implementacija (Ključni dio)

```cpp
// dist[n][m] inicijaliziran na -1
queue<pair<int, int>> q;
q.push(start); dist[start.x][start.y] = 0;

int dr[] = {-1, 1, 0, 0}; // Smjerovi redaka
int dc[] = {0, 0, -1, 1}; // Smjerovi stupaca

while (!q.empty()) {
    auto [r, c] = q.front(); q.pop();
    if (r == end.x && c == end.y) break; // Nađen cilj

    for (int i = 0; i < 4; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        
        // Provjera granica, zidova i posjećenosti
        if (isValid(nr, nc) && grid[nr][nc] != '#' && dist[nr][nc] == -1) {
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
}
```
**Složenost:** $O(N \cdot M)$

---

# Problem 2: Povezane komponente (DFS)

**Zadatak:**
Koliko ima odvojenih grupa soba (komponenata) u grafu?

**Algoritam:**
1. Postavi `visited` na false. `brojac = 0`.
2. Iteriraj `i` od 1 do $N$:
   * Ako `i` nije posjećen:
     * `brojac++`
     * Pokreni `dfs(i)` $\to$ ovo će označiti cijelu komponentu kao posjećenu.

---

# DFS Implementacija

```cpp
vector<int> adj[MAXN];
bool visited[MAXN];

void dfs(int u) {
    visited[u] = true;
    // Posjeti sve susjede rekurzivno
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

# Detekcija ciklusa: Kod

Modificiramo DFS da prati roditelja `p`.

```cpp
bool has_cycle = false;

void dfs_cycle(int u, int p) {
    visited[u] = true;
    
    for (int v : adj[u]) {
        if (v == p) continue; // Ignoriraj brid kojim smo došli
        
        if (visited[v]) {
            has_cycle = true; // Već viđen susjed -> CIKLUS!
            return;
        } else {
            dfs_cycle(v, u);
        }
    }
}
```

---

# Zadaci za vježbu (CSES)

1. **[Counting Rooms](https://cses.fi/problemset/task/1192)**
   * Primjena DFS/BFS na 2D mreži za brojanje komponenata.
2. **[Labyrinth](https://cses.fi/problemset/task/1193)**
   * BFS za najkraći put + rekonstrukcija puta (pamti `parent` polje).
3. **[Building Teams](https://cses.fi/problemset/task/1668)**
   * Provjera je li graf bipartitan (2-bojanje grafa).
4. **[Message Route](https://cses.fi/problemset/task/1667)**
   * Klasičan BFS na grafu (ne na mreži).

---

<!-- _class: title -->
# 1. Counting Rooms (CSES)

## Brojanje povezanih komponenata na mreži

---

# Analiza: Counting Rooms

**Problem:**
Zadana je tlocrt zgrade veličine $N \times M$. Neka polja su zidovi (`#`), a neka pod (`.`).
Želimo prebrojati koliko ima "soba". Soba je skup podnih polja povezanih horizontalno ili vertikalno.

**Intuicija:**
Ovo je klasičan problem **brojanja povezanih komponenata** (Connected Components), ali na implicitnom grafu (mreži).
Svako polje `.` je čvor, a susjedna polja `.` su povezana bridom.

**Algoritam:**
Prolazimo kroz svako polje $(i, j)$ u mreži:
1. Ako je polje zid (`#`) ili već posjećeno $\to$ preskoči.
2. Ako je polje pod (`.`) i nije posjećeno $\to$ pronašli smo novu sobu!
   - Povećaj brojač soba.
   - Pokreni DFS/BFS od tog polja da označiš cijelu sobu kao posjećenu.

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
    for(int i=0; i<4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        if(nx >= 0 && nx < n && ny >= 0 && ny < m && 
           grid[nx][ny] == '.' && !visited[nx][ny]) {
            dfs(nx, ny);
        }
    }
}

// U main-u:
int rooms = 0;
for(int i=0; i<n; ++i) {
    for(int j=0; j<m; ++j) {
        if(grid[i][j] == '.' && !visited[i][j]) {
            rooms++;
            dfs(i, j);
        }
    }
}
```

---

<!-- _class: title -->
# 2. Labyrinth (CSES)

## Najkraći put i rekonstrukcija

---

# Analiza: Labyrinth

**Problem:**
Naći najkraći put od `A` do `B` u labirintu. Ako postoji, ispisati duljinu i sam put (niz znakova 'L', 'R', 'U', 'D').

**Intuicija:**
Najkraći put u ne-težinskom grafu $\to$ **BFS**.
Da bismo ispisali put, nije dovoljno pamtiti samo udaljenost. Moramo pamtiti **odakle smo došli**.

**Struktura za rekonstrukciju:**
Koristimo 2D polje `parent[N][M]` koje za svako polje pamti smjer ('L', 'R', 'U', 'D') kojim smo došli do njega.
Kada BFS dođe do `B`, krećemo od `B` i pratimo `parent` pokazivače unatrag sve do `A`.

---

# Implementacija: Labyrinth (BFS)

```cpp
queue<pair<int, int>> q;
q.push(start); 
visited[start.x][start.y] = true;

while(!q.empty()) {
    auto [x, y] = q.front(); q.pop();
    if (x == end.x && y == end.y) break; // Našli smo B

    for(int i=0; i<4; ++i) {
        int nx = x + dx[i], ny = y + dy[i];
        if(isValid(nx, ny) && !visited[nx][ny]) {
            visited[nx][ny] = true;
            parent[nx][ny] = i; // Pamtimo indeks smjera (0=U, 1=D...)
            q.push({nx, ny});
        }
    }
}
```

**Rekonstrukcija:**
Ako je `visited[end.x][end.y]` true:
1. Kreni od `end`.
2. Uzmi smjer iz `parent`. Dodaj odgovarajuće slovo u string.
3. Pomakni se u suprotnom smjeru. Ponavljaj dok ne dođeš do `start`.
4. Okreni string (jer smo išli od kraja prema početku).

---

<!-- _class: title -->
# 3. Building Teams (CSES)

## Bipartitnost grafa (2-bojanje)

---

# Analiza: Building Teams

**Problem:**
Podijeli učenike u dva tima tako da niti jedan par prijatelja nije u istom timu.

**Intuicija:**
Ovo je problem provjere je li graf **bipartitan**.
Graf je bipartitan ako se njegovi čvorovi mogu obojiti s 2 boje tako da svaki brid spaja čvorove različitih boja.

**Algoritam (BFS ili DFS):**
1. Oboji prvi neobojani čvor u boju 1.
2. Sve njegove susjede oboji u boju 2.
3. Sve susjede susjeda oboji u boju 1...
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
if (!possible) cout << "IMPOSSIBLE";
else for(int i=1; i<=n; ++i) cout << color[i] << " ";
```

---

<!-- _class: title -->
# 4. Message Route (CSES)

## Najkraći put u općem grafu

---

# Analiza: Message Route

**Problem:**
Mreža računala. Nađi najkraći put (minimalan broj konekcija) od računala 1 do računala $N$.

**Sličnost s Labyrinthom:**
Isti princip (BFS za najkraći put + rekonstrukcija), ali struktura je **graf** (lista susjedstva), a ne 2D mreža.

**Struktura:**
- `adj[N]`: Lista susjedstva.
- `dist[N]`: Udaljenost od izvora (inicijalno $\infty$).
- `parent[N]`: Prethodni čvor na putu (za rekonstrukciju).

---

# Implementacija: Message Route

```cpp
vector<int> dist(n + 1, -1), parent(n + 1);
queue<int> q;

q.push(1);
dist[1] = 0;

while (!q.empty()) {
    int u = q.front(); q.pop();
    if (u == n) break; // Stigli do cilja

    for (int v : adj[u]) {
        if (dist[v] == -1) { // Ako nije posjećen
            dist[v] = dist[u] + 1;
            parent[v] = u; // Pamtimo odakle smo došli
            q.push(v);
        }
    }
}

if (dist[n] == -1) cout << "IMPOSSIBLE";
else {
    // Rekonstrukcija puta od n do 1 preko parent niza
    vector<int> path;
    for (int curr = n; curr != 0; curr = parent[curr]) path.push_back(curr);
    reverse(path.begin(), path.end());
    // Ispis...
}
```

---

# Zadaci za vježbu (Codeforces)

Preporuka: Filtrirati zadatke s tagom `graphs` i težinom `800-1200`.

[Codeforces Graph Problems](https://codeforces.com/problemset?order=BY_RATING_ASC&tags=graphs)

---

