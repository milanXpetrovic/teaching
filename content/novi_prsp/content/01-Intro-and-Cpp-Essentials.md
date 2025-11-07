---
nav_exclude: true
layout: default
parent: PRSP
nav_order: 1
has_toc: true
---

# Uvod i osnove

## Pregled

Dobro došli na kolegij "Programiranje za rješavanje složenih problema"! Ovaj tjedan postavit ćemo temelje za ostatak semestra. Naš cilj je razumjeti što je natjecateljsko programiranje, zašto je C++ dominantan jezik u tom području te kako postaviti brzo i efikasno okruženje. Također ćemo ponoviti i usvojiti ključne C++ konstrukte i strukture podataka iz Standardne Biblioteke Predložaka (STL) koje su neophodne za rješavanje problema.

Na ovom kolegiju dotičemo se i natjecateljskog programiranja. Natjecateljsko programiranje je misaoni sport u kojem sudionici rješavaju algoritamske probleme unutar zadanih vremenskih i memorijskih ograničenja. Rješavanje problema sastoji se od dva ključna dijela:

1. **Dizajn algoritma:** Analiza problema, prepoznavanje poznatih struktura i osmišljavanje rješenja koje je **točno** i **efikasno**.
2. **Implementacija algoritma:** Pisanje čistog, sažetog i ispravnog koda koji uspješno prolazi sve testne primjere unutar zadanih resursa.

Za razliku od tradicionalnog softverskog inženjerstva, programi su obično kratki (do stotinjak linija koda), ne zahtijevaju dugoročno održavanje, a fokus je na performansama i brzini implementacije.

## C++ kao jezik izbora

Iako se problemi mogu rješavati u raznim jezicima (Python, Java), C++ je daleko najpopularniji izbor u natjecateljskom programiranju iz nekoliko razloga:

* **Performanse:** C++ je izuzetno brz jezik, što je ključno kada se programi izvršavaju na velikim ulaznim podacima unutar strogih vremenskih ograničenja (obično 1-2 sekunde).
* **Standardna Biblioteka Predložaka (STL):** C++ nudi moćnu biblioteku gotovih struktura podataka (poput dinamičkih polja, skupova, mapa) i algoritama (sortiranje, pretraživanje) koje drastično ubrzavaju implementaciju.
* **Kontrola nad memorijom:** Omogućuje precizno upravljanje memorijom, što je važno za probleme s ograničenom memorijom.

## Postavljanje efikasnog C++ okruženja

### Kompajler

Koristit ćemo `g++` kompajler, koji je standard na većini natjecateljskih platformi. Na Windowsima se može instalirati putem MinGW-a ili WSL-a (Windows Subsystem for Linux). Na Linuxu i macOS-u je obično već dostupan.

### Osnovni predložak (template)

Većina natjecatelja koristi osnovni predložak koda kako bi ubrzali pisanje. Naš početni predložak izgledat će ovako:

```cpp
// g++ -o solution.cpp ./s 
// alias gpp='g++ -o ./s solution.cpp'

// #include <iostream>
// #include <vector>
// #include <string>
// #include <algorithm>

// Često se koristi i <bits/stdc++.h> koji uključuje sve standardne biblioteke,
// ali je dostupan samo na g++ kompajleru. Zbog praktičnosti, koristit ćemo ga.
// #include <bits/stdc++.h>

#include <bits/stdc++.h>
using namespace std;

const int INF = INT_MAX;
int main(){
    freopen("ulaz.txt", "r", stdin);
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // RJESENJE ZADATKA
}
```

### Kompajliranje koda

Kod kompajliramo koristeći naredbu u terminalu:

```g++ -std=c++11 -O2 -Wall solution.cpp -o solution```

* `-std=c++17`: Koristi C++17 standard (ili neki noviji).
* `-O2`: Optimizira kod za brzinu.
* `-Wall`: Prikazuje sva upozorenja, što je korisno za otkrivanje potencijalnih grešaka.
* `-o solution`: Ime izvršne datoteke.

Naravno — evo uređene i proširene verzije u **Markdown** formatu, spremne da ubaciš u skriptu za studente:

---

#### Korištenje aliasa za brže kompajliranje

Kod natjecateljskog programiranja ili učestalog testiranja koda, praktično je definirati **alias** – prečac koji zamjenjuje dužu naredbu za kompajliranje.

Umjesto da svaki put pišemo:

```bash
g++ -std=c++17 -O2 -Wall solution.cpp -o s
```

možemo definirati `alias` u terminalu:

```bash
alias gpp='g++ -std=c++17 -O2 -Wall solution.cpp -o solution'
```

Nakon što se alias definira, dovoljno je jednostavno pokrenuti:

```bash
gpp
```

što će automatski kompajlirati `solution.cpp` u izvršnu datoteku `s`, koju zatim pokrećemo s:

```bash
./solution
```

**Univerzalniji alias:**

Ako često mijenjate ime datoteke, možete napraviti fleksibilniji alias koji prima argumente:

```bash
alias gpp='g++ -std=c++17 -O2 -Wall -o s'
```

Tada kompajlirate bilo koju datoteku ovako:

```bash
gpp main.cpp
```

ili

```bash
gpp zadatak1.cpp
```

---

## Osnove ulaza i izlaza (I/O)

### Brzi I/O

Standardni `cin` i `cout` mogu biti spori. Na početku `main` funkcije uvijek dodajte sljedeće linije za ubrzanje:

```cpp
ios_base::sync_with_stdio(false);
cin.tie(NULL);
```

Također, umjesto `endl` koristite `'\n'` za ispis novog reda, jer `endl` dodatno prazni buffer, što usporava program.

### Čitanje ulaza

Uobičajeni način čitanja podataka:

```cpp
int a, b;
string s;
cin >> a >> b >> s; // Čita npr. "10 20 rijec"
```

Za čitanje cijele linije, uključujući razmake:

```cpp
string line;
getline(cin, line);
```

Za čitanje dok god ima ulaza:

```cpp
int x;
while (cin >> x) {
    // obrada varijable x
}
```

### Rad s datotekama

Za probleme gdje je ulaz/izlaz u datotekama (npr. `input.txt`, `output.txt`), možete preusmjeriti standardne streamove:

```cpp
freopen("input.txt", "r", stdin);
freopen("output.txt", "w", stdout);
```

Ove linije stavite na početak `main` funkcije, a ostatak koda pišete kao da koristite standardni ulaz i izlaz.

## Osnovne strukture podataka (STL)

STL je vaš najvažniji alat. A u nastavku su navedene osnove.

### `vector` (Dinamičko polje)

`vector` je dinamičko polje koje automatski mijenja veličinu.

```cpp
vector<int> v;
v.push_back(5); // Dodaje element na kraj:
v.push_back(2); //

cout << v; // Ispisuje 5

// Iteracija kroz vektor
for (int x : v) {
    cout << x << " ";
}
cout << '\n';

// Veličina vektora
cout << v.size() << '\n'; // Ispisuje 2
```

### `string`

`string` je sličan `vector<char>`, ali s dodatnim funkcionalnostima.

```cpp
string a = "test";
string b = "iranje";
string s = a + b; // s = "testiranje"
cout << s.substr(2, 4); // Ispisuje "stir" (podstring od indeksa 2, duljine 4)
```

### `pair` i `tuple`

`pair` sprema dva elementa (mogu biti različitih tipova), a `tuple` sprema proizvoljan broj elemenata.

```cpp
pair<int, string> p = {1, "rijec"};
cout << p.first << " " << p.second << '\n'; // 1 rijec

tuple<int, char, double> t = {5, 'a', 3.14};
cout << get<0>(t) << '\n'; // 5
```

### `sort` algoritam

Funkcija `sort` sortira elemente u rasponu. Za `vector` se koristi ovako:

```cpp
vector<int> v = {4, 2, 5, 3, 5, 8, 3};
sort(v.begin(), v.end()); // Sortira cijeli vektor
// v sada sadrži
```

Za obično C-style polje:

```cpp
int arr[] = {4, 2, 5, 3, 5, 8, 3};
int n = 7;
sort(arr, arr + n);
```

## Vježbe i zadaci

1. **Postavite svoje okruženje:** Instalirajte g++ kompajler i odaberite editor (npr. VS Code s C++ ekstenzijama). Napravite svoj osnovni predložak koda.
2. **Jednostavan ulaz/izlaz:** Riješite zadatak koji zahtijeva čitanje nekoliko brojeva i stringova, izvođenje jednostavne matematičke operacije i ispis rezultata.
3. **Sortiranje parova:** Napišite program koji čita `n` parova brojeva, sortira ih primarno po prvom elementu, a sekundarno po drugom, te ispisuje sortirane parove.
4. **Manipulacija stringovima:** Riješite zadatak koji zahtijeva čitanje stringa, pronalaženje podstringa i ispis rezultata.
5. **Vježba na online platformi:** Riješite nekoliko jednostavnih implementacijskih zadataka na platformi poput Codeforces ili CSES kako biste se navikli na format zadataka.
    * [Codeforces: Watermelon](https://codeforces.com/problemset/problem/4/A)
    * [CSES: Weird Algorithm](https://cses.fi/problemset/task/1068)
    * [Codeforces: Way Too Long Words](https://codeforces.com/problemset/problem/71/A)

---
