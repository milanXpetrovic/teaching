---
nav_exclude: true
---

# Tjedan 9: Algoritmi za Najkraći Put

## Sadržaj
1.  [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Problem Najkraćeg Puta](#problem-najkraćeg-puta)
    *   [Razlika u Odnosu na BFS](#razlika-u-odnosu-na-bfs)
    *   [Dva Ključna Algoritma: Dijkstra i Bellman-Ford](#dva-ključna-algoritma-dijkstra-i-bellman-ford)
    *   [Preporučena Literatura](#preporučena-literatura)
2.  [Dijkstra Algoritam (za ne-negativne težine)](#dijkstra-algoritam-za-ne-negativne-težine)
    *   [Intuicija: Širenje Kruga Poznatog](#intuicija-širenje-kruga-poznatog)
    *   [Implementacija s Prioritetnim Redom](#implementacija-s-prioritetnim-redom)
    *   [Analiza Složenosti](#analiza-složenosti)
3.  [Bellman-Ford Algoritam (za težine koje mogu biti negativne)](#bellman-ford-algoritam-za-težine-koje-mogu-biti-negativne)
    *   [Intuicija: Iterativno Poboljšavanje](#intuicija-iterativno-poboljšavanje)
    *   [Detekcija Negativnih Ciklusa](#detekcija-negativnih-ciklusa)
    *   [Implementacija](#implementacija)
    *   [Analiza Složenosti](#analiza-složenosti-1)
4.  [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Problem Najkraćeg Puta
Problem pronalaženja najkraćeg puta između dva čvora u grafu jedan je od najvažnijih i najčešćih problema u računarstvu. Primjene su svuda oko nas:
-   **GPS navigacija:** Pronalaženje najbrže rute od točke A do točke B.
-   **Mrežni usmjerivači:** Određivanje najefikasnijeg puta za slanje paketa podataka.
-   **Analiza ovisnosti:** Pronalaženje najkraćeg niza koraka za izvršenje zadatka.

Formalno, zadan je **težinski usmjeren graf** `G = (V, E)` gdje svaka veza `(u, v)` ima težinu `w(u, v)`. Duljina puta je zbroj težina veza na tom putu. Cilj je pronaći put minimalne duljine od početnog čvora `s` do svih ostalih čvorova (ili do određenog ciljnog čvora `t`).

### Razlika u Odnosu na BFS
Prošli tjedan smo vidjeli BFS (pretraživanje u širinu) kao metodu za pronalaženje najkraćeg puta. Važno je razumjeti da BFS pronalazi put s **najmanjim brojem veza**, što je ekvivalentno rješavanju problema na **ne-težinskom grafu** (gdje svaka veza ima težinu 1).

Ako veze imaju različite težine, BFS ne daje točno rješenje. Put s manje veza može biti "skuplji" od puta s više veza.

### Dva Ključna Algoritma: Dijkstra i Bellman-Ford
Ovaj tjedan fokusiramo se na dva temeljna algoritma:

1.  **Dijkstra algoritam:** Izuzetno efikasan (`O(m log n)`), ali radi samo ako su sve težine veza **ne-negativne**. Ovo je najčešće korišten algoritam za najkraći put u praksi.
2.  **Bellman-Ford algoritam:** Sporiji (`O(nm)`), ali robusniji. Radi i s **negativnim težinama veza** i može detektirati postojanje **negativnih ciklusa** (ciklusa čiji je zbroj težina negativan, što implicira da "najkraći put" nije dobro definiran).

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 13: *Shortest paths*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 24: *Single-Source Shortest Paths* (detaljna teorijska podloga)

---

## Dijkstra Algoritam (za ne-negativne težine)

### Intuicija: Širenje Kruga Poznatog
Dijkstra algoritam je **pohlepni algoritam**. Možemo ga zamisliti kao proces širenja "kruga poznatog teritorija" iz početnog čvora `s`.
1.  U početku, znamo samo udaljenost do `s`, koja je 0. Za sve ostale čvorove, pretpostavljamo da je udaljenost beskonačna.
2.  Algoritam održava skup **obrađenih** čvorova. Na svakom koraku, pohlepno odabire čvor `u` koji **nije obrađen**, a ima **najmanju trenutno poznatu udaljenost** od `s`.
3.  Kada odaberemo `u`, proglašavamo njegovu udaljenost **konačnom**. Zašto je to sigurno? Budući da su sve težine veza ne-negativne, bilo koji drugi put do `u` koji bi išao preko nekog još neobrađenog čvora `v` morao bi imati veću ili jednaku udaljenost.
4.  Nakon obrade `u`, ažuriramo (relaksiramo) udaljenosti do svih njegovih susjeda.

### Implementacija s Prioritetnim Redom
Za efikasno pronalaženje čvora s najmanjom udaljenošću, koristimo **prioritetni red (min-heap)**.
-   U red spremamo parove `(udaljenost, čvor)`.
-   Na početku, u red stavimo `(0, s)`.
-   U svakoj iteraciji, `extract-min` operacija nam u `O(log n)` vremenu daje sljedeći najbliži čvor.

**Kod:**
```cpp
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18;
const int MAXN = 1e5 + 5;

vector<pair<int, int>> adj[MAXN];
vector<long long> distance(MAXN, INF);
vector<bool> processed(MAXN, false);

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, m; // broj čvorova i veza
    cin >> n >> m;
    for (int i = 0; i < m; ++i) {
        int a, b, w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
        // Za neusmjereni graf: adj[b].push_back({a, w});
    }

    int start_node = 1;
    distance[start_node] = 0;
    
    // Prioritetni red sprema {-udaljenost, čvor}
    // Negativna udaljenost jer C++ priority_queue je max-heap
    priority_queue<pair<long long, int>> q;
    q.push({0, start_node});

    while (!q.empty()) {
        int a = q.top().second;
        q.pop();

        if (processed[a]) continue;
        processed[a] = true;

        for (auto edge : adj[a]) {
            int b = edge.first;
            int w = edge.second;
            if (distance[a] + w < distance[b]) {
                distance[b] = distance[a] + w;
                q.push({-distance[b], b});
            }
        }
    }
    
    for (int i = 1; i <= n; ++i) {
        cout << distance[i] << " ";
    }
    cout << '\n';

    return 0;
}
```

### Analiza Složenosti
-   Svaki čvor se dodaje u prioritetni red.
-   Svaki čvor se vadi iz reda točno jednom (zbog `processed` provjere).
-   Svaki brid `(u, v)` se relaksira točno jednom kada se `u` obrađuje.
-   `push` i `pop` operacije na `priority_queue` traju `O(log n)`.

Ukupna složenost je **O(m log n)** (ili preciznije, `O(n log n + m log n)`), gdje je `n` broj čvorova, a `m` broj veza.

---

## Bellman-Ford Algoritam (za težine koje mogu biti negativne)

### Intuicija: Iterativno Poboljšavanje
Bellman-Ford je algoritam temeljen na dinamičkom programiranju. Njegova osnovna ideja je:
-   Najkraći put od `s` do bilo kojeg čvora može imati najviše `n-1` bridova (ako nema negativnih ciklusa).
-   Algoritam iterativno pronalazi najkraće puteve koristeći sve više i više bridova.
-   Nakon `i` iteracija, algoritam garantira da je pronašao sve najkraće puteve koji koriste najviše `i` bridova.

Zbog toga, algoritam jednostavno ponavlja proces relaksacije **svih bridova u grafu** `n-1` puta.

**Algoritam:**
1.  Inicijaliziraj udaljenosti: `dist[s] = 0`, `dist[v] = ∞` za sve ostale.
2.  Ponavljaj `n-1` puta:
    *   Za svaki brid `(a, b)` s težinom `w`:
        *   Relaksiraj brid: `dist[b] = min(dist[b], dist[a] + w)`.

### Detekcija Negativnih Ciklusa
Što se dogodi ako algoritam pokrenemo `n` puta umjesto `n-1`?
-   Ako u `n`-toj iteraciji i dalje dođe do smanjenja neke udaljenosti, to znači da postoji **negativni ciklus** dostupan iz `s`. Zašto? Najkraći *jednostavni* put ima najviše `n-1` bridova. Ako se put može skratiti `n`-tim bridom, taj put mora sadržavati ciklus. Ako taj ciklus smanjuje ukupnu duljinu, on mora biti negativan.

### Implementacija
Budući da moramo iterirati kroz sve bridove, reprezentacija grafa kao **lista bridova** je najjednostavnija.

**Kod:**
```cpp
#include <iostream>
#include <vector>
#include <tuple>

const long long INF = 1e18;

int main() {
    // ... Brzi I/O ...
    int n, m; // broj čvorova i veza
    cin >> n >> m;
    vector<tuple<int, int, int>> edges;
    for (int i = 0; i < m; ++i) {
        int a, b, w;
        cin >> a >> b >> w;
        edges.emplace_back(a, b, w);
    }
    
    int start_node = 1;
    vector<long long> distance(n + 1, INF);
    distance[start_node] = 0;
    
    for (int i = 0; i < n - 1; ++i) {
        for (auto e : edges) {
            int a, b, w;
            tie(a, b, w) = e;
            if (distance[a] != INF) {
                distance[b] = min(distance[b], distance[a] + w);
            }
        }
    }

    // Provjera za negativne cikluse (n-ta iteracija)
    for (auto e : edges) {
        int a, b, w;
        tie(a, b, w) = e;
        if (distance[a] != INF && distance[a] + w < distance[b]) {
            // Pronađen je negativni ciklus
            // Ovdje se može označiti da su svi čvorovi dostupni iz ovog ciklusa na -INF
        }
    }
    
    // Ispis udaljenosti
    for (int i = 1; i <= n; ++i) {
        cout << distance[i] << " ";
    }
    cout << '\n';

    return 0;
}
```

### Analiza Složenosti
-   Inicijalizacija: O(n).
-   Glavni dio: `n-1` iteracija, svaka prolazi kroz `m` bridova. Ukupno `(n-1) * m`.
-   Detekcija ciklusa: Jedan dodatni prolaz kroz `m` bridova.

Ukupna složenost je **O(nm)**. Ovo je znatno sporije od Dijkstrinog algoritma, ali je nužno ako graf sadrži negativne težine.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **Shortest Routes I:** Standardna primjena Dijkstrinog algoritma.
*   **Shortest Routes II:** Problem najkraćeg puta između svih parova. Može se riješiti pokretanjem Dijkstre `n` puta (ako nema negativnih težina), ili Floyd-Warshall algoritmom (koji ćemo raditi kasnije).
*   **High Score:** Problem pronalaženja *najdužeg* puta. Može se transformirati u problem najkraćeg puta množenjem svih težina s -1. Ovo stvara negativne težine i potencijalne negativne cikluse (koji su sada "pozitivni" ciklusi). Bellman-Ford je potreban.
*   **Flight Discount:** Zahtijeva modifikaciju stanja. Umjesto `dist[u]`, koristimo `dist[u][0]` (bez popusta) i `dist[u][1]` (s popustom). Primijeni Dijkstrin algoritam na ovaj prošireni graf stanja.
*   **Flight Routes:** Pronalaženje `k` najkraćih puteva. Modifikacija Dijkstrinog algoritma gdje za svaki čvor pamtimo `k` najboljih udaljenosti, npr. u `priority_queue` ili `multiset`.

### Codeforces

*   **Dijkstra?** (Problem 20C): Direktan zadatak za vježbu Dijkstrinog algoritma s ispisom puta.
*   **Bellman-Ford:** Potražite probleme s tagom `bellman-ford` ili `shortest-paths` na Codeforcesu. Često uključuju negativne težine ili detekciju negativnih ciklusa. Jedan takav klasičan problem je **Wormholes** (dostupan na raznim platformama poput UVA Online Judge, ID 558).


### Sljedeća lekcija: []()

[Sljedeća lekcija: ](){: .btn .btn-purple .float-right}