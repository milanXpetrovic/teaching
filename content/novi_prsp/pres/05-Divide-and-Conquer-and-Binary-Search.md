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

<!-- _class: lead -->

# Pitanja?

Sljedeća lekcija: Uvod u dinamičko programiranje

```
