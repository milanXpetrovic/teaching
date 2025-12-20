---
nav_exclude: true
---

# Napredni algoritmi za stringove

## Sadržaj
1. [Uvod i Preporučena Literatura](#uvod-i-preporučena-literatura)
2. [KMP Algoritam (Knuth-Morris-Pratt)]( #kmp-algoritam-knuth-morris-pratt)
3. [Aho-Corasick Algoritam](#aho-corasick-algoritam)
4. [Sufiksni Niz (Suffix Array)](#sufiksni-niz-suffix-array)
5. [Zadaci za vježbu](#zadaci-za-vježbu)

---

## Uvod i Preporučena Literatura

Dok su *Hashing* i *Trie* moćni alati, postoje problemi koji zahtijevaju deterministička rješenja bez kolizija ili rješavanje specifičnih upita (poput brojanja različitih podnizova) u linearnom vremenu. Napredni algoritmi za stringove oslanjaju se na iskorištavanje unutarnje strukture stringa (ponavljanja, prefiksi, sufiksi).

### Preporučena Literatura

*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 26: *String Algorithms* (KMP, Z-algo, Suffix Structures).
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 32: *String Matching* (Detaljna teorija KMP-a).
*   **CP-Algorithms:**
    *   Sekcija *String Processing* (Izvrsni tutorijali za Suffix Automaton i Suffix Array).
*   **Stringology:** [Link](http://www.stringology.org/) (Zbirka algoritama).

---

## KMP Algoritam (Knuth-Morris-Pratt)

KMP algoritam rješava problem pronalaska uzorka $P$ u tekstu $T$ u vremenu $O(|T| + |P|)$. Srž algoritma je **prefiksna funkcija** (često označavana s $\pi$).

### Prefiksna funkcija ($\pi$)
Za dani string $S$, $\pi[i]$ je duljina najdužeg **pravog prefiksa** podniza $S[0 \dots i]$ koji je ujedno i **sufiks** tog istog podniza.

Primjer za $S = \text{"ABCAB"}$:
*   $\pi[0]$ ("A"): 0 (nema pravog prefiksa).
*   $\pi[1]$ ("AB"): 0.
*   $\pi[2]$ ("ABC"): 0.
*   $\pi[3]$ ("ABCA"): 1 (prefiks "A" je sufiks "A").
*   $\pi[4]$ ("ABCAB"): 2 (prefiks "AB" je sufiks "AB").

### Implementacija Prefiksne Funkcije

```cpp
vector<int> prefix_function(string s) {
    int n = s.length();
    vector<int> pi(n);
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j])
            j = pi[j-1];
        if (s[i] == s[j])
            j++;
        pi[i] = j;
    }
    return pi;
}
```

### Primjena: Pretraživanje uzorka
Da bismo našli pojavljivanja uzorka $P$ u tekstu $T$, stvorimo string $S = P + \# + T$ (gdje je $\#$ separator).
Izračunamo $\pi$ niz za $S$.
Gdje god je $\pi[i] == |P|$, to znači da sufiks duljine $|P|$ (koji je u dijelu teksta) odgovara prefiksu duljine $|P|$ (koji je naš uzorak).

---

## Aho-Corasick Algoritam

Aho-Corasick je generalizacija KMP algoritma za **više uzoraka**. Omogućuje nam da u jednom prolazu kroz tekst pronađemo pojavljivanja bilo kojeg uzorka iz skupa $\{P_1, P_2, \dots, P_k\}$.

### Struktura
Algoritam gradi **automat** (baziran na Trie strukturi) s dodatnim "failure links" (slično kao $\pi$ funkcija u KMP-u).
1.  Izgradi Trie od svih uzoraka.
2.  BFS-om izračunaj **failure link** za svaki čvor. Failure link čvora $u$ pokazuje na čvor $v$ koji predstavlja najduži mogući pravi sufiks stringa predstavljenog čvorom $u$, a koji je također prefiks nekog uzorka u Trie-u.

### Primjena
*   Pretraživanje virusa (potpisa) u datotekama.
*   Rješavanje problema tipa "koji se od rječničkih riječi pojavljuju u tekstu".

**Složenost:** Linearna u odnosu na duljinu teksta i sumu duljina svih uzoraka.

---

## Sufiksni Niz (Suffix Array)

Sufiksni niz je moćna struktura koja sadrži **indekse svih sufiksa** stringa, **sortirane leksikografski**.

Primjer za $S = \text{"banana"}$:
Sufiksi:
0: banana
1: anana
2: nana
3: ana
4: na
5: a

Sortirani sufiksi:
5: a
3: ana
1: anana
0: banana
4: na
2: nana

Sufiksni niz: `[5, 3, 1, 0, 4, 2]`

### Izgradnja
Naivno sortiranje traje $O(N^2 \log N)$. Standardni pristup u natjecateljskom programiranju koristi sortiranje parova cikličkih pomaka u vremenu **$O(N \log N)$** ili **$O(N \log^2 N)$**.

### LCP Niz (Longest Common Prefix)
Uz sufiksni niz, često računamo **LCP niz**.
`LCP[i]` je duljina najdužeg zajedničkog prefiksa između sufiksa na poziciji $SA[i]$ i $SA[i-1]$ u sortiranom poretku.

Pomoću Kasaijevog algoritma, LCP niz se gradi u $O(N)$.

### Primjene
1.  **Broj različitih podnizova:** $\frac{N(N+1)}{2} - \sum LCP[i]$.
2.  **Najduži ponavljajući podniz:** Maksimalna vrijednost u LCP nizu.
3.  **Traženje uzorka:** Binarno pretraživanje po sufiksnom nizu.

---

## Zadaci za vježbu

### CSES Problem Set (String Algorithms)
*   **[String Matching](https://cses.fi/problemset/task/1753):** Klasična primjena KMP algoritma.
*   **[Finding Borders](https://cses.fi/problemset/task/1732):** Granica (border) je prefiks koji je ujedno i sufiks. Ovo je direktna primjena $\pi$ funkcije (iteriranje: $j = \pi[N-1], \pi[j-1] \dots$).
*   **[Word Combinations](https://cses.fi/problemset/task/1731):** Može se riješiti pomoću Trie + DP ili Aho-Corasick.
*   **[Longest Palindrome](https://cses.fi/problemset/task/1111):** Manacherov algoritam (specijaliziran za palindrome) ili String Hashing.
*   **[Distinct Substrings](https://cses.fi/problemset/task/2103):** Klasičan zadatak za Suffix Array + LCP ili Suffix Automaton.

### Codeforces
*   **[Password](https://codeforces.com/problemset/problem/126/B):** KMP zadatak. Traži se podniz koji je prefiks, sufiks i pojavljuje se u sredini.
*   **[MUH and Cube Walls](https://codeforces.com/problemset/problem/471/D):** KMP na razlikama susjednih elemenata.
*   **[Entropy](https://codeforces.com/problemset/problem/452/E):** Napredan zadatak koji zahtijeva Suffix Array/Automaton za brojanje pojavljivanja u više stringova.

[Sljedeća lekcija: Računalna geometrija](../content/18-Geometry) *(Opcionalno)*