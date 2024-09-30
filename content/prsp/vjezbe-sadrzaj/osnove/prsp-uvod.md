---
layout: default
parent: PRSP
nav_order: 1
---

# Uvod

## Registracija na stranicama Codeforces, CSES i GitHub

U ovom kolegiju bavit ćemo se rješavanjem algoritamskih problema koristeći različite online platforme koje omogućuju evaluaciju vaših rješenja. Dvije od najčešće korištenih platformi su **Codeforces** i **CSES**. Također, preporučuje se da napravite račun na **GitHubu** kako biste mogli pohranjivati i dijeliti svoja rješenja. Prije nego što krenemo s rješavanjem problema, potrebno je kreirati račune na ovim platformama.

## Registracija na GitHub

**GitHub** je popularna platforma za verzioniranje koda koja omogućuje pohranu vaših projekata, suradnju s drugima i dijeljenje rješenja. Da biste otvorili svoj račun na GitHubu, slijedite ove korake:

1. Otvorite web stranicu [GitHub](https://github.com/).
2. U gornjem desnom kutu kliknite na **Sign up**.
3. Ispunite tražene podatke (korisničko ime, e-mail adresu, lozinku) i slijedite upute za dovršetak registracije.
4. Potvrdite svoju registraciju putem e-maila koji ćete dobiti.

Nakon uspješne registracije, provjerite da se možete prijaviti na svoj račun te istražite razne značajke koje GitHub nudi, uključujući mogućnost izrade repozitorija za pohranu vaših rješenja.

## Registracija na Codeforces

**Codeforces** je jedna od najpopularnijih platformi za natjecateljsko programiranje koja nudi široku bazu problema te redovito organizira natjecanja. Pratite sljedeće korake kako biste otvorili svoj račun:

1. Otvorite web stranicu [Codeforces](https://codeforces.com/).
2. U gornjem desnom kutu kliknite na **Register**.
3. Ispunite tražene podatke (korisničko ime, lozinku, e-mail adresu) i kliknite na **Register**.
4. Potvrdite registraciju putem e-maila koji ćete dobiti.

Nakon uspješne registracije, provjerite da se možete prijaviti na svoj račun te istražite različite opcije i zadatke koje platforma nudi.

## Registracija na CSES

**CSES** je zbirka algoritamskih problema s naglaskom na klasične algoritamske izazove, a posebno je korisna za učenje osnova. Za pristup zadacima na CSES platformi, slijedite ove korake:

1. Otvorite web stranicu [CSES Problem Set](https://cses.fi/problemset/).
2. Kliknite na **Login/Register** u gornjem desnom kutu.
3. Ispunite potrebne informacije (korisničko ime, lozinku, e-mail adresu) i kliknite na **Register**.
4. Potvrdite svoju registraciju putem e-maila.

## Input i Output u C++

U rješavanju algoritamskih problema, najčešći zadatak je pročitati ulazne podatke, obraditi ih i ispisati rezultat. U C++ jeziku za to koristimo standardne biblioteke za ulaz i izlaz podataka.

### Ulaz

Za čitanje podataka s konzole koristimo **`cin`** (standard input). Na natjecanjima ulazne podatke obično čitamo izravno iz standardnog ulaza, i to na sljedeći način:

```cpp
int a, b;
cin >> a >> b;
```

Ovaj kod će čitati dva cijela broja (integers) unesena od strane korisnika.

Ako imate više vrijednosti za čitanje, one su obično razdvojene razmacima ili prelaskom u novi redak. Primjer:

```cpp
int n;
cin >> n; // Čitanje jednog broja

for (int i = 0; i < n; ++i) {
    int x;
    cin >> x; // Čitanje sljedećih n brojeva
}
```

### Izlaz

Za ispis rezultata na konzolu koristimo `cout` (standard output). Rezultati se ispisuju na sljedeći način:

```cpp
int sum = a + b;
cout << sum << endl;
```

Ovdje cout ispisuje zbroj varijabli `a` i `b`, a `endl` označava prelazak u novi redak.

### Primjer s ulazom i izlazom

Evo primjera jednostavnog zadatka koji čita dva broja i ispisuje njihov zbroj:

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
```

Ovaj kod prima dva cijela broja s ulaza, izračunava njihov zbroj i ispisuje rezultat na izlaz.

Pomoću ovih osnovnih principa za unos i ispis podataka, možete rješavati većinu zadataka s platformi poput Codeforces i CSES.

## Primjer: Zadatak 1

Potrebno je s pomoću `for` petlji kreirajte zadani uzorak:

```text
1 
1 2 
1 2 3 
1 2 3 4 
```

**Input:** Visina piramide $n$ $$(1 <= n <= 15)$$

### Primjer

**Input:**

```text
5
```

**Output:**

```text
1 
1 2 
1 2 3 
1 2 3 4 
1 2 3 4 5
```

## Zadaci za vježbu

- [Codeforces: Watermelon](https://codeforces.com/problemset/problem/4/A)
- [CSES: Weird Algorithm](https://cses.fi/problemset/task/1068)
- [Codeforces: Way Too Long Words](https://codeforces.com/problemset/problem/71/A)

[Sljedeća lekcija: Vremenska složenost](../vremenska-slozenost){: .btn .btn-purple .float-right}
