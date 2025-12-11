---
nav_exclude: true
---

# Tjedan 14: Algoritmi za Stringove i Računalna Geometrija

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Dva Svijeta Problema](#dva-svijeta-problema)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Algoritmi za Stringove](#algoritmi-za-stringove)
    * [Problem 1: Heširanje Stringova (String Hashing)](#problem-1-heširanje-stringova-string-hashing)
    * [Problem 2: Knuth-Morris-Pratt (KMP) algoritam](#problem-2-knuth-morris-pratt-kmp-algoritam)
    * [Problem 3: Trie (Prefiksno Stablo)](#problem-3-trie-prefiksno-stablo)
3. [Računalna Geometrija](#računalna-geometrija)
    * [Oprez: Aritmetika s pomičnim zarezom](#oprez-aritmetika-s-pomičnim-zarezom)
    * [Osnovni Geometrijski Primitivi: Vektorski Produkt](#osnovni-geometrijski-primitivi-vektorski-produkt)
    * [Problem 4: Konveksna Ljuska (Convex Hull)](#problem-4-konveksna-ljuska-convex-hull)
4. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Dva Svijeta Problema
Ovaj tjedan pokrivamo dvije specijalizirane, ali iznimno važne grane algoritama.

1.  **Algoritmi za stringove:** Rad s tekstom je sveprisutan. Od pretraživanja uzoraka u tekstu (Ctrl+F) do bioinformatike (analiza DNA sekvenci), efikasni algoritmi za stringove su ključni. Dok naivni pristupi često imaju kvadratnu složenost, naučit ćemo tehnike koje rješavaju probleme u linearnom ili log-linearnom vremenu.

2.  **Računalna geometrija:** Problemi koji uključuju točke, linije i poligone u ravnini. Iako su vizualno intuitivni, implementacija može biti puna zamki, pogotovo zbog aritmetike s pomičnim zarezom i rubnih slučajeva (npr. kolinearnost). Ključ uspjeha je korištenje robusnih cjelobrojnih metoda gdje je to moguće.

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 26: *String algorithms*
    *   Poglavlja 29 & 30: *Geometry*, *Sweep line algorithms*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 32: *String Matching*
    *   Poglavlje 33: *Computational Geometry*

---

## Algoritmi za Stringove

### Problem 1: Heširanje Stringova (String Hashing)

**Zadatak:** Brzo provjeriti jesu li dva podstringa nekog velikog stringa jednaka.

**Intuicija:** Umjesto da uspoređujemo znak po znak (što može biti sporo), svakom stringu dodijelimo **brojčanu vrijednost (hash)**. Ako su dva stringa ista, njihovi heševi su također isti. Ako su heševi različiti, stringovi su sigurno različiti. Postoji mala vjerojatnost **kolizije** (različiti stringovi imaju isti hash), ali odabirom dobrih parametara možemo je učiniti zanemarivom.

**Metoda: Polinomijalni Rolling Hash**
String `s` duljine `n` možemo tretirati kao broj u bazi `p`:
`hash(s) = (s[0] * p^(n-1) + s[1] * p^(n-2) + ... + s[n-1]) % m`
gdje je `p` prost broj veći od veličine alfabeta (npr. 31 ili 53), a `m` je veliki prosti broj (npr. `10^9 + 7`).

**Trik:** Predračunavanjem prefiksnih heševa, možemo izračunati hash bilo kojeg podstringa `s[a..b]` u **O(1)** vremenu.

**Implementacija:**
```cpp
const int P = 31;
const int M = 1e9 + 7;
vector<long long> p_pow;
vector<long long> h;

void precompute_hashes(const string& s) {
    int n = s.length();
    p_pow.resize(n);
    h.resize(n + 1, 0);

    p_pow = 1;
    for (int i = 1; i < n; ++i) {
        p_pow[i] = (p_pow[i-1] * P) % M;
    }

    for (int i = 0; i < n; ++i) {
        h[i+1] = (h[i] + (s[i] - 'a' + 1) * p_pow[i]) % M;
    }
}

long long get_substring_hash(int a, int b) { // za s[a..b]
    long long raw_hash = (h[b+1] - h[a] + M) % M;
    // Trebamo pomnožiti s p^(-a) da normaliziramo
    // Ovdje koristimo modularni inverz
    // Ekvivalentno, u pretraživanju uzoraka, heš uzorka množimo s p^a
    return raw_hash;
}
```
**Složenost:** Predračunanje `O(n)`. Upit `O(1)` (ako imamo modularni inverz). Primjena u Rabin-Karp algoritmu za pretraživanje uzoraka je `O(n+m)`.

### Problem 2: Knuth-Morris-Pratt (KMP) algoritam

**Zadatak:** Pronađi sve pojave uzorka `P` u tekstu `T` u `O(n+m)` vremenu.

**Intuicija:** KMP je deterministički algoritam koji izbjegava heširanje. Kada dođe do nepodudaranja, umjesto da se vrati na početak uzorka, on koristi informacije o **granicama (borders)** uzorka kako bi "pametno" pomaknuo uzorak naprijed. Granica stringa je prefiks koji je ujedno i sufiks.

**Prefiks funkcija (`π`):** Ključ KMP-a. `π[i]` je duljina najduže prave granice (prefiks koji nije cijeli string) prefiksa `P[0..i]`.
**Primjer:** `P = "abacaba"`. `π` polje je `[0, 0, 1, 0, 1, 2, 3]`.
`π[6] = 3` jer je "aba" najduži pravi prefiks od "abacaba" koji je ujedno i sufiks.

**Algoritam:**
1.  Predračunaj `π` polje za uzorak `P` u `O(m)` vremenu.
2.  Pretražuj tekst `T` koristeći `π` polje za pametne pomake.

**Kod (samo `compute_prefix_function`):**
```cpp
vector<int> compute_prefix_function(const string& p) {
    int m = p.length();
    vector<int> pi(m);
    for (int i = 1, j = 0; i < m; i++) {
        while (j > 0 && p[i] != p[j]) {
            j = pi[j-1];
        }
        if (p[i] == p[j]) {
            j++;
        }
        pi[i] = j;
    }
    return pi;
}
```
**Složenost:** **O(n + m)**. Brži je u praksi od Rabin-Karpa za jednostruko pretraživanje jer nema overhead heširanja, i deterministički je.

### Problem 3: Trie (Prefiksno Stablo)

**Zadatak:** Pohrani skup stringova tako da se mogu efikasno pretraživati, posebno s obzirom na prefikse.

**Intuicija:** Trie je stablo gdje svaki brid predstavlja jedan znak. Put od korijena do nekog čvora predstavlja prefiks. Ako je čvor označen kao "kraj riječi", taj put predstavlja cijelu riječ iz skupa.

**Struktura:** Svaki čvor ima polje pokazivača (ili mapu) na svoju djecu, gdje svaki pokazivač odgovara jednom znaku iz alfabeta.

**Implementacija:**
```cpp
struct TrieNode {
    map<char, TrieNode*> children;
    bool is_end_of_word = false;
};

void insert(TrieNode* root, const string& word) {
    TrieNode* curr = root;
    for (char c : word) {
        if (curr->children.find(c) == curr->children.end()) {
            curr->children[c] = new TrieNode();
        }
        curr = curr->children[c];
    }
    curr->is_end_of_word = true;
}

bool search(TrieNode* root, const string& word) {
    TrieNode* curr = root;
    for (char c : word) {
        if (curr->children.find(c) == curr->children.end()) {
            return false;
        }
        curr = curr->children[c];
    }
    return curr != nullptr && curr->is_end_of_word;
}
```
**Složenost:** Umetanje i pretraživanje stringa duljine `L` je **O(L)**. Prostorna složenost ovisi o broju i duljini stringova.

---

## Računalna Geometrija

### Oprez: Aritmetika s pomičnim zarezom
Geometrijski problemi često uključuju realne koordinate. Korištenje `double` ili `long double` može dovesti do grešaka u zaokruživanju. Uvijek uspoređuj dva broja s pomičnim zarezom `a` i `b` s tolerancijom: `abs(a - b) < EPS`, gdje je `EPS` mala vrijednost (npr. `1e-9`). Kad god je moguće, koristi cjelobrojnu aritmetiku.

### Osnovni Geometrijski Primitivi: Vektorski Produkt
**Vektorski produkt (Cross Product)** je najvažniji alat u 2D geometriji. Za dva vektora `p1 = (x1, y1)` i `p2 = (x2, y2)`, njihov produkt je `x1*y2 - x2*y1`.
-   **Značenje:** Predznak produkta govori o **orijentaciji**.
    -   `p1 x p2 > 0`: `p2` je "lijevo" od `p1` (suprotno od kazaljke na satu).
    -   `p1 x p2 < 0`: `p2` je "desno" od `p1` (u smjeru kazaljke na satu).
    -   `p1 x p2 = 0`: `p1` i `p2` su kolinearni.

**Test orijentacije:** Za tri točke `p0`, `p1`, `p2`, produkt `(p1-p0) x (p2-p0)` nam govori je li skretanje od `p0->p1` do `p1->p2` lijevo, desno ili ravno.

### Problem 4: Konveksna Ljuska (Convex Hull)

**Zadatak:** Zadan je skup od `n` točaka u ravnini. Pronađi najmanji konveksni poligon koji sadrži sve točke.

**Intuicija:** Zamisli da su točke čavli na dasci. Konveksna ljuska je oblik koji bi napravila gumica nategnuta oko svih čavala.

#### Graham Scan Algoritam (O(n log n))
1.  **Pronađi "sidro":** Odaberi točku s najmanjom y-koordinatom (i najmanjom x-koordinatom u slučaju izjednačenja). Nazovimo je `p0`.
2.  **Sortiraj točke:** Sortiraj sve ostale točke po polarnom kutu u odnosu na `p0`. Za usporedbu kutova, koristi test orijentacije (vektorski produkt), ne stvarne kutove.
3.  **Izgradi ljusku:** Iteriraj kroz sortirane točke i održavaj stog `S` s kandidatima za vrhove ljuske. Za svaku novu točku `p_i`:
    *   Dok stog ima barem dva vrha i put od drugog vrha na stogu do vrha stoga i do `p_i` ne čini "lijevo skretanje", izbacuj vrh sa stoga.
    *   Stavi `p_i` na stog.

**Kod (skica):**
```cpp
// p0 - sidro
// točke p1...pn-1 sortirane po kutu oko p0
stack<Point> s;
s.push(p0);
s.push(p1);

for (int i = 2; i < n; ++i) {
    Point top = s.top(); s.pop();
    Point next_to_top = s.top();
    s.push(top);
    
    // cross_product(next_to_top -> top, top -> p[i])
    while (orientation(next_to_top, top, p[i]) != LEFT_TURN) {
        s.pop();
        // ažuriraj top i next_to_top
    }
    s.push(p[i]);
}
```
**Složenost:** **O(n log n)**, dominirano sortiranjem. Prolazak kroz točke je amortizirano O(n).

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

*   **String Matching:** Implementiraj KMP ili Rabin-Karp algoritam.
*   **Finding Borders:** Vježba za računanje prefiks funkcije (KMP).
*   **Word Combinations:** Problem koji se elegantno rješava kombinacijom DP-a i Tria (ili heširanja).
*   **Convex Hull:** Direktan zadatak za implementaciju Graham Scan-a.
*   **Point in Polygon:** Primjena geometrijskih primitiva. Zahtijeva provjeru je li točka unutar poligona.
*   **Line Segment Intersection:** Primjena testa orijentacije.

### Codeforces

*   **Password** (Problem 126B): Klasičan problem koji koristi svojstva KMP prefiks funkcije.
*   **Polygon** (naći zadatak s tim imenom, npr. 166B): Zadatak koji obično testira razumijevanje konveksnosti i geometrijskih primitiva.
*   **Points on Line** (Problem 251A): Problem koji kombinira geometrijsku intuiciju s tehnikom dva pokazivača ili binarnim pretraživanjem.
*   **Good Substrings** (Problem 271D): Kombinacija heširanja stringova i rada sa setovima za brojanje jedinstvenih podstringova.

### Sljedeća lekcija: []()
