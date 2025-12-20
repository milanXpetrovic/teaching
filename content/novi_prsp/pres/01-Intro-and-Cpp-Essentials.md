---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Uvod i C++ osnove"
footer: "Programiranje za rješavanje složenih problema | Vježbe 2025/26"
---

<!-- paginate: false -->
<!-- _class: title  -->
# Uvod i C++ osnove

Programiranje za rješavanje složenih problema

---

# O kolegiju

**Cilj:** Razviti vještine rješavanja algoritamskih problema.

**Fokus:**

- Efikasnost (vremenska i prostorna složenost).
- Poznavanje struktura podataka i algoritama.
- Implementacija u C++.

**Platforme koje koristimo:**

- **CSES Problem Set:** Standardni problemi za učenje.
- **Codeforces:** Natjecanja i raznovrsni zadaci.

---

# Zašto C++?

U natjecateljskom programiranju C++ je standard zbog:

1. **Brzine:** Kompajlirani jezik, vrlo brz izvršni kod.
2. **STL (Standard Template Library):** Bogata biblioteka algoritama (sortiranje, pretraživanje) i struktura podataka (vektori, mape, skupovi).
3. **Kontrole:** Mogućnost upravljanja memorijom (iako rijetko potrebno na ovoj razini).

---

# Preporučena literatura

- **Competitive Programmer's Handbook (CPH):**
  - Poglavlje 1: *Introduction*
  - Poglavlje 2: *Time complexity*
- **C++ Reference (cppreference.com):**
  - Dokumentacija za STL.

---

<!-- _class: title -->

# Osnove C++

---

# Template za rješavanje zadataka

Većina rješenja počinje ovim predloškom:

```cpp
#include <bits/stdc++.h> // Uključuje sve standardne biblioteke
using namespace std;

int main() {
    // Optimizacija ulaza/izlaza
    ios::sync_with_stdio(0);
    cin.tie(0);

    // Rješenje ide ovdje
    int n;
    cin >> n;
    cout << n << "\n";

    return 0;
}
```

---

# Ulaz i izlaz (I/O)

Standardni `cin` i `cout` mogu biti spori.

**Ključne optimizacije:**

1. `ios::sync_with_stdio(0);` - Isključuje sinkronizaciju s C-stilom I/O.
2. `cin.tie(0);` - Odvaja `cin` od `cout` (ne flusha se buffer prije svakog unosa).
3. Koristite `\n` umjesto `endl`.
   - `endl` forsira ispis (flush), što je sporo u petljama.

---

# Tipovi podataka

Pazite na opsege varijabli!

- **`int`**: 32-bitni, do $\approx 2 \cdot 10^9$.
- **`long long`**: 64-bitni, do $\approx 9 \cdot 10^{18}$.
  - *Pravilo:* Ako rezultat može preći 2 milijarde, koristite `long long`.
- **`double`**: Decimalni brojevi.
  - *Oprez:* Greške u preciznosti. Za usporedbu koristite epsilon: `abs(a-b) < 1e-9`.

---

<!-- _class: lead -->

# Standard Template Library (STL)

## Vektori i ostali kontejneri

---

# Vector (Dinamičko polje)

Najčešće korištena struktura.

```cpp
vector<int> v;
v.push_back(3);  // [3]
v.push_back(5);  // [3, 5]
v.push_back(2);  // [3, 5, 2]

// Iteracija
for (int x : v) {
    cout << x << " ";

// Sortiranje
sort(v.begin(), v.end()); // [2, 3, 5]
}
```

---

# String

C++ `string` je moćan i fleksibilan.

```cpp
string s = "algoritmi";
string sub = s.substr(0, 4); // "algo"

s += " su super"; // Konkatenacija

// Čitanje cijele linije
string line;
getline(cin, line);
```

---

# Set i Map

**Set (`set<T>`)**: Skup jedinstvenih elemenata.

- Operacije `insert`, `find`, `erase` su $O(\log N)$.

**Map (`map<K, V>`)**: Ključ-vrijednost parovi, sortirano po ključu.

- Pristup: `m["kljuc"] = vrijednost`. Složenost $O(\log N)$.

**Unordered varijante (`unordered_set`, `unordered_map`)**:

- Koriste hashiranje. Prosječno $O(1)$, ali u najgorem slučaju $O(N)$.
- Ne čuvaju poredak.

---

<!-- _class: lead -->

# Složenost algoritama

## Big O notacija

---

# Procjena složenosti

Koliko operacija računalo može izvesti u 1 sekundi?
$\approx 10^8$ (100 milijuna).

**Vodič za vrijeme 1s:**

| N (veličina ulaza) | Očekivana složenost | Primjer algoritma |
| :--- | :--- | :--- |
| $N \le 10$ | $O(N!)$ | Permutacije |
| $N \le 20$ | $O(2^N)$ | Podskupovi (bitmask) |
| $N \le 10^5$ | $O(N \log N)$ | Sortiranje, Set/Map |
| $N \le 10^6$ | $O(N)$ | Linearna pretraga, Two pointers |
| $N \le 10^{18}$ | $O(\log N)$ ili $O(1)$ | Binarno pretraživanje, Math |

---

<!-- _class: lead -->

# Zadaci za vježbu

## CSES Problem Set

- **[Weird Algorithm](https://cses.fi/problemset/task/1068)**
  - Simulacija procesa, `long long`.
- **[Missing Number](https://cses.fi/problemset/task/1083)**
  - Matematika (suma niza) ili XOR ili boolean polje.
- **[Repetitions](https://cses.fi/problemset/task/1069)**
  - Linearni prolaz kroz string.

---

<!-- _class: title -->

# Weird Algorithm (CSES)

## Analiza i rješenje

---

# Analiza zadatka: Weird Algorithm

**Problem:**
Počinjemo s brojem $n$.

- Ako je $n$ paran, $n = n / 2$.
- Ako je $n$ neparan, $n = 3n + 1$.
Ponavljamo dok $n$ ne postane 1. Ispisati sekvencu.

**Ograničenja:**
$1 \le n \le 10^6$.

**Zamka:**
Iako je $n$ mali, vrijednost može narasti iznad granice `int` (2 milijarde) tijekom procesa.
Npr. $n$ raste s $3n+1$.
$\rightarrow$ Moramo koristiti **`long long`**.

---

# Implementacija: Weird Algorithm

```cpp
#include <iostream>
using namespace std;

int main() {
    long long n; // Ključno: long long
    cin >> n;

    while (true) {
        cout << n << " ";
        if (n == 1) break;
        
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n = n * 3 + 1;
        }
    }
    cout << "\n";
    return 0;
}
```

---

# Sažetak

1. **Postavite okolinu:** Koristite template za brzi I/O.
2. **Pazite na tipove:** `long long` spašava stvar.
3. **Upoznajte STL:** `vector`, `sort`, `string` su vaši najbolji prijatelji.
4. **Analizirajte složenost:** Prije kodiranja provjerite hoće li rješenje proći vremensko ograničenje.

---

<!-- _class: title -->

# Rješavanje zadataka na Codeforcesu

---

# Kako rješavati zadatke na Codeforcesu?

1. **Pročitaj zadatak:** Pažljivo pročitaj tekst, ograničenja i primjere.
2. **Analiziraj:** Razmisli o rubnim slučajevima i algoritmu.
3. **Implementiraj:** Napiši kod u svom editoru (VS Code, CLion...).
4. **Testiraj:** Provjeri radi li kod na primjerima iz zadatka.
5. **Predaj (Submit):**
   - Odaberi jezik (npr. GNU C++17 ili C++20).
   - Zalijepi kod ili uploadaj datoteku.
   - Čekaj presudu (Verdict).

---

# Presude (Verdicts)

- **Accepted (AC):** Rješenje je točno!
- **Wrong Answer (WA):** Rješenje daje krivi izlaz na nekom testnom primjeru.
- **Time Limit Exceeded (TLE):** Rješenje je presporo.
- **Compilation Error (CE):** Kod se ne može kompajlirati.
- **Runtime Error (RE):** Greška tijekom izvođenja (npr. dijeljenje s nulom, pristup izvan niza).

---

<!-- _class: title -->

# Watermelon (Codeforces 4A)

## Analiza i rješenje

---

# Analiza zadatka: Watermelon

**Problem:**
Pete i Billy su kupili lubenicu težine $w$ kilograma. Žele je podijeliti na dva dijela tako da:

1. Svaki dio ima **parnu** težinu (2, 4, 6...).
2. Dijelovi ne moraju biti jednaki.

**Pitanje:**
Je li moguće podijeliti lubenicu na takav način? Ispisati "YES" ili "NO".

**Ulaz:**
Jedan cijeli broj $w$ ($1 \le w \le 100$).

---

# Razmišljanje o rješenju

Tražimo dva parna broja $a$ i $b$ takva da je $a + b = w$.

- Zbroj dva parna broja je uvijek **paran**.
  - $2k + 2m = 2(k+m)$.
- Dakle, prvi uvjet je da $w$ mora biti **paran**.
  - Ako je $w$ neparan (npr. 3, 5), odgovor je odmah "NO".

Je li svaki paran broj rješenje?

- $w=4 \rightarrow 2 + 2$ (OK)
- $w=8 \rightarrow 4 + 4$ ili $2 + 6$ (OK)

---

# Rubni slučajevi (Edge Cases)

Što je s najmanjim parnim brojem?

- **$w = 2$**

Možemo li 2 podijeliti na dva parna dijela?

- Jedina podjela je $1 + 1$.
- 1 nije paran broj.
- Dakle, za $w=2$ odgovor je **"NO"**.

**Zaključak:**
Odgovor je "YES" ako je $w$ paran i $w > 2$. U suprotnom "NO".

---

# Implementacija: Watermelon

```cpp
#include <iostream>
using namespace std;

int main() {
    int w;
    cin >> w;

    // Provjera uvjeta: paran i veći od 2
    if (w % 2 == 0 && w > 2) {
        cout << "YES" << endl;
    } else {
        cout << "NO" << endl;
    }

    return 0;
}
```

---

# Kako predati rješenje?

1. Otvorite [Codeforces Problem 4A](https://codeforces.com/problemset/problem/4/A).
2. Klik na gumb **Submit** (u izborniku ili desno).
3. Zalijepi gornji kod.
4. Odaberite **GNU C++17** (ili noviji).
5. Klik **Submit**.

Ako je sve u redu, vidjeti ćeš zeleni tekst **Accepted**.
