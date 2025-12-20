---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Podijeli pa vladaj i binarno pretraživanje"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- _class: title -->

# Podijeli pa vladaj i binarno pretraživanje

# Divide and Conquer, Binary Search, BS on Answer

---

# Sadržaj

1. **Uvod i Motivacija**
   - Princip "Podijeli pa vladaj"
   - Binarno pretraživanje
   - Binarno pretraživanje po rješenju
2. **Primjeri Zadataka**
   - Maksimalni zbroj podniza (D&C)
   - Pronalaženje fiksne točke
   - Agresivne krave (BS on Answer)
3. **Zadaci za vježbu**

---

# Princip "Podijeli pa Vladaj" (Divide & Conquer)

Moćna paradigma koja rješava problem u tri koraka:

1. **Podijeli (Divide):** Razbij problem na manje podprobleme istog tipa.
2. **Vladaj (Conquer):** Riješi podprobleme rekurzivno (ili direktno ako su mali).
3. **Kombiniraj (Combine):** Spoji rješenja podproblema u konačno rješenje.

**Primjeri:**
- **Merge Sort:** Podijeli na pola, sortiraj polovice, spoji sortirane nizove ($O(N \log N)$).
- **Binarno pretraživanje:** Specijalni slučaj gdje rješavamo samo jedan podproblem.

---

# Binarno Pretraživanje

Traženje elementa u **sortiranom** nizu.

1. **Podijeli:** Nađi sredinu (`mid`).
2. **Vladaj:**
   - Ako je `arr[mid] == target` $\to$ Kraj.
   - Ako je `arr[mid] > target` $\to$ Traži lijevo.
   - Ako je `arr[mid] < target` $\to$ Traži desno.
3. **Kombiniraj:** Nema (rezultat podproblema je rezultat cijelog problema).

**Složenost:** **$O(\log N)$**.
Svakim korakom odbacujemo polovicu prostora pretrage.

---

# Binarno Pretraživanje po Rješenju (BS on Answer)

Jedna od najkorisnijih tehnika u natjecateljskom programiranju.
Koristi se za **optimizacijske probleme** (minimizacija/maksimizacija).

**Ideja:**
Umjesto traženja optimalnog $X$, pitamo se:
> *"Je li moguće postići rješenje s vrijednošću $X$?"*

**Uvjet:** Problem mora biti **monoton**.
- Ako je moguće za $X$, moguće je i za sve manje od $X$ (ili veće, ovisno o problemu).
- To nam omogućuje binarnu pretragu po mogućim vrijednostima rješenja.

---

# Problem 1: Maksimalni zbroj podniza

**Zadatak:** Nađi podniz s najvećim zbrojem.
*(Znamo Kadaneov algoritam $O(N)$, ali riješimo ovo s D&C pristupom).*

**Strategija ($O(N \log N)$):**
Maksimalni podniz se nalazi ili:

1. Potpuno u **lijevoj** polovici.
2. Potpuno u **desnoj** polovici.
3. **Prelazi preko sredine** (dio lijevo + dio desno).

Rješenje je `max(Lijevo, Desno, Crossing)`.

---

# Max Subarray Sum: Kod

```cpp
long long maxCrossingSum(const vector<int>& arr, int l, int m, int r) {
    long long sum = 0, left_sum = -1e18;
    for (int i = m; i >= l; i--) { // Od sredine nalijevo
        sum += arr[i];
        if (sum > left_sum) left_sum = sum;
    }
    sum = 0; long long right_sum = -1e18;
    for (int i = m + 1; i <= r; i++) { // Od sredine nadesno
        sum += arr[i];
        if (sum > right_sum) right_sum = sum;
    }
    return left_sum + right_sum;
}

long long maxSubarraySum(const vector<int>& arr, int l, int r) {
    if (l == r) return arr[l];
    int m = l + (r - l) / 2;
    return max({
        maxSubarraySum(arr, l, m),
        maxSubarraySum(arr, m + 1, r),
        maxCrossingSum(arr, l, m, r)
    });
}
```

---

# Problem 2: Fiksna točka

**Zadatak:** Zadan je sortiran niz različitih cijelih brojeva. Nađi indeks $i$ takav da $A[i] = i$.

**Analiza:**
Definirajmo $B[i] = A[i] - i$. Tražimo $i$ takav da $B[i] = 0$.
Kako su elementi $A$ različiti cijeli brojevi i sortirani, niz $A$ raste barem za 1 u svakom koraku.
$\implies B$ je **monotono neopadajući**.
Možemo koristiti binarno pretraživanje na $B$ (implicitno).

---

# Fiksna točka: Implementacija

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for(int &x : a) cin >> x;

    int l = 0, r = n - 1, ans = -1;
    
    while (l <= r) {
        int mid = l + (r - l) / 2;
        
        if (a[mid] == mid) {
            ans = mid;
            break; // Našli smo!
        } else if (a[mid] > mid) {
            // Vrijednost je prevelika, mora biti lijevo
            // (jer indeks raste sporije od vrijednosti)
            r = mid - 1;
        } else {
            // Vrijednost premala, mora biti desno
            l = mid + 1;
        }
    }
    cout << ans << endl;
}
```

---

# Problem 3: Agresivne krave (Aggressive Cows)

**Zadatak:** Imamo $N$ štala na pozicijama $x_1, \dots, x_N$ i $C$ krava.
Rasporedi krave u štale tako da je **minimalna udaljenost** između bilo koje dvije krave **maksimalna**.

**Pristup (BS on Answer):**
Umjesto traženja udaljenosti, pitamo se:
> *"Mogu li smjestiti $C$ krava tako da je razmak barem $D$?"*

Ako mogu s razmakom $D$, probaj veći. Ako ne mogu, probaj manji.

---

# Provjera rješenja (Greedy Check)

Funkcija `check(d)` vraća `true` ako možemo postaviti krave s razmakom $\ge d$.

```cpp
bool check(long long d, int c, const vector<int>& stalls) {
    int cows_placed = 1;
    int last_pos = stalls[0]; // Prvu kravu uvijek stavimo u prvu štalu

    for (size_t i = 1; i < stalls.size(); ++i) {
        if (stalls[i] - last_pos >= d) {
            cows_placed++;
            last_pos = stalls[i];
            if (cows_placed == c) return true;
        }
    }
    return false;
}
```

*Napomena: Štale moraju biti sortirane!*

---

# Agresivne krave: Main Loop

```cpp
int main() {
    int n, c; cin >> n >> c;
    vector<int> stalls(n);
    for (int i = 0; i < n; ++i) cin >> stalls[i];
    
    sort(stalls.begin(), stalls.end()); // Obavezno sortiranje

    long long l = 0, r = 1e9, ans = 0;
    
    while (l <= r) {
        long long mid = l + (r - l) / 2;
        
        if (check(mid, c, stalls)) {
            ans = mid;  // Ovo je moguće rješenje, spremi ga
            l = mid + 1; // Pokušaj naći veće
        } else {
            r = mid - 1; // Razmak je prevelik, smanji
        }
    }
    cout << ans << '\n';
}
```

Složenost: $O(N \log (\text{max\_dist}))$.

---

# Zadaci za vježbu

## CSES Problem Set

1. **Sum of Two Values:** Nađi dva broja koja daju zbroj $X$ (Sort + Binary Search ili Two Pointers).
2. **Factory Machines:** Min vrijeme za proizvodnju $K$ proizvoda (BS on Answer).
3. **Towers:** Slaganje tornjeva (Upper bound / Multiset).

## Codeforces

* Pretraži tagove: `binary search`, `divide and conquer`.
- Zadaci težine 800-1200 za početak.

---

<!-- _class: title -->
# Sum of Two Values (CSES)

## Two Pointers ili Binary Search

---

# Analiza: Sum of Two Values

**Problem:**
Zadan je niz od $n$ cijelih brojeva i ciljni zbroj $x$.
Pronađi **indekse** dva broja čiji je zbroj točno $x$.

### Pristup 1: Sortiranje + Binarno pretraživanje
1. Spremimo parove `{vrijednost, originalni_indeks}`.
2. Sortiramo niz.
3. Za svaki element $a$, tražimo $x - a$ u ostatku niza koristeći binarno pretraživanje.
**Složenost:** $O(N \log N)$.

### Pristup 2: Two Pointers (Dva pokazivača)
1. Sortiramo niz.
2. Postavimo $L=0, R=N-1$.
3. Ako je $A[L] + A[R] < x \implies L++$.
4. Ako je $A[L] + A[R] > x \implies R--$.

---

# Implementacija: Sum of Two Values

```cpp
int n, target; cin >> n >> target;
vector<pair<int, int>> a(n);
for(int i=0; i<n; ++i) {
    cin >> a[i].first;
    a[i].second = i + 1; // 1-based indeksiranje
}
sort(a.begin(), a.end());

int l = 0, r = n - 1;
while(l < r) {
    int sum = a[l].first + a[r].first;
    if(sum == target) {
        cout << a[l].second << " " << a[r].second << endl;
        return 0;
    }
    if(sum < target) l++;
    else r--;
}
cout << "IMPOSSIBLE" << endl;
```

---

<!-- _class: title -->
# Factory Machines (CSES)

## Binarno pretraživanje po rješenju

---

# Analiza: Factory Machines

**Problem:**
Imamo $n$ strojeva. Stroj $i$ treba $k_i$ sekundi za jedan proizvod.
Koliko je minimalno vremena potrebno za proizvodnju $t$ proizvoda?

### Intuicija (BS on Answer)
Ako možemo proizvesti $t$ proizvoda u vremenu $T$, možemo i u vremenu $T+1$.
Funkcija "mogu li proizvesti" je monotona.

**Check funkcija:**
Za zadano vrijeme `time`, stroj $i$ proizvede $\lfloor \text{time} / k_i \rfloor$ proizvoda.
Ukupno proizvoda = $\sum \lfloor \text{time} / k_i \rfloor$.
Paziti na overflow (suma može preći $t$, limitiramo je).

---

# Implementacija: Factory Machines

```cpp
long long n, t; cin >> n >> t;
vector<long long> k(n);
for(int i=0; i<n; ++i) cin >> k[i];

long long l = 0, r = 1e18, ans = 1e18; // 1e18 je sigurna gornja granica

while(l <= r) {
    long long mid = l + (r - l) / 2;
    long long products = 0;
    for(long long x : k) {
        products += mid / x;
        if(products >= t) break; // Optimizacija i zaštita od overflowa
    }

    if(products >= t) {
        ans = mid;
        r = mid - 1;
    } else {
        l = mid + 1;
    }
}
cout << ans << endl;
```

---

<!-- _class: title -->
# Towers (CSES)

## Pohlepni pristup s Multisetom

---

# Analiza: Towers

**Problem:**
Kocke dolaze jedna po jedna. Kocku veličine $X$ možemo staviti na vrh postojećeg tornja ako je vrh tog tornja **strogo veći** od $X$.
Inače započinjemo novi toranj. Minimiziraj broj tornjeva.

### Intuicija
Pohlepno: Kocku $X$ stavi na toranj čiji je vrh **najmanji mogući, ali veći od $X$**.
Zašto? Čuvamo velike vrhove za velike kocke koje dolaze kasnije.
Trebamo strukturu koja podržava:
1. Nađi najmanji element $> X$.
2. Obriši ga i ubaci $X$.

Koristimo `std::multiset` i `upper_bound`.

---

# Implementacija: Towers

```cpp
int n; cin >> n;
multiset<int> towers;

for(int i=0; i<n; ++i) {
    int x; cin >> x;
    
    // upper_bound vraća iterator na prvi element strogo veći od x
    auto it = towers.upper_bound(x);
    
    if(it == towers.end()) {
        // Nema većeg elementa -> novi toranj
        towers.insert(x);
    } else {
        // Našli smo toranj -> zamijeni vrh
        towers.erase(it);
        towers.insert(x);
    }
}
cout << towers.size() << endl;
```

---

<!-- _class: lead -->

# Pitanja?

Sljedeća lekcija: Uvod u dinamičko programiranje
