---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Pohlepni algoritmi"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
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

| Dinamičko programiranje | Pohlepni algoritmi |
| :--- | :--- |
| Prvo rješava podprobleme, a zatim na temelju njih donosi odluku. | Prvo donosi odluku, a zatim rješava preostali podproblem. |
| Razmatra **sve** opcije. | Razmatra **samo jednu** (pohlepnu) opciju. |
| Sporije, ali uvijek točno. | Brže, ali ne radi uvijek. |

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

**Zadatak:** Treba pronaći minimalan broj novčića za iznos $N$ koristeći zadane denominacije.

**Pohlepna strategija:**
Uvijek uzimamo **najveći mogući novčić** koji nije veći od preostalog iznosa.

**Primjer (euro centi: 1, 2, 5, 10, 20, 50):** $N = 48$

1. Uzimamo 20 (ostaje 28)
2. Uzimamo 20 (ostaje 8)
3. Uzimamo 5 (ostaje 3)
4. Uzimamo 2 (ostaje 1)
5. Uzimamo 1 (ostaje 0)

**Rješenje:** 5 novčića. (Optimalno!)

---

# Kada pohlepni pristup NE radi?

Pohlepna strategija radi za "kanonske" sustave (euro, dolar), ali ne za sve.

**Kontraprimjer:**

- Kovanice: $\{1, 3, 4\}$
- Cilj: $6$

**Pohlepno:** $4 + 1 + 1$ $\rightarrow$ **3 novčića**.
**Optimalno:** $3 + 3$ $\rightarrow$ **2 novčića**.

**Zaključak:** Za općeniti skup kovanica moramo koristiti **dinamičko programiranje**.

---

<!-- _class: lead -->
# Raspoređivanje događaja

## Activity Selection Problem

---

# Problem: Activity Selection

**Zadatak:** Treba odabrati maksimalan broj događaja koji se ne preklapaju. Svaki događaj ima `start` i `end` vrijeme.

**Koja je ispravna pohlepna strategija?**

1. ~~Najkraći događaj?~~ (Ne, kratak može biti u sredini dva duga)
2. ~~Najraniji početak?~~ (Ne, jedan dugi može blokirati sve ostale)
3. **Najraniji završetak!**

**Intuicija:**
Odabirom događaja koji **najranije završava**, oslobađamo resurs što je prije moguće za ostale događaje.

---

# Algoritam

1. **Sortiramo** događaje po vremenu završetka.
2. Uzimamo prvi događaj.
3. Uzimamo sljedeći koji počinje **nakon** što je prethodni završio.

**Složenost:** $O(N \log N)$ zbog sortiranja.

---

# Implementacija: Activity Selection

```cpp
struct Event { int start, end; };

// Sortiramo po vremenu završetka
bool compareEvents(const Event& a, const Event& b) {
    return a.end < b.end;
}

sort(events.begin(), events.end(), compareEvents);

int ans = 1;
int last_end = events[0].end;

for (int i = 1; i < n; ++i) {
    if (events[i].start >= last_end) { // Ako se ne preklapa
        ans++;
        last_end = events[i].end;
    }
}
```

---

<!-- _class: lead -->
# Huffmanovo kodiranje

## Kompresija podataka

---

# Huffmanovo kodiranje

**Cilj:** Prikazati podatke koristeći što manje bitova (kompresija). Česti znakovi trebaju imati kraće kodove.
**Uvjet:** Kodovi moraju biti **prefiksni** (nijedan kod nije početak drugog).

**Pohlepna strategija:**
Gradimo stablo odozdo prema gore. U svakom koraku spajamo **dva čvora s najmanjom frekvencijom**.

**Alat:** Prioritetni red (`std::priority_queue`).

---

# Algoritam (Huffman)

1. Kreiramo list za svaki znak (težina = frekvencija).
2. Ubacimo sve u **min-heap**.
3. Dok u heapu ima više od 1 čvora:
   - Izvadimo dva najmanja: $A$ i $B$.
   - Kreiramo novi čvor $C$ s težinom $freq(A) + freq(B)$.
   - Postavimo $A$ i $B$ kao djecu od $C$.
   - Vratimo $C$ u heap.

**Rezultat:** Stablo gdje put lijevo znači `0`, a desno `1`.

---

# Implementacija: čvor i usporedba

```cpp
struct Node {
    char ch;
    int freq;
    Node *left = nullptr, *right = nullptr;
    Node(char c, int f) : ch(c), freq(f) {}
};

// Min-heap: čvor s manjom frekvencijom ima veći prioritet
struct Compare {
    bool operator()(Node* a, Node* b) {
        return a->freq > b->freq;
    }
};

priority_queue<Node*, vector<Node*>, Compare> minHeap;
```

---

# Implementacija: gradnja stabla

```cpp
// Inicijalizacija: za svaki znak ubacimo list u minHeap

while (minHeap.size() > 1) {
    // Uzimamo dva najmanja
    Node* a = minHeap.top(); minHeap.pop();
    Node* b = minHeap.top(); minHeap.pop();

    // Spajamo ih u novi čvor ('$' označava unutarnji čvor)
    Node* c = new Node('$', a->freq + b->freq);
    c->left = a;
    c->right = b;

    minHeap.push(c);
}
// minHeap.top() je korijen Huffmanovog stabla
```

**Složenost:** $O(N \log N)$, gdje je $N$ broj različitih znakova.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set

1. **[Movie Festival](https://cses.fi/problemset/task/1629)**
   - Klasičan *Activity Selection* problem. Sortiramo po kraju filma.
2. **[Stick Lengths](https://cses.fi/problemset/task/1074)**
   - Minimizacija sume razlika $|x - p_i|$. Optimalni $x$ je **medijan**.
3. **[Tasks and Deadlines](https://cses.fi/problemset/task/1630)**
   - Maksimizacija nagrade $= deadline - finish$.
   - *Hint:* Kraće zadatke obavljamo prve.
4. **[Towers](https://cses.fi/problemset/task/1073)**
   - Slaganje kocki jedne na drugu. Zahtijeva `multiset` za efikasno traženje "baze".

---

# Codeforces preporuke

Tražite zadatke s tagom `greedy` težine 800-1200.

- **[Hit the Lottery](https://codeforces.com/problemset/problem/996/A)**
  - Problem novčića s novčanicama 1, 5, 10, 20, 100 (kanonski sustav).
- **[Boats Competition](https://codeforces.com/problemset/problem/1399/C)**
  - Formiranje parova s istim zbrojem težina. Sortiranje + Two Pointers.

---

<!-- _class: title -->
# Movie Festival (CSES)

## Activity Selection u praksi

---

# Analiza: Movie Festival

**Problem:**
U kinu se prikazuje $n$ filmova. Svaki ima vrijeme početka i kraja.
Želimo pogledati **maksimalan broj filmova** u cijelosti (bez preklapanja).

**Intuicija:**
Ovo je identičan problem kao **Activity Selection**.
Pohlepna strategija: uvijek biramo film koji **najranije završava**, a da ne počinje prije nego što je prethodni završio.

Zašto? Time ostavljamo najviše vremena za ostale filmove.

---

# Implementacija: Movie Festival

```cpp
int n; cin >> n;
vector<pair<int, int>> movies(n);
for (int i = 0; i < n; ++i)
    cin >> movies[i].second >> movies[i].first; // Učitavamo kao {kraj, početak}

sort(movies.begin(), movies.end()); // Sortira po kraju (first)

int ans = 0;
int current_time = 0;

for (auto m : movies) {
    if (m.second >= current_time) { // m.second je početak
        ans++;
        current_time = m.first; // m.first je kraj
    }
}
cout << ans << "\n";
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
Cijena promjene je $|p_i - x|$. Treba minimizirati ukupnu cijenu $\sum |p_i - x|$.

**Intuicija:**
Tražimo broj $x$ koji minimizira sumu apsolutnih udaljenosti.

- Da je kvadratna udaljenost $(p_i - x)^2$, to bi bio prosjek (mean).
- Za apsolutnu udaljenost, to je **medijan**.

Ako sortiramo niz, medijan je element na sredini (`p[n/2]`).

---

# Implementacija: Stick Lengths

```cpp
int n; cin >> n;
vector<int> p(n);
for (int i = 0; i < n; ++i) cin >> p[i];

sort(p.begin(), p.end());

int median = p[n / 2];
long long cost = 0;

for (int x : p) {
    cost += abs(x - median);
}

cout << cost << "\n";
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
Treba maksimizirati ukupnu nagradu.

**Intuicija:**
Ukupna nagrada = $\sum (d_i - f_i) = \sum d_i - \sum f_i$.
$\sum d_i$ je konstanta (ne ovisi o redoslijedu).
Da bismo maksimizirali izraz, moramo **minimizirati $\sum f_i$** (sumu vremena završetaka).

Suma završetaka je minimalna ako **kraće zadatke radimo prve**.
(Ako imamo zadatke trajanja 2 i 10: redoslijed 2, 10 daje završetke 2 i 12 (suma 14). Redoslijed 10, 2 daje 10 i 12 (suma 22).)

---

# Implementacija: Tasks and Deadlines

```cpp
int n; cin >> n;
vector<pair<int, int>> tasks(n);
for (int i = 0; i < n; ++i)
    cin >> tasks[i].first >> tasks[i].second; // {trajanje, rok}

sort(tasks.begin(), tasks.end()); // Sortiramo po trajanju

long long current_time = 0;
long long reward = 0;

for (auto t : tasks) {
    current_time += t.first;
    reward += (t.second - current_time);
}

cout << reward << "\n";
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepno slaganje i Multiset

---

# Analiza: Towers

**Problem:**
Imamo $n$ kocaka koje dolaze jedna po jedna (veličine se mogu ponavljati).
Kocku možemo staviti na vrh postojećeg tornja samo ako je **strogo manja** od trenutne vršne kocke. Inače započinjemo novi toranj.
Treba minimizirati broj tornjeva.

**Intuicija:**
Kad dođe kocka veličine $X$, na koji toranj je staviti?
Želimo "potrošiti" toranj čiji je vrh **najmanji mogući, ali strogo veći od $X$**.
Zašto? Da bismo veće vrhove sačuvali za veće kocke koje možda dođu kasnije.

Vrhove svih tornjeva pratimo u `multiset`-u i za $X$ tražimo `upper_bound(X)`.
Zbog strogog uvjeta koristimo `upper_bound`, a ne `lower_bound` (jednaku kocku ne smijemo staviti na vrh).

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for (int i = 0; i < n; ++i) {
    int x; cin >> x;

    // Najmanji vrh koji je strogo veći od x
    auto it = towers.upper_bound(x);

    if (it == towers.end()) {
        // Nema takvog tornja, radimo novi
        towers.insert(x);
    } else {
        // Proširujemo postojeći toranj:
        // mičemo stari vrh i stavljamo novi (x)
        towers.erase(it);
        towers.insert(x);
    }
}
cout << towers.size() << "\n";
```

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Pohlepni pristup:**
   - Donošenje lokalno optimalnih odluka u nadi da ćemo doći do globalnog optimuma.
   - Brzo i jednostavno, ali ne radi uvijek (npr. problem novčića s neobičnim kovanicama).

2. **Ključni algoritmi:**
   - **Activity Selection:** Uvijek biramo događaj koji **najranije završava**.
   - **Huffmanovo kodiranje:** Spajamo dva čvora s najmanjom frekvencijom (koristeći `priority_queue`).

3. **Kada koristiti?**
   - Kad problem ima **svojstvo pohlepnog izbora** i **optimalnu podstrukturu**.

---

# Savjeti za rješavanje zadataka

- **Sortiranje je često prvi korak:**
  - Većina pohlepnih algoritama zahtijeva sortiran ulaz (po cijeni, težini, vremenu kraja...).
- **Pokušajte smisliti kontraprimjer:**
  - Prije kodiranja probajte naći mali testni slučaj na kojem vaša ideja pada.
- **Ako pohlepno ne radi:**
  - Vjerojatno trebate **dinamičko programiranje** (DP).