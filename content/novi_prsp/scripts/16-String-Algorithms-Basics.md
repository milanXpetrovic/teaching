---
nav_exclude: true

---

# Osnovni algoritmi za stringove

## Sadržaj

1. [Uvod i terminologija](#uvod-i-terminologija)
2. [Trie (Prefiksno stablo)](#trie-prefiksno-stablo)
3. [String Hashing (Polinomijalno raspršivanje)](#string-hashing-polinomijalno-raspršivanje)
4. [Z-Algoritam](#z-algoritam)
5. [Zadaci za vježbu](#zadaci-za-vježbu)

---

## Uvod i terminologija

Algoritmi za rad sa stringovima (nizovima znakova) ključni su u mnogim područjima računalne znanosti, od pretraživanja teksta do bioinformatike.

**Osnovni pojmovi:**

* **Prefiks:** Podniz koji počinje na početku stringa. Za string "ABCDE", prefiksi su "A", "AB", "ABC", ...
* **Sufiks:** Podniz koji završava na kraju stringa. Za string "ABCDE", sufiksi su "E", "DE", "CDE", ...
* **Podniz (Substring):** Bilo koji uzastopni niz znakova unutar stringa. "BCD" je podniz od "ABCDE".
* **Podniz (Subsequence):** Niz znakova koji se dobiva brisanjem nula ili više znakova iz originalnog stringa, zadržavajući redoslijed preostalih. "ACE" je podniz (subsequence) od "ABCDE", ali nije substring.

---

## Trie (Prefiksno stablo)

**Trie** (izgovara se kao "try") je stablasta struktura podataka koja se koristi za efikasno spremanje skupa stringova. Svaki čvor u stablu predstavlja prefiks nekog stringa iz skupa.

### Struktura

* Korijen stabla predstavlja prazan string.
* Svaki brid prema djetetu predstavlja jedan znak.
* Čvorovi mogu imati oznaku (npr. `is_end`) koja govori završava li neka riječ u tom čvoru.

### Operacije

* **Umetanje (Insert):** Krećemo od korijena i pratimo bridove koji odgovaraju znakovima riječi. Ako brid ne postoji, stvaramo novi čvor.
* **Pretraživanje (Search):** Slično umetanju, ali ako brid ne postoji, riječ nije u stablu.

**Složenost:** $O(L)$ za umetanje i pretraživanje, gdje je $L$ duljina riječi. Ovo je brže od $O(L \log N)$ koliko bi trebalo `std::set<string>` ili `std::map`.

### Implementacija

```cpp
struct TrieNode {
    TrieNode* children[26];
    bool is_end;

    TrieNode() {
        for (int i = 0; i < 26; i++) children[i] = nullptr;
        is_end = false;
    }
};

void insert(TrieNode* root, string s) {
    TrieNode* curr = root;
    for (char c : s) {
        int index = c - 'A'; // Pretpostavka: velika slova
        if (curr->children[index] == nullptr) {
            curr->children[index] = new TrieNode();
        }
        curr = curr->children[index];
    }
    curr->is_end = true;
}

bool search(TrieNode* root, string s) {
    TrieNode* curr = root;
    for (char c : s) {
        int index = c - 'A';
        if (curr->children[index] == nullptr) return false;
        curr = curr->children[index];
    }
    return curr->is_end;
}
```

---

## String Hashing (Polinomijalno raspršivanje)

Usporedba dva stringa duljine $N$ obično traje $O(N)$. Pomoću **hashiranja**, možemo uspoređivati stringove (ili njihove podnizove) u **O(1)** vremenu, uz malu vjerojatnost pogreške.

### Polinomijalni Rolling Hash

Ideja je svakom stringu pridružiti cijeli broj (hash) koristeći formulu:
$$ H(S) = (S[0] \cdot B^{n-1} + S[1] \cdot B^{n-2} + \dots + S[n-1] \cdot B^0) \pmod M $$

Gdje su:

* $B$: Baza (obično prost broj veći od broja mogućih znakova, npr. 31 ili 53 za mala/velika slova, 313 za sve ASCII).
* $M$: Modul (veliki prost broj, npr. $10^9 + 7$ ili $10^9 + 9$).

### Predračun (Preprocessing)

Da bismo mogli računati hash bilo kojeg podniza u $O(1)$, računamo:

1. **Potencije baze:** $P[i] = B^i \pmod M$.
2. **Prefiksne hasheve:** $H[i]$ je hash prefiksa duljine $i$.
    $$ H[i] = (H[i-1] \cdot B + S[i-1]) \pmod M $$

### Hash podniza

Hash podniza od indeksa $L$ do $R$ (0-indeksirano) računa se kao:
$$ Hash(L, R) = (H[R+1] - H[L] \cdot P[R-L+1]) \pmod M $$
*(Napomena: Ako je rezultat negativan, dodamo $M$).*

Ako dva podniza imaju isti hash, velika je vjerojatnost da su jednaki. Da bismo smanjili vjerojatnost kolizije, često koristimo **Double Hashing** (računamo dva hasha s različitim parovima $B$ i $M$).

---

## Z-Algoritam

Z-Algoritam se koristi za pretraživanje uzoraka (pattern matching).
Za string $S$, konstruiramo niz $Z$, gdje je $Z[i]$ duljina **najdužeg zajedničkog prefiksa** (LCP) između stringa $S$ i sufiksa koji počinje na $S[i]$.

* $Z[0]$ nije definiran (ili je duljina stringa).
* Ako je $Z[i] = k$, to znači da su $S[0 \dots k-1]$ i $S[i \dots i+k-1]$ jednaki.

**Složenost:** $O(N)$.

### Primjena: Pattern Matching

Ako želimo pronaći uzorak $P$ u tekstu $T$:

1. Konstruiramo string $S = P + \# + T$ (gdje je $\#$ znak koji se ne pojavljuje u tekstu).
2. Izračunamo Z-niz za $S$.
3. Gdje god je $Z[i]$ jednak duljini uzorka $|P|$, našli smo pojavljivanje uzorka u tekstu.

### Implementacija

```cpp
vector<int> z_function(string s) {
    int n = s.length();
    vector<int> z(n);
    // [l, r] je trenutni najdesniji segment koji se podudara s prefiksom
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r)
            z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]])
            ++z[i];
        if (i + z[i] - 1 > r)
            l = i, r = i + z[i] - 1;
    }
    return z;
}
```

---

## Zadaci za vježbu

### CSES Problem Set (String Algorithms)

* **[Word Combinations](https://cses.fi/problemset/task/1731):** Zadan je string i rječnik. Na koliko načina se string može sastaviti od riječi iz rječnika? (Trie + DP).
* **[String Matching](https://cses.fi/problemset/task/1753):** Broj pojavljivanja uzorka u tekstu. (KMP ili Z-Algoritam ili Hashing).
* **[Finding Borders](https://cses.fi/problemset/task/1732):** Pronađi sve duljine prefiksa koji su ujedno i sufiksi stringa. (Hashing ili KMP/Z).
* **[Minimal Rotation](https://cses.fi/problemset/task/1110):** Leksikografski najmanja rotacija stringa. (Hashing ili Booth's algoritam).

### Codeforces

* **[Double Profiles](https://codeforces.com/problemset/problem/154/C):** Primjena hashinga na grafovima/stringovima.
* **[Good Substrings](https://codeforces.com/problemset/problem/271/D):** Brojanje različitih podnizova s ograničenjima (Trie ili Hashing).

[Sljedeća lekcija: Napredni algoritmi za stringove (KMP, Aho-Corasick)](../content/17-Advanced-String-Algorithms) *(Opcionalno)*
