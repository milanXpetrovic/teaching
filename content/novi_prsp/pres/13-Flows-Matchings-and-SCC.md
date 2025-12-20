---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Mrežni tokovi, uparivanja i jake komponente"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---
<!-- _class: title -->

# Mrežni tokovi, uparivanja i jake komponente

## Ford-Fulkerson, Edmonds-Karp, Bipartitno uparivanje, Kosaraju

---

# Slike

- Uvod i Motivacija (Protok)
- http://www.b4b.com.lv/blog-1/params/post/4802130/system-constraint-bottleneck-dialogue-part-2
- https://site-2143475.mozfiles.com/files/2143475/toc1.png

- Slajd "Ford-Fulkerson metoda" ili "Edmonds-Karp".
Izvor: <https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm>
<https://upload.wikimedia.org/wikipedia/commons/a/ad/FordFulkersonDemo.gif>
<https://commons.wikimedia.org/wiki/File:FordFulkerson.gif>

Izvor: Graphs - Maximum flow (Edmonds-Karp)
<https://inginious.org/course/competitive-programming/graphs-maxflow>
<https://inginious.org/course/competitive-programming/graphs-maxflow/anim.gif>

- slajd Ključni koncept: Rezidualni graf

- Slajd: Min-Cut Teorem
https://samarthmittal94.medium.com/graph-theory-max-min-flow-9aa0b378683d

Minimum cut for the network
https://miro.medium.com/v2/resize:fit:640/format:webp/1*JMGSruP13HaLSpIfSpc2Gw.png

- Slajd: Maksimalno Uparivanje (Bipartitni graf)

https://cp-algorithms.com/graph/strongly-connected-components.html

https://cp-algorithms.com/graph/strongly-connected-components-tikzpicture/graph.svg

- Slajd: Kosaraju (Transponirani graf)
https://en.wikipedia.org/wiki/Transpose_graph
transposed-graph.jpg


- Slajd: Police Chase (Zadatak)
https://images.telegram.hr/qVKdQ8iUuK6he71o2-vLq-AOztpQKTgGGKWkTMgLwlg/preset:single1/aHR0cHM6Ly93d3cudGVsZWdyYW0uaHIvd3AtY29udGVudC91cGxvYWRzLzIwMjUvMDcvODcuanBn.jpg

https://www.telegram.hr/vijesti/ovo-je-zagreb-danas-zbog-mimohoda-zatvorene-brojne-ulice-dosta-je-promjena-i-u-javnom-prijevozu/


---

# Sadržaj

1. **Uvod i Motivacija**
   - Protok materijala i resursa
   - Problem dodjele (Assignment problem)
2. **Maksimalni Tok (Maximum Flow)**
   - Definicije i Rezidualni graf
   - Ford-Fulkerson i Edmonds-Karp
   - Min-Cut teorem
3. **Maksimalno Uparivanje**
   - Bipartitni grafovi
4. **Jake Komponente (SCC)**
   - Kosarajuov algoritam
   - 2-SAT problem
5. **Zadaci za vježbu**

---

# Uvod i Motivacija

# 1. Protok (Flow)

Zamislite mrežu cijevi. Želimo poslati **maksimalnu količinu vode** od izvora do ponora.

- Primjeri: Promet u gradu, podaci u računalnoj mreži, logistika.

### 2. Uparivanje (Matching)

Imamo radnike i poslove. Svaki radnik može raditi samo određene poslove.

- Cilj: Zaposliti što više ljudi (maksimalno uparivanje).

### 3. Struktura grafova (SCC)

Kako analizirati grafove koji imaju cikluse?

- **Jako povezana komponenta (SCC):** Unutar nje možemo doći od svakog do svakog.
- Ako sažmemo SCC-ove, dobivamo **DAG** (usmjereni aciklički graf).

---

# Maksimalni Tok: Definicije

Imamo usmjereni graf s izvorom $s$ i ponorom $t$.
Svaki brid $(u, v)$ ima **kapacitet** $c(u, v)$.

**Pravila toka $f(u, v)$:**

1. **Kapacitet:** $0 \le f(u, v) \le c(u, v)$ (Ne možemo poslati više nego što cijev prima).
2. **Očuvanje toka:** Sve što uđe u čvor (osim $s$ i $t$), mora i izaći.

---

# Ključni koncept: Rezidualni graf

Kako znamo možemo li poslati još toka? Gledamo **rezidualni graf**.

Za svaki brid $(u, v)$ s kapacitetom $C$ i trenutnim tokom $F$:

1. **Forward edge $(u, v)$:** Preostali kapacitet je $C - F$.
2. **Backward edge $(v, u)$:** Kapacitet je $F$.
   - *Ovo je ključno!* Omogućuje nam da "poništimo" odluku i preusmjerimo tok ako nađemo bolji put.

---

# Ford-Fulkerson metoda

Ideja: Dok god postoji put od $s$ do $t$ u rezidualnom grafu, šalji tok tim putem!

1. Inicijaliziraj tok na 0.
2. Traži put od $s$ do $t$ (bilo kojim algoritmom) gdje svaki brid ima $kapacitet > 0$.
3. Nađi "usko grlo" (najmanji kapacitet na tom putu).
4. Povećaj tok na bridovima puta, smanji na obrnutim bridovima.
5. Ponavljaj dok puta nema.

## Edmonds-Karp Algoritam

Specifična implementacija Ford-Fulkersona koja koristi **BFS** za traženje puta.

- **Složenost:** $O(V \cdot E^2)$
- Garantira najkraći put (u broju bridova), što osigurava zaustavljanje.

---

# Edmonds-Karp: Implementacija (BFS dio)

```cpp
long long max_flow = 0;
while (true) {
    fill(parent.begin(), parent.end(), -1);
    queue<pair<int, int>> q;
    q.push({s, INF}); parent[s] = s;

    while (!q.empty()) { // BFS traži put
        int u = q.front().first; int flow = q.front().second; q.pop();
        for (int v : adj[u]) {
            if (parent[v] == -1 && capacity[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, capacity[u][v]);
                if (v == t) { path_flow = new_flow; goto found_path; }
                q.push({v, new_flow});
            }
        }
    }
    break; // Nema više puta
    found_path:
    max_flow += path_flow;
    // Ažuriraj kapacitete unatrag (backtracking od t do s)...
}
```

---

# Min-Cut Teorem

**Definicija Reza:** Podjela čvorova na dva skupa $S$ (sadrži izvor) i $T$ (sadrži ponor).
**Kapacitet reza:** Zbroj kapaciteta bridova koji idu iz $S$ u $T$.

> **Teorem:** Vrijednost maksimalnog toka jednaka je kapacitetu minimalnog reza.

**Primjena:**
Nakon što algoritam završi, svi čvorovi do kojih možemo doći iz $s$ u rezidualnom grafu čine skup $S$. Bridovi koji izlaze iz $S$ su "usko grlo" mreže.

---

# Maksimalno Uparivanje (Bipartitni graf)

Imamo dva skupa čvorova, $L$ (lijevo) i $R$ (desno). Bridovi idu samo iz $L$ u $R$.
Želimo odabrati maksimalan broj bridova koji nemaju zajedničkih vrhova.

**Svođenje na Max Flow:**

1. Dodaj **izvor $s$** i spoji ga sa svim čvorovima u $L$ (kapacitet 1).
2. Dodaj **ponor $t$** i spoji sve čvorove iz $R$ prema njemu (kapacitet 1).
3. Svi bridovi između $L$ i $R$ imaju kapacitet 1.
4. Max Flow u ovoj mreži = Veličina maksimalnog uparivanja.

---

# Jako Povezane Komponente (SCC)

**Definicija:** Podskup čvorova gdje postoji put $u \to v$ i $v \to u$ za svaki par.

## Kosarajuov Algoritam $O(N+M)$

Koristi dva prolaza DFS-a.

1. **Prvi prolaz (DFS):**
   Napravi DFS po grafu. Bilježi redoslijed završetka obrade čvorova (stavi ih na stog).

2. **Drugi prolaz (Reverzni DFS):**
   Transponiraj graf (okreni sve bridove: $u \to v$ postaje $v \to u$).
   Uzimaj čvorove sa stoga (obrnutim redoslijedom završetka).
   Ako čvor nije posjećen, pokreni DFS – svi dohvatljivi čvorovi čine jednu **SCC**.

---

# Kosaraju: Implementacija

```cpp
vector<int> order, component;
vector<bool> visited;

void dfs1(int u) { // 1. Prolaz
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) dfs1(v);
    order.push_back(u); // Bilježimo vrijeme izlaska
}

void dfs2(int u) { // 2. Prolaz na obrnutom grafu
    visited[u] = true;
    component.push_back(u);
    for (int v : rev_adj[u]) if (!visited[v]) dfs2(v);
}

// Main:
// 1. Run dfs1 za sve neposjećene
// 2. Reverse(order)
// 3. Reset visited
// 4. Run dfs2 za čvorove iz ordera -> svaki poziv je nova SCC
```

---

# Primjena: 2-SAT Problem

Imamo logičku formulu: $(x_1 \lor \neg x_2) \land (\neg x_1 \lor x_3) \dots$
Može li se zadovoljiti?

**Svođenje na SCC:**

- Svaka varijabla ima dva čvora: $x_i$ i $\neg x_i$.
- Klauzula $(a \lor b)$ je isto što i $(\neg a \implies b)$ i $(\neg b \implies a)$.
- Dodaj bridove za implikacije.

**Rješenje:**
Formula je **nezadovoljiva** ako i samo ako se $x_i$ i $\neg x_i$ nalaze u **istoj SCC** (jer to znači $x_i \implies \neg x_i$ i obrnuto, što je kontradikcija).

---

# Zadaci za vježbu

---
<!-- _class: title -->

# : Police Chase (CSES)

## Primjena Max-Flow Min-Cut teorema

---

# Zadatak: Police Chase

**Problem:**
Kaaleppi je opljačkao banku (čvor 1) i bježi prema luci (čvor $n$). Policija želi spriječiti bijeg zatvaranjem ulica.

**Ulaz:**

- $n$ križanja ($2 \le n \le 500$) i $m$ ulica.
- Ulice su dvosmjerne.

**Izlaz:**

1. **Minimalni broj ulica** koje treba zatvoriti da ne postoji put od 1 do $n$.
2. Popis tih ulica.

---

# Intuicija i Modeliranje

Ovo je klasičan problem **Minimalnog reza (Min-Cut)**.

- Želimo podijeliti graf na dva dijela: jedan koji sadrži izvor (Banku), a drugi ponor (Luku).
- Cijena reza je broj bridova koje "presijecamo".
- Želimo minimizirati tu cijenu.

**Teorem o maksimalnom toku i minimalnom rezu:**
> Vrijednost maksimalnog toka u mreži jednaka je kapacitetu minimalnog reza.

**Ideja rješenja:**

1. Svakoj ulici dodijelimo **kapacitet 1**.
2. Izračunamo **Maksimalni tok** od 1 do $n$. Vrijednost toka = broj ulica.
3. Pronađemo koje su to ulice analizom **rezidualnog grafa**.

---

# Korak 1: Izgradnja grafa

Budući da su ulice dvosmjerne, a graf toka je usmjeren:
Svaka ulica između $u$ i $v$ postaje:

- Brid $u \to v$ s kapacitetom 1.
- Brid $v \to u$ s kapacitetom 1.

Zašto 1? Jer zatvaranje jedne ulice "košta" 1.

```cpp
// Inicijalizacija
for (int i = 0; i < m; ++i) {
    int u, v; cin >> u >> v;
    // Pamtimo originalne bridove za ispis rješenja na kraju
    original_edges.push_back({u, v}); 
    
    // Gradimo graf za Max Flow
    adj[u].push_back(v);
    adj[v].push_back(u);
    capacity[u][v] = 1;
    capacity[v][u] = 1;
}
```

---

# Korak 2: Izračun Maksimalnog toka

Koristimo **Edmonds-Karp** algoritam (BFS za traženje puta).
Kako je $N \le 500$, a kapaciteti su mali, ovo je dovoljno brzo.

```cpp
int max_flow = 0;
while (true) {
    fill(parent.begin(), parent.end(), 0);
    queue<pair<int, int>> q;
    q.push({1, INF}); parent[1] = 1; // 1 je izvor

    while (!q.empty()) {
        int u = q.front().first; int flow = q.front().second; q.pop();
        for (int v : adj[u]) {
            // Tražimo put u REZIDUALNOM grafu (tamo gdje ima preostalog kapaciteta)
            if (parent[v] == 0 && capacity[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, capacity[u][v]);
                if (v == n) { path_flow = new_flow; goto found; } // n je ponor
                q.push({v, new_flow});
            }
        }
    }
    break; // Nema više puta
    found:
    max_flow += path_flow;
    // ... Ažuriraj kapacitete (backtracking) ...
}
```

---

# Korak 3: Rekonstrukcija reza (Ključni dio!)

Nakon što Max Flow algoritam završi, kako znamo koje ulice zatvoriti?

**Definicija Min-Cuta:**

Minimalni rez dijeli čvorove na dva skupa:

- **Skup S:** Čvorovi koji su i dalje **dohvatljivi** iz izvora u *rezidualnom grafu*.
- **Skup T:** Čvorovi koji su postali nedohvatljivi jer su bridovi "zasićeni".

**Algoritam za rekonstrukciju:**

1. Pokreni BFS/DFS iz izvora (čvor 1) koristeći **samo bridove s preostalim kapacitetom > 0**.
2. Svi posjećeni čvorovi čine skup $S$.
3. Rješenje su sve **originalne ulice** $(u, v)$ takve da je jedan kraj u $S$, a drugi u $T$ (nije u $S$).

---

# Implementacija rekonstrukcije

```cpp
// 1. Označi sve dohvatljive čvorove u rezidualnom grafu
vector<bool> visited(n + 1, false);
queue<int> q;
q.push(1);
visited[1] = true;

while (!q.empty()) {
    int u = q.front(); q.pop();
    for (int v : adj[u]) {
        // Ključno: Možemo li proći bridom u rezidualnom grafu?
        if (!visited[v] && capacity[u][v] > 0) {
            visited[v] = true;
            q.push(v);
        }
    }
}

// 2. Ispiši bridove koji prelaze iz S u T
cout << max_flow << endl;
for (auto& edge : original_edges) {
    int u = edge.first;
    int v = edge.second;
    // Ako je jedan kraj dohvatljiv, a drugi nije -> to je brid reza
    if (visited[u] && !visited[v]) cout << u << " " << v << endl;
    else if (visited[v] && !visited[u]) cout << u << " " << v << endl;
}
```

---

# Sažetak rješenja

1. **Modeliraj problem:**
   - Čvorovi = Križanja.
   - Bridovi = Ulice (dvosmjerni, kapacitet 1).
   - Izvor = 1, Ponor = $N$.

2. **Izračunaj Max Flow:**
   - Rezultat (broj) je minimalni broj ulica koje treba zatvoriti.
   - Ovo "zasićuje" usko grlo mreže.

3. **Pronađi Min Cut:**
   - Nađi sve čvorove do kojih još uvijek možemo doći iz izvora (skup $S$).
   - Bridovi koji povezuju $S$ i ostatak svijeta su tražene ulice.

---

<!-- _class: title -->

# School Dance (CSES)

## Maksimalno uparivanje u bipartitnom grafu

---

## Zadatak: School Dance

**Problem:**
U školi je $N$ dječaka i $M$ djevojčica. Postoji $K$ potencijalnih parova (dječak i djevojčica koji žele plesati zajedno).
Svaki učenik može plesati **najviše s jednim** partnerom.

**Cilj:**
Pronaći **maksimalan broj parova** koji mogu plesati istovremeno i ispisati te parove.

**Ograničenja:**

- $N, M \le 500$
- $K \le 1000$

---

# Intuicija: Bipartitni graf

Ovo je problem na **bipartitnom grafu** jer čvorove možemo podijeliti u dvije skupine:

1. **Lijeva strana:** Dječaci (1 do $N$).
2. **Desna strana:** Djevojčice (1 do $M$).

Bridovi postoje **samo** između lijeve i desne strane (nema gej parova u ovom zadatku, niti dječak pleše sam sa sobom).

Tražimo **Maksimalno uparivanje (Matching):** skup bridova bez zajedničkih vrhova.

---

# Rješenje: Svođenje na Maksimalni Tok

Problem rješavamo pretvaranjem u mrežu toka.

1. **Dodamo Super-Izvor ($S$):** Spojimo ga sa svim dječacima.
   - Kapacitet bridova $S \to \text{Boy}_i$ je **1**.
   - (Znači: svaki dječak može sudjelovati u najviše 1 paru).

2. **Dodamo Super-Ponor ($T$):** Spojimo sve djevojčice s njim.
   - Kapacitet bridova $\text{Girl}_j \to T$ je **1**.
   - (Znači: svaka djevojčica može sudjelovati u najviše 1 paru).

3. **Veza Dječak-Djevojčica:**
   - Ako dječak $i$ i djevojčica $j$ žele plesati, dodamo brid $\text{Boy}_i \to \text{Girl}_j$.
   - Kapacitet je **1**.

**Rezultat:** Maksimalni tok u ovoj mreži = Maksimalan broj parova.

---

# Implementacija: Numeracija čvorova

Da bismo izgradili graf, moramo jedinstveno označiti čvorove jer su u ulazu dječaci 1..N i djevojčice 1..M.

**Mapiranje:**

- **Izvor ($S$):** Čvor 0.
- **Dječaci ($1 \dots N$):** Čvorovi $1 \dots N$.
- **Djevojčice ($1 \dots M$):** Čvorovi $N+1 \dots N+M$.
- **Ponor ($T$):** Čvor $N+M+1$.

```cpp
int n, m, k; cin >> n >> m >> k;
int s = 0, t = n + m + 1;

for (int i = 0; i < k; ++i) {
    int u, v; cin >> u >> v;
    // Brid od dječaka u do djevojčice v (mapirane na n+v)
    adj[u].push_back(n + v);
    adj[n + v].push_back(u);
    capacity[u][n + v] = 1; 
}

// Spoji Izvor s Dječacima
for (int i = 1; i <= n; ++i) {
    adj[s].push_back(i); adj[i].push_back(s);
    capacity[s][i] = 1;
}

// Spoji Djevojčice s Ponorom
for (int i = 1; i <= m; ++i) {
    adj[n + i].push_back(t); adj[t].push_back(n + i);
    capacity[n + i][t] = 1;
}
```

---

# Izračun Toka (Edmonds-Karp)

Koristimo standardni algoritam.
Budući da je svaki kapacitet 1, ovo se ponaša kao **Hopcroft-Karp** algoritam u jednostavnijoj formi (zapravo DFS bi ovdje bio brži, ali BFS je siguran i dovoljno brz za $N=500$).

```cpp
int max_pairs = 0;
while (true) {
    fill(parent.begin(), parent.end(), -1);
    queue<pair<int, int>> q;
    q.push({s, INF}); 

    while (!q.empty()) {
        int u = q.front().first; int flow = q.front().second; q.pop();
        for (int v : adj[u]) {
            if (parent[v] == -1 && capacity[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, capacity[u][v]);
                if (v == t) { path_flow = new_flow; goto found; }
                q.push({v, new_flow});
            }
        }
    }
    break; 
    found:
    max_pairs += path_flow;
    // ... update capacities (backwards) ...
    int curr = t;
    while (curr != s) {
        int prev = parent[curr];
        capacity[prev][curr] -= path_flow;
        capacity[curr][prev] += path_flow;
        curr = prev;
    }
}
```

---

# Rekonstrukcija rješenja

Kada algoritam završi, moramo ispisati parove.
Gledamo bridove koji idu od **Dječaka** prema **Djevojčicama**.

Ako je kapacitet brida $\text{Boy}_i \to \text{Girl}_j$ postao **0** (a bio je 1), to znači da je tok prošao tuda -> **Oni su par!**

```cpp
cout << max_pairs << endl;

for (int i = 1; i <= n; ++i) { // Iteriraj kroz dječake
    for (int v : adj[i]) {
        // Ako je susjed djevojčica (indeks > n) i ne uključuje Izvor/Ponor
        if (v > n && v != t) {
            // Ako je kapacitet 0, znači da je iskorišten
            if (capacity[i][v] == 0) {
                // Ispiši originalne indekse
                cout << i << " " << (v - n) << endl;
            }
        }
    }
}
```

---

# Sažetak

1. **Modeliranje:**
   - Izvor $\to$ Dječaci (cap 1).
   - Djevojčice $\to$ Ponor (cap 1).
   - Dječak $\to$ Djevojčica (cap 1).

2. **Algoritam:**
   - Pusti Max Flow.
   - Vrijednost toka je broj parova.

3. **Ispis:**
   - Provjeri zasićene bridove između dječaka i djevojčica.
   - Pazi na mapiranje indeksa ($v - n$ za djevojčice).

---

<!-- _class: title -->

# CSES: Distinct Routes

## Bridno disjunktni putevi i rekonstrukcija toka

---

# Zadatak: Distinct Routes

**Problem:**
Igra se odvija u $N$ soba povezanih teleporterima. Cilj je doći od sobe 1 do sobe $N$.
Svaki teleporter (brid) može se iskoristiti **najviše jednom** tijekom cijele igre (kroz sve dane).

**Pitanje:**
Koliko najviše dana možemo igrati (tj. koliko različitih puteva možemo pronaći) i koji su to putevi?

**Ograničenja:**

- $N \le 500$, $M \le 1000$.
- Bridovi su usmjereni.

---

# Modeliranje: Max Flow

Ovo je školski primjer problema **bridno disjunktnih puteva**.

1. **Kapaciteti:**
   Svakom teleporteru dodijelimo **kapacitet 1**.
   - To osigurava da kroz njega tok može proći najviše jednom.

2. **Tok:**
   Pustimo Maksimalni tok od čvora 1 do čvora $N$.

3. **Značenje rezultata:**
   - **Vrijednost Max Flow-a ($K$)** = Maksimalni broj dana (puteva).
   - Svaka jedinica toka koja stigne u ponor predstavlja jedan validan put.

---

# Korak 1: Izračun toka

Koristimo standardni Edmonds-Karp ili Dinic algoritam.
Bitno je pamtiti strukturu brida kako bismo kasnije mogli provjeriti koji su bridovi iskorišteni.

```cpp
struct Edge {
    int v;          // Kamo vodi
    int flow;       // Trenutni tok
    int capacity;   // Kapacitet (uvijek 1 u startu)
    int rev;        // Indeks obrnutog brida u adj[v]
};

// ... Inicijalizacija i Max Flow algoritam ...
// Nakon izvršenja, imamo varijablu max_flow = K.
cout << max_flow << endl;
```

Nakon što algoritam završi, bridovi koji su dio rješenja imat će `flow == 1`.

---

# Korak 2: Rekonstrukcija puteva (Izazov)

Imamo mrežu kroz koju "teče" $K$ jedinica toka. Kako ih razdvojiti u $K$ zasebnih puteva?

**Ideja (Ljuštenje grafa):**

1. Znamo da imamo $K$ puteva.
2. Pokrenemo petlju $K$ puta.
3. U svakoj iteraciji radimo **DFS** (ili jednostavnu šetnju) od izvora (1) do ponora ($N$).
4. Krećemo se **samo po bridovima koji imaju `flow == 1`**.
5. **Ključno:** Kad prođemo kroz brid, postavimo mu `flow = 0`.
   - Time ga "brišemo" iz grafa da ga idući put ne koristimo.
   - Zbog očuvanja toka, sigurno ćemo stići do ponora.

---

# Implementacija rekonstrukcije

```cpp
vector<int> path; // Trenutni put

// DFS funkcija za pronalazak JEDNOG puta
void find_path(int u) {
    path.push_back(u);
    if (u == n) return; // Stigli smo do cilja

    for (auto& e : adj[u]) {
        // Tražimo brid koji je zasićen (flow == 1) i ima kapacitet 1
        // (Pazimo da ne idemo po backward bridovima rezidualnog grafa)
        if (e.capacity == 1 && e.flow == 1) {
            e.flow = 0; // "Potroši" brid da ga ne nađemo opet
            find_path(e.v);
            return; // Našli smo nastavak puta, prekidamo petlju za ovaj čvor
        }
    }
}

// U main funkciji nakon Max Flow-a:
for (int i = 0; i < max_flow; ++i) {
    path.clear();
    find_path(1);
    
    // Ispis puta
    cout << path.size() << endl;
    for (int node : path) cout << node << " ";
    cout << endl;
}
```

---

# Detalji implementacije (Iterativno)

Rekurzija je OK, ali iterativni pristup je često sigurniji i lakši za shvatiti.

```cpp
for (int k = 0; k < max_flow; ++k) {
    vector<int> current_path;
    int curr = 1;
    
    while (curr != n) {
        current_path.push_back(curr);
        
        for (auto& edge : adj[curr]) {
            // Ako je brid dio toka (flow == 1) i nije backward brid
            if (edge.capacity == 1 && edge.flow == 1) {
                edge.flow = 0; // Ukloni brid
                curr = edge.v; // Pomakni se na idući čvor
                break; // Izađi iz for petlje, nastavi while
            }
        }
    }
    current_path.push_back(n); // Dodaj krajnji čvor

    // Ispis
    cout << current_path.size() << endl;
    for (int node : current_path) cout << node << " ";
    cout << endl;
}
```

---

# Sažetak

1. **Problem:** Naći što više puteva koji ne dijele bridove.
2. **Alat:** Maksimalni tok s kapacitetima bridova = 1.
3. **Rezultat:** Vrijednost toka je broj puteva.
4. **Ispis:**
   - Graf sada sadrži superpoziciju svih puteva.
   - Koristimo pohlepni prolaz (DFS/While) prateći bridove s tokom.
   - **Destruktivno čitanje:** Kad iskoristimo brid za jedan put, brišemo mu tok da ga ne bi koristili za drugi put.

---

# CSES: Coin Collector

## Kondenzacija grafa i DP na DAG-u

---

# Zadatak: Coin Collector

**Problem:**
Imamo $N$ soba i $M$ jednosmjernih tunela. Svaka soba sadrži određeni broj novčića $k_i$.
Možemo početi u bilo kojoj sobi i završiti u bilo kojoj.

**Cilj:**
Sakupiti **maksimalan ukupan broj novčića**.
(Napomena: Ako se vrtimo u krug, možemo pokupiti novčiće iz svih soba u tom krugu).

**Ograničenja:**

- $N \le 10^5$, $M \le 2 \cdot 10^5$.
- Novčići $k_i \le 10^9$.
- **Pazi:** Ukupna suma može premašiti 32-bitni integer -> Koristi `long long`.

---

# Intuicija i Analiza

1. **Ciklusi:**
   Ako uđemo u skup soba koje čine ciklus (ili jače: **Jako Povezanu Komponentu - SCC**), možemo se vrtjeti u krug koliko god želimo.
   $\Rightarrow$ **Uvijek uzimamo SVE novčiće iz cijele komponente.**

2. **Kondenzacija grafa:**
   Možemo promatrati svaku SCC kao jedan **"Super-čvor"**.
   Težina tog super-čvora je zbroj svih novčića u toj komponenti.

3. **Struktura:**
   Kada graf sažmemo u SCC-ove, dobivamo **DAG** (Directed Acyclic Graph).
   Problem se svodi na pronalaženje puta s najvećom težinom u DAG-u.

---

# Korak 1: Pronalaženje SCC-ova

Koristimo **Kosarajuov algoritam** (ili Tarjanov) da identificiramo komponente.
Istovremeno računamo sumu novčića za svaku komponentu.

```cpp
// 1. Prolaz (DFS) - računanje poretka
void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) if (!visited[v]) dfs1(v);
    order.push_back(u);
}

// 2. Prolaz (Reverzni DFS) - formiranje komponenti
void dfs2(int u, int comp_id) {
    visited[u] = true;
    component[u] = comp_id;
    scc_coins[comp_id] += coins[u]; // Zbrajamo novčiće u komponenti!
    for (int v : rev_adj[u]) if (!visited[v]) dfs2(v, comp_id);
}
```

---

# Korak 2: Izgradnja Kondenziranog Grafa (DAG)

Sada gradimo novi graf gdje su čvorovi indeksi komponenata.

```cpp
// adj_scc[u] sadrži listu susjednih KOMPONENTI
vector<int> adj_scc[MAXN]; 

for (int u = 1; u <= n; ++u) {
    for (int v : adj[u]) {
        // Ako postoji brid između dvije RAZLIČITE komponente
        if (component[u] != component[v]) {
            adj_scc[component[u]].push_back(component[v]);
        }
    }
}
```

*Napomena:* Ovdje možemo dobiti višestruke bridove između istih komponenti. Za DP nam to ne smeta (samo ćemo uzeti max više puta), ali možemo koristiti `std::unique` ili `std::set` ako želimo čišći graf.

---

# Korak 3: DP na DAG-u

Tražimo najduži put (težinski) u DAG-u. Budući da nema ciklusa, možemo koristiti **memoizaciju** (rekurziju s pamćenjem).

**Stanje:** `dp[u]` = maksimalni novčići koje možemo skupiti počevši od komponente `u`.
**Prijelaz:** `dp[u] = scc_coins[u] + max(dp[v])` za sve susjedne komponente `v`.

```cpp
long long memo[MAXN];
bool visited_dp[MAXN];

long long solve_dp(int u) {
    if (visited_dp[u]) return memo[u];
    
    long long max_next = 0;
    for (int v : adj_scc[u]) {
        max_next = max(max_next, solve_dp(v));
    }
    
    visited_dp[u] = true;
    return memo[u] = scc_coins[u] + max_next;
}
```

---

# Glavni program (Main logic)

```cpp
int main() {
    // ... Učitavanje, Kosaraju algoritam ...
    
    // Izračunaj SCC-ove i popuni scc_coins
    // Izgradi adj_scc graf
    
    long long ans = 0;
    
    // Rješenje je maksimum DP-a pokrenutog iz svake komponente
    // (Možemo početi bilo gdje)
    for (int i = 1; i <= scc_count; ++i) {
        ans = max(ans, solve_dp(i));
    }
    
    cout << ans << endl;
}
```

**Složenost:**

- Kosaraju: $O(N + M)$
- Izgradnja DAG-a: $O(N + M)$
- DP (svaki brid i čvor DAG-a jednom): $O(N_{scc} + M_{scc})$
- **Ukupno:** $O(N + M)$, što je idealno za $10^5$.

---

# Sažetak rješenja

1. **Prepoznaj SCC:** Ako možeš kružiti, uzmi sve.
   $\to$ Kondenziraj graf u komponente.
2. **Izračunaj težine:** Svaki čvor u novom grafu ima težinu = sumi novčića u toj komponenti.
3. **Izgradi DAG:** Bridovi idu samo između različitih komponenata.
4. **DP:** Nađi put s najvećom sumom u DAG-u.
   - `dp[u] = weight[u] + max(dp[neighbours])`

---

<!-- _class: title -->

# CSES: Planets and Kingdoms

## Direktna primjena Jakih Komponenti (SCC)

---

## Zadatak: Planets and Kingdoms

**Problem:**
Imamo $N$ planeta i $M$ jednosmjernih teleportera.
Definicija kraljevstva: Dva planeta $A$ i $B$ pripadaju istom kraljevstvu **ako i samo ako** postoji put od $A$ do $B$ **I** put od $B$ do $A$.

**Cilj:**

1. Odrediti ukupan broj kraljevstava.
2. Svakom planetu dodijeliti oznaku kraljevstva (broj od $1$ do $K$).

**Ograničenja:**

- $N \le 10^5$, $M \le 2 \cdot 10^5$.
- Potrebna složenost: Linearna $O(N+M)$.

---

# Teorija: Što je zapravo "Kraljevstvo"?

Uvjet zadatka ($A \to B$ i $B \to A$) je točna matematička definicija **Jako Povezane Komponente (Strongly Connected Component - SCC)**.

Zadatak se svodi na:

1. Pronađi sve SCC-ove u grafu.
2. Prebroji ih.
3. Svakom čvoru pridruži ID njegove komponente.

Koristit ćemo **Kosarajuov algoritam** (dva prolaza DFS-a).

---

# Kosarajuov Algoritam: Pregled

Algoritam radi u dva koraka koristeći DFS:

1. **Prvi prolaz (Originalni graf):**
   - Cilj je odrediti "topološki" poredak završetka obrade.
   - Kad DFS završi s čvorom $u$, stavimo ga na **stog** (ili listu).

2. **Drugi prolaz (Transponirani graf):**
   - "Okrenemo" sve bridove ($u \to v$ postaje $v \to u$).
   - Uzimamo čvorove sa stoga (zadnji obrađen $\to$ prvi).
   - Ako čvor nije posjećen, pokrećemo DFS. Svi dohvatljivi čvorovi u ovom koraku čine **jedno kraljevstvo**.

---

# Korak 1: Prvi DFS (Punjenje stoga)

Trebamo pratiti poredak izlaska iz DFS-a.

```cpp
vector<int> adj[MAXN], rev_adj[MAXN];
vector<int> order;
bool visited[MAXN];

void dfs1(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) dfs1(v);
    }
    // Ključno: dodajemo u listu tek kad smo obradili svu djecu
    order.push_back(u); 
}
```

*Napomena:* Učitavanjem bridova odmah gradimo i `rev_adj` (obrnuti graf).
`rev_adj[v].push_back(u)` za svaki ulaz `u -> v`.

---

# Korak 2: Drugi DFS (Označavanje kraljevstava)

Sada radimo na **obrnutom** grafu. Svaki put kad pokrenemo `dfs2` iz *main* petlje, nalazimo novo kraljevstvo.

```cpp
int kingdom[MAXN]; // Ovdje spremamo rješenje

void dfs2(int u, int k_id) {
    visited[u] = true;
    kingdom[u] = k_id; // Pridruži planetu ID kraljevstva
    
    for (int v : rev_adj[u]) {
        if (!visited[v]) dfs2(v, k_id);
    }
}
```

---

# Glavni program (Spajanje svega)

```cpp
int main() {
    // ... Učitaj N, M, izgradi adj i rev_adj ...

    // 1. Prolaz
    fill(visited, visited + n + 1, false);
    for (int i = 1; i <= n; ++i) {
        if (!visited[i]) dfs1(i);
    }

    // 2. Prolaz
    fill(visited, visited + n + 1, false);
    reverse(order.begin(), order.end()); // Bitno! Krećemo od zadnjeg završenog
    
    int kingdom_count = 0;
    for (int u : order) {
        if (!visited[u]) {
            kingdom_count++;
            dfs2(u, kingdom_count);
        }
    }

    // Ispis rezultata
    cout << kingdom_count << endl;
    for (int i = 1; i <= n; ++i) {
        cout << kingdom[i] << " ";
    }
    cout << endl;
}
```

---

# Analiza Složenosti

1. **Izgradnja grafa:** $O(N + M)$ (učitavamo i gradimo normalni i reverzni graf).
2. **Prvi DFS:** Posjeti svaki čvor i brid točno jednom. $O(N + M)$.
3. **Drugi DFS:** Također posjeti svaki čvor i brid točno jednom (na reverznom grafu). $O(N + M)$.

**Ukupna složenost:** **$O(N + M)$**
Vremenski limit od 1.00s je sasvim dovoljan za $N=10^5$.
Memorijski limit je također siguran (koristimo nekoliko nizova veličine $N$).

---

# Sažetak

1. Problem traži particioniranje grafa na skupove uzajamno dohvatljivih čvorova.
2. To je definicija **Jako Povezanih Komponenti (SCC)**.
3. Rješenje je "udžbenička" primjena **Kosarajuovog algoritma**:
   - DFS1 (sortiraj po vremenu završetka).
   - Obrni bridove.
   - DFS2 (broji komponente i označavaj).

---
