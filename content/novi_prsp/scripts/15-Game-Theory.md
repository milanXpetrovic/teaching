---
nav_exclude: true
---

# Teorija igara

## Sadržaj

1. [Uvod u kombinatorne igre](#uvod-u-kombinatorne-igre)
2. [Pobjednička i gubitnička stanja](#pobjednička-i-gubitnička-stanja)
3. [Igra Nim](#igra-nim)
4. [Sprague-Grundy teorem](#sprague-grundy-teorem)
5. [Zadaci za vježbu](#zadaci-za-vježbu)

---

## Preporučena literatura: Teorija igara

* **CPH (Competitive Programmer's Handbook):**
  * **Poglavlje 25:** *Game theory* (Nim igra, teorija nepristranih igara, Sprague-Grundy teorem).

Doodatna literatura za proširiti znanje o teoriji igara:

* **Game Theory (Thomas S. Ferguson):**
  * Part I: *Impartial Games* (Odličan sveučilišni materijal dostupan online).
* **CP-Algorithms:**
  * Sekcija *Game Theory* (Games on arbitrary graphs, Sprague-Grundy).
* **Dodatno:**
  * *Winning Ways for your Mathematical Plays* (Berlekamp, Conway, Guy) – "Biblija" kombinatorne teorije igara.

---

## Uvod u kombinatorne igre

U natjecateljskom programiranju, teorija igara najčešće se bavi **nepristranim kombinatornim igrama** (Impartial Combinatorial Games). Takve igre imaju sljedeća svojstva:

* Igraju dva igrača (često ih zovemo Alice i Bob, ili Prvi i Drugi) koji izmjenjuju poteze.
* Stanje igre je potpuno poznato obojici igrača (nema skrivenih informacija, nema sreće/kockica).
* Potezi koji su na raspolaganju ovise isključivo o stanju igre, a ne o tome koji je igrač na redu (zato se zovu "nepristrane").
* Igra završava kada igrač ne može napraviti potez.
* **Normalna igra (Normal Play):** Igrač koji ne može napraviti potez **gubi** (tj. zadnji igrač koji je napravio potez pobjeđuje).

---

## Pobjednička i gubitnička stanja

Svako stanje igre može se klasificirati kao **pobjedničko (Winning - W)** ili **gubitničko (Losing - L)**.

* **Losing (L):** Stanje iz kojeg svi mogući potezi vode u pobjedničko stanje protivnika. (Također: završno stanje je L).
* **Winning (W):** Stanje iz kojeg postoji barem jedan potez koji vodi u gubitničko stanje protivnika.

Ova definicija je rekurzivna.

1. Stanje bez mogućih poteza je **L**.
2. Ako možemo doći do **L** stanja, trenutno stanje je **W**.
3. Ako svi potezi vode u **W** stanja, trenutno stanje je **L**.

### Primjer: Igra oduzimanja (Subtraction Game)

Imamo hrpu od $N$ žetona. U jednom potezu igrač može uzeti 1, 2 ili 3 žetona.

Analiza stanja:

* $N=0$: **L** (nema poteza)
* $N=1$: Mogu uzeti 1 $\to$ dolazim na 0 (L). Dakle $1$ je **W**.
* $N=2$: Mogu na 0 (L) ili 1 (W). Postoji put u L, dakle $2$ je **W**.
* $N=3$: Mogu na 0 (L), 1 (W), 2 (W). Postoji put u L, dakle $3$ je **W**.
* $N=4$: Mogu na 1 (W), 2 (W), 3 (W). Svi vode u W, dakle $4$ je **L**.

Uočavamo uzorak: Stanja su L ako je $N$ djeljiv s 4. Inače su W.
Općenito, ako se može uzeti $\{1, 2, \dots, k\}$ žetona, stanje je L ako $N \equiv 0 \pmod{k+1}$.

---

## Igra Nim

Nim je najpoznatija nepristrana igra koja služi kao temelj za rješavanje mnogih složenijih igara.

**Pravila:**

* Postoji $k$ hrpa žetona, veličina $x_1, x_2, \dots, x_k$.
* U svakom potezu igrač bira **jednu** hrpu i s nje uzima proizvoljan broj žetona (barem jedan, može i cijelu hrpu).
* Igrač koji uzme zadnji žeton pobjeđuje.

### Nim Suma

Stanje igre Nim određeno je **Nim sumom** (XOR sumom) veličina svih hrpa:
$$ S = x_1 \oplus x_2 \oplus \dots \oplus x_k $$

**Teorem:**

* Ako je $S = 0$, stanje je **Gubitničko (L)**.
* Ako je $S \neq 0$, stanje je **Pobjedničko (W)**.

**Strategija:**
Ako je $S \neq 0$, igrač uvijek može odabrati potez tako da nova Nim suma postane 0.
Ako je $S = 0$, bilo koji potez će promijeniti sumu u vrijednost različitu od 0.

### Primjer

Hrpe veličina 5, 7, 9.
$$ 5 \oplus 7 \oplus 9 = (101)_2 \oplus (111)_2 \oplus (1001)_2 $$
$$ 101 \oplus 111 = 010 $$
$$ 010 \oplus 1001 = 1011 = 11_{10} $$
Suma je $11 \neq 0$, dakle prvi igrač pobjeđuje. Mora napraviti potez koji mijenja sumu u 0.

---

## Sprague-Grundy teorem

Ovaj teorem nam omogućuje da **bilo koju** nepristranu igru pretvorimo u ekvivalentnu Nim hrpu.

### Mex funkcija

Za skup nenegativnih cijelih brojeva $S$, $\text{mex}(S)$ (Minimum Excluded value) je najmanji nenegativni cijeli broj koji **nije** u skupu $S$.
Primjeri:

* $\text{mex}(\{0, 1, 3\}) = 2$
* $\text{mex}(\{1, 2, 3\}) = 0$
* $\text{mex}(\emptyset) = 0$

### Grundyjev broj (Nim-vrijednost)

Svakom stanju igre možemo pridružiti **Grundyjev broj** $g(state)$.
$$ g(state) = \text{mex}(\{ g(next\_state) \mid next\_state \text{ je dostižan potezom} \}) $$

Ovo je zapravo generalizacija W/L stanja:

* $g(state) = 0$ odgovara **L** stanju.
* $g(state) > 0$ odgovara **W** stanju.

### Kompozicija igara

Ako se igra sastoji od nekoliko neovisnih pod-igara (npr. nekoliko hrpa u Nimu, ili nekoliko figura na ploči koje se ne ometaju), Grundyjev broj cijele igre je **XOR suma** Grundyjevih brojeva pod-igara.

$$ G_{total} = g(subgame_1) \oplus g(subgame_2) \oplus \dots \oplus g(subgame_k) $$

Ako je $G_{total} > 0$, prvi igrač pobjeđuje.

### Primjer primjene

Imamo jednu hrpu od $N$ žetona. Dozvoljeno je uzeti 2 ili 3 žetona.

* $g(0) = \text{mex}(\emptyset) = 0$
* $g(1) = \text{mex}(\emptyset) = 0$ (nema poteza)
* $g(2) = \text{mex}(\{g(0)\}) = \text{mex}(\{0\}) = 1$
* $g(3) = \text{mex}(\{g(1), g(0)\}) = \text{mex}(\{0, 0\}) = 1$
* $g(4) = \text{mex}(\{g(2), g(1)\}) = \text{mex}(\{1, 0\}) = 2$
* $g(5) = \text{mex}(\{g(3), g(2)\}) = \text{mex}(\{1, 1\}) = 0$
* ...

Ako imamo više takvih hrpa, izračunamo $g(N)$ za svaku i napravimo XOR sumu.

```cpp
int memo[MAXN];
int calculate_grundy(int n) {
    if (n == 0) return 0;
    if (memo[n] != -1) return memo[n];
    
    set<int> reachable_states;
    // Ovisno o pravilima igre dodajemo stanja
    if (n >= 2) reachable_states.insert(calculate_grundy(n-2));
    if (n >= 3) reachable_states.insert(calculate_grundy(n-3));
    
    int mex = 0;
    while (reachable_states.count(mex)) mex++;
    return memo[n] = mex;
}
```

---

## Zadaci za vježbu

### CSES Problem Set (Mathematics / Game Theory)

Većina ovih zadataka nalazi se u sekciji *Mathematics* na CSES-u.

* **[Nim Game I](https://cses.fi/problemset/task/1730):** Osnovni Nim (XOR suma).
* **[Nim Game II](https://cses.fi/problemset/task/1098):** Varijacija Nima. (Hint: modulo 4).
* **[Stair Game](https://cses.fi/problemset/task/1099):** Žetoni na stepenicama. Pomicanje žetona sa stepenice $i$ na $i-1$. (Hint: Pomiču se samo žetoni s neparnih pozicija).
* **[Stick Game](https://cses.fi/problemset/task/1729):** Klasična igra oduzimanja sa zadanim skupom dozvoljenih poteza. Rješava se pomoću W/L stanja (DP).
* **[Grundy's Game](https://cses.fi/problemset/task/2207):** Podjela hrpe na dvije nejednake hrpe. Primjena Sprague-Grundy teorema.
* **[Sprague-Grundy Theorem](https://cses.fi/problemset/task/2208):** Još jedan zadatak za vježbu teorema.

### Codeforces

* Potražite zadatke s tagom `games`. Često se pojavljuju u Div2 A/B (ad-hoc logika) ili Div2 D/E (Sprague-Grundy).

[Sljedeća lekcija: Upiti nad rasponima (Range queries)](../content/12-Range-Queries)
