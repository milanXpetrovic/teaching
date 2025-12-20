---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pohlepni algoritmi"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- _class: title  -->

# Pohlepni algoritmi

## Lokalno optimalno = Globalno optimalno?

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Uvod i motivacija**
   - Što je pohlepni algoritam?
   - Usporedba s dinamičkim programiranjem
2. **Problem novčića (Coin Problem)**
   - Kada radi, a kada ne?
3. **Raspoređivanje događaja (Activity Selection)**
   - Strategija ranog završetka
4. **Huffmanovo kodiranje**
   - Kompresija podataka
5. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Uvod i motivacija

## Strategija donošenja odluka

---

# Što je pohlepni algoritam?

**Definicija:** Strategija koja na svakom koraku donosi **lokalno optimalan izbor** u nadi da će to dovesti do **globalno optimalnog rješenja**.

**Karakteristike:**
- **Konačnost odluke:** Jednom napravljen izbor se ne preispituje (nema *backtrackinga*).
- **Brzina:** Obično vrlo efikasni ($O(N)$ ili $O(N \log N)$ zbog sortiranja).
- **Jednostavnost:** Lako se implementiraju, ali...
- **Izazov:** Teško je dokazati da su ispravni za svaki slučaj.

---

# Pohlepni vs. Dinamičko Programiranje

Obje tehnike koriste svojstvo **optimalne podstrukture**, ali pristupaju problemu drugačije:

| Dinamičko Programiranje | Pohlepni Algoritmi |
| :--- | :--- |
| **Bottom-up:** Rješava sve podprobleme, pa donosi odluku. | **Top-down:** Donosi odluku odmah, pa rješava preostali problem. |
| Razmatra **sve** opcije. | Razmatra **samo jednu** (pohlepnu) opciju. |
| Sporije, ali sigurnije. | Brže, ali ne radi uvijek. |

---

# Ključna svojstva

Da bi pohlepni pristup bio ispravan, problem mora zadovoljiti:

1. **Svojstvo pohlepnog izbora (Greedy-choice property):**
   Globalno optimalno rješenje možemo izgraditi nizom lokalno optimalnih izbora. Prvi izbor nas ne sprječava da dođemo do rješenja.

2. **Optimalna podstruktura (Optimal substructure):**
   Optimalno rješenje problema sadrži optimalna rješenja svojih podproblema.

---

<!-- _class: lead -->
# Problem novčića

## Coin Problem

---

# Problem novčića

**Zadatak:** Pronađi minimalan broj novčića za iznos $N$ koristeći zadane denominacije.

**Pohlepna strategija:**
Uvijek uzmi **najveći mogući novčić** koji je manji ili jednak preostalom iznosu.

**Primjer (Euro):** $N = 48$
1. Uzmi 20 (ostalo 28)
2. Uzmi 20 (ostalo 8)
3. Uzmi 5 (ostalo 3)
4. Uzmi 2 (ostalo 1)
5. Uzmi 1 (ostalo 0)
**Rješenje:** 5 novčića. (Optimalno!)

---

# Kada pohlepni pristup NE radi?

Pohlepna strategija radi za "kanonske" sustave (Euro, Dolar), ali ne za sve.

**Kontraprimjer:**
- Kovanice: $\{1, 3, 4\}$
- Cilj: $6$

**Pohlepno:** $4 + 1 + 1$ $\rightarrow$ **3 novčića**.
**Optimalno:** $3 + 3$ $\rightarrow$ **2 novčića**.

**Zaključak:** Za općeniti skup kovanica moramo koristiti **Dinamičko programiranje**.

---

<!-- _class: lead -->
# Raspoređivanje događaja

## Activity Selection Problem

---

# Problem: Activity Selection

**Zadatak:** Odaberi maksimalan broj događaja koji se ne preklapaju. Svaki događaj ima `start` i `end` vrijeme.

**Koja je ispravna pohlepna strategija?**
1. ~~Najkraći događaj?~~ (Ne, kratak može biti u sredini dva duga)
2. ~~Najraniji početak?~~ (Ne, jedan dugi može blokirati sve ostale)
3. **Najraniji završetak!**

**Intuicija:**
Odabirom događaja koji **najranije završava**, oslobađamo resurs što je prije moguće za ostale događaje.

---

# Algoritam i Implementacija

1. **Sortiraj** događaje po vremenu završetka.
2. Uzmi prvi događaj.
3. Uzmi sljedeći koji počinje **nakon** što je prethodni završio.

```cpp
struct Event { int start, end; };
// Sortiramo po vremenu završetka
bool compareEvents(const Event& a, const Event& b) {
    return a.end < b.end;
}

sort(events.begin(), events.end(), compareEvents);

int count = 1;
int last_end = events[0].end;

for (int i = 1; i < n; ++i) {
    if (events[i].start >= last_end) { // Ako se ne preklapa
        count++;
        last_end = events[i].end;
    }
}
```
**Složenost:** $O(N \log N)$ zbog sortiranja.

---

<!-- _class: lead -->
# Huffmanovo kodiranje

## Kompresija podataka

---

# Huffmanovo kodiranje

**Cilj:** Prikazati podatke koristeći što manje bitova (kompresija). Česti znakovi trebaju imati kraće kodove.
**Uvjet:** Kodovi moraju biti **prefiksni** (nijedan kod nije početak drugog).

**Pohlepna strategija:**
Gradi stablo odozdo prema gore. U svakom koraku spoji **dva čvora s najmanjom frekvencijom**.

**Alat:** Prioritetni red (`std::priority_queue`).

---

# Algoritam (Huffman)

1. Kreiraj list za svaki znak (težina = frekvencija).
2. Ubaci sve u **Min-Heap**.
3. Dok u heapu ima više od 1 čvora:
   - Izvadi dva najmanja: $A$ i $B$.
   - Kreiraj novi čvor $C$ s težinom $freq(A) + freq(B)$.
   - Postavi $A$ i $B$ kao djecu od $C$.
   - Vrati $C$ u heap.

**Rezultat:** Stablo gdje put lijevo znači `0`, a desno `1`.

---

# Implementacija (Snippet)

```cpp
priority_queue<Node*, vector<Node*>, compare> minHeap;

// Inicijalizacija heapa...

while (minHeap.size() != 1) {
    // Uzmi dva najmanja
    left = minHeap.top(); minHeap.pop();
    right = minHeap.top(); minHeap.pop();

    // Spoji ih u novi čvor
    top = new Node('$', left->freq + right->freq);
    top->left = left;
    top->right = right;
    
    minHeap.push(top);
}
// minHeap.top() je korijen Huffmanovog stabla
```
**Složenost:** $O(N \log N)$.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set

1. **[Movie Festival](https://cses.fi/problemset/task/1629)**
   - Klasičan *Activity Selection* problem. Sortiraj po kraju filma.
2. **[Stick Lengths](https://cses.fi/problemset/task/1074)**
   - Minimiziraj sumu razlika $|x - p_i|$. Optimalno $x$ je **medijan**.
3. **[Tasks and Deadlines](https://cses.fi/problemset/task/1630)**
   - Maksimiziraj profit = $deadline - finish$.
   - *Hint:* Obavljaj kraće zadatke prve.
4. **[Towers](https://cses.fi/problemset/task/1073)**
   - Slaganje kocki jedne na drugu. Zahtijeva `multiset` za efikasno traženje "baze".

---

# Codeforces preporuke

Tražite zadatke s tagom `greedy` težine 800-1200.

- **[Ciel and Receipt](https://codeforces.com/problemset/problem/320/A)**
  - Problem sličan problemu novčića (potencije broja 2).
- **[Boats Competition](https://codeforces.com/problemset/problem/1399/C)**
  - Formiranje parova s istom težinom. Sortiranje + Two Pointers.

---

<!-- _class: title -->
# Movie Festival (CSES)

## Activity Selection u praksi

---

# Analiza: Movie Festival

**Problem:**
U kinu se prikazuje $n$ filmova. Svaki ima vrijeme početka i kraja.
Želimo pogledati **maksimalan broj filmova** u cijelosti (bez preklapanja).

### Intuicija
Ovo je identičan problem kao **Activity Selection**.
Pohlepna strategija: Uvijek biraj film koji **najranije završava**, a da ne počinje prije nego što je prethodni završio.

Zašto? Time ostavljamo najviše vremena za ostale filmove.

---

# Implementacija: Movie Festival

```cpp
int n; cin >> n;
vector<pair<int, int>> movies(n);
for(int i=0; i<n; ++i) 
    cin >> movies[i].second >> movies[i].first; // Učitaj kao {kraj, početak}

sort(movies.begin(), movies.end()); // Sortira po kraju (first)

int count = 0;
int current_time = 0;

for(auto m : movies) {
    if(m.second >= current_time) { // m.second je početak
        count++;
        current_time = m.first; // m.first je kraj
    }
}
cout << count << endl;
```

---

<!-- _class: title -->
# Stick Lengths (CSES)

## Medijan kao optimalna točka

---

# Analiza: Stick Lengths

**Problem:**
Imamo $n$ štapova duljina $p_1, p_2, \dots, p_n$.
Želimo ih sve skratiti ili produžiti na istu duljinu $x$.
Cijena promjene je $|p_i - x|$. Minimiziraj ukupnu cijenu $\sum |p_i - x|$.

### Intuicija
Tražimo broj $x$ koji minimizira sumu apsolutnih udaljenosti.
- Da je kvadratna udaljenost $(p_i - x)^2$, to bi bio prosjek (mean).
- Za apsolutnu udaljenost, to je **medijan**.

Ako sortiramo niz, medijan je element na sredini (`p[n/2]`).

---

# Implementacija: Stick Lengths

```cpp
int n; cin >> n;
vector<int> p(n);
for(int i=0; i<n; ++i) cin >> p[i];

sort(p.begin(), p.end());

int median = p[n / 2];
long long cost = 0;

for(int x : p) {
    cost += abs(x - median);
}

cout << cost << endl;
```
**Napomena:** Koristite `long long` za cijenu jer suma može biti velika!

---

<!-- _class: title -->
# Tasks and Deadlines (CSES)

## Minimizacija kazne

---

# Analiza: Tasks and Deadlines

**Problem:**
Imamo $n$ zadataka. Svaki traje $a_i$ i ima rok $d_i$.
Za svaki zadatak dobivamo nagradu $d_i - f_i$, gdje je $f_i$ vrijeme završetka.
Maksimiziraj ukupnu nagradu.

### Intuicija
Ukupna nagrada = $\sum (d_i - f_i) = \sum d_i - \sum f_i$.
$\sum d_i$ je konstanta (ne ovisi o redoslijedu).
Da bismo maksimizirali izraz, moramo **minimizirati $\sum f_i$** (sumu vremena završetaka).

Suma završetaka je minimalna ako **kraće zadatke radimo prve**.
(Ako imamo zadatke trajanja 2 i 10: redoslijed 2, 10 daje završetke 2 i 12 (suma 14). Redoslijed 10, 2 daje 10 i 12 (suma 22)).

---

# Implementacija: Tasks and Deadlines

```cpp
int n; cin >> n;
vector<pair<int, int>> tasks(n);
for(int i=0; i<n; ++i) cin >> tasks[i].first >> tasks[i].second; // {trajanje, rok}

sort(tasks.begin(), tasks.end()); // Sortiraj po trajanju

long long current_time = 0;
long long reward = 0;

for(auto t : tasks) {
    current_time += t.first;
    reward += (t.second - current_time);
}

cout << reward << endl;
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepno slaganje i Multiset

---

# Analiza: Towers

**Problem:**
Imamo $n$ kocaka različitih veličina koje dolaze jedna po jedna.
Kocku možemo staviti na vrh postojećeg tornja ako je manja od trenutne vršne kocke. Inače započinjemo novi toranj.
Minimiziraj broj tornjeva.

### Intuicija
Kad dođe kocka veličine $X$, na koji toranj je staviti?
Želimo "potrošiti" toranj čiji je vrh **najmanji mogući, ali veći od $X$**.
Zašto? Da bismo veće vrhove sačuvali za veće kocke koje možda dođu kasnije.

Koristimo `multiset` za praćenje vrhova svih tornjeva. Za $X$ tražimo `upper_bound(X)`.

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for(int i=0; i<n; ++i) {
    int x; cin >> x;
    
    // Nađi najmanji vrh koji je strogo veći od x
    auto it = towers.upper_bound(x);
    
    if(it == towers.end()) {
        // Nema takvog tornja, moramo napraviti novi
        towers.insert(x);
    } else {
        // Proširujemo postojeći toranj
        // Mičemo stari vrh i stavljamo novi (x)
        towers.erase(it);
        towers.insert(x);
    }
}
cout << towers.size() << endl;
```

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Pohlepni pristup:**
   - Donošenje lokalno optimalnih odluka u nadi da ćemo doći do globalnog optimuma.
   - Brzo i jednostavno, ali ne radi uvijek (npr. Coin problem s čudnim kovanicama).

2. **Ključni algoritmi:**
   - **Activity Selection:** Uvijek biraj događaj koji **najranije završava**.
   - **Huffmanovo kodiranje:** Spajaj dva čvora s najmanjom frekvencijom (koristeći `priority_queue`).

3. **Kada koristiti?**
   - Kad problem ima **svojstvo pohlepnog izbora** i **optimalnu podstrukturu**.

---

# Savjeti za rješavanje zadataka

- **Sortiranje je često prvi korak:**
  - Većina pohlepnih algoritama zahtijeva sortiran ulaz (po cijeni, težini, vremenu kraja...).
- **Pokušaj smisliti kontraprimjer:**
  - Prije kodiranja, probaj naći mali testni slučaj gdje tvoja ideja pada u vodu.
- **Ako pohlepno ne radi:**
  - Vjerojatno trebaš **Dinamičko programiranje** (DP).
