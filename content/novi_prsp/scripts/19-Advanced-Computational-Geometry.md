---
nav_exclude: true
---

# Napredna računalna geometrija

## Sadržaj

1. [Uvod i Preporučena Literatura](#uvod-i-preporučena-literatura)
2. [Pickov Teorem (Polygon Lattice Points)](#pickov-teorem-polygon-lattice-points)
3. [Rotirajuća čeljust (Rotating Calipers)](#rotirajuća-čeljust-rotating-calipers)
4. [Najbliži par točaka (Closest Pair of Points)](#najbliži-par-točaka-closest-pair-of-points)
5. [Sweep-line algoritmi](#sweep-line-algoritmi)
6. [Zadaci za vježbu](#zadaci-za-vježbu)

---

## Uvod i Preporučena Literatura

U osnovama geometrije naučili smo raditi s vektorima i poligonima u $O(N)$ ili $O(N^2)$. Napredna geometrija fokusira se na efikasnost. Često kombiniramo geometriju s drugim strukturama podataka (poput `std::set` ili Segmentnog stabla) ili koristimo paradigmu "Podijeli pa vladaj".

### Preporučena Literatura

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 29: *Geometry* (Pickov teorem).
  * Poglavlje 30: *Sweep-line algorithms* (Presjek dužina, Najbliži par).
* **CP-Algorithms:**
  * Sekcija *Geometry* (Pick's Theorem, Rotating Calipers).
* **Computational Geometry: Algorithms and Applications (de Berg et al.):** Standardni udžbenik za dublje razumijevanje (npr. Voronoi dijagrami, Delaunay triangulacija).

---

## Pickov Teorem (Polygon Lattice Points)

Pickov teorem povezuje površinu poligona s brojem cjelobrojnih točaka (točaka s cjelobrojnim koordinatama) koje se nalaze na njegovom rubu i u njegovoj unutrašnjosti.

Vrijedi za **jednostavne poligone** (ne sijeku sami sebe) čiji su vrhovi na cjelobrojnim koordinatama.

$$ Area = I + \frac{B}{2} - 1 $$

Gdje su:

* $Area$: Površina poligona (izračunata Shoelace formulom).
* $I$ (Interior): Broj cjelobrojnih točaka strogo **unutar** poligona.
* $B$ (Boundary): Broj cjelobrojnih točaka na **rubu** (stranicama) poligona.

### Kako izračunati $B$?

Broj cjelobrojnih točaka na dužini između $(x_1, y_1)$ i $(x_2, y_2)$ jednak je:
$$ \text{points} = \gcd(|x_1 - x_2|, |y_1 - y_2|) $$
*(Napomena: Ovo uključuje jednu krajnju točku, ali ne i drugu, pa jednostavnim zbrajanjem po svim stranicama dobivamo točan $B$).*

### Primjena

Često se traži broj točaka unutar poligona ($I$). Iz formule slijedi:
$$ I = Area - \frac{B}{2} + 1 $$

---

## Rotirajuća čeljust (Rotating Calipers)

Nakon što izračunamo **konveksnu ljusku** skupa točaka, često želimo izračunati **promjer** skupa (najveću udaljenost između bilo koje dvije točke).
Naivni pristup usporedbe svih parova traje $O(N^2)$. Pomoću tehnike **Rotirajuće čeljusti**, to možemo učiniti u **$O(N)$**.

### Intuicija

Zamislimo dvije paralelne pravce (čeljusti) koje dodiruju poligon s suprotnih strana. Rotiramo te pravce oko poligona dok ne obiđemo cijeli krug.
Maksimalna udaljenost može se dogoditi samo između parova točaka koje dodiruju te paralelne pravce (antipodalne točke).

### Algoritam

1. Izračunaj konveksnu ljusku.
2. Nađi točku s najmanjom $y$ koordinatom ($p_{min}$) i najvećom $y$ koordinatom ($p_{max}$).
3. Rotiraj "čeljusti":
    * U svakom koraku promatramo bridove na obje strane ljuske.
    * Koristimo **vektorski produkt** da odredimo koji kut je manji (tj. koji brid će se prvi "priljubiti" uz čeljust).
    * Pomakni čeljust na taj brid i izračunaj udaljenost između novih antipodalnih parova.

Osim promjera, ova tehnika rješava:

* Širinu poligona.
* Minimalni pravokutnik koji opisuje poligon.
* Maksimalnu udaljenost između dva konveksna poligona.

---

## Najbliži par točaka (Closest Pair of Points)

Zadan je skup od $N$ točaka. Pronađi par s najmanjom Euklidskom udaljenosti.
Naivno: $O(N^2)$.
Optimizirano: **$O(N \log N)$** koristeći "Podijeli pa vladaj".

### Divide & Conquer pristup

1. **Sortiraj** točke po $x$-koordinati.
2. **Podijeli:** Podijeli skup na lijevu ($S_L$) i desnu ($S_R$) polovicu vertikalnom linijom $x = x_{mid}$.
3. **Vladaj:** Rekurzivno nađi najmanju udaljenost u $S_L$ ($d_L$) i $S_R$ ($d_R$). Neka je $d = \min(d_L, d_R)$.
4. **Kombiniraj:** Provjeri postoji li par točaka gdje je jedna u $S_L$, a druga u $S_R$, a njihova udaljenost je manja od $d$.
    * Promatramo samo točke koje su unutar trake širine $d$ oko središnje linije ($|x_i - x_{mid}| < d$).
    * Te točke sortiramo po $y$-koordinati.
    * Za svaku točku u traci, dovoljno je provjeriti sljedećih **7 točaka** (geometrijski dokazano) u sortiranom poretku. Ako je razlika u $y$ veća od $d$, prekidamo petlju.

```cpp
// Pseudokod dijela za spajanje (Combine)
double d = min(solve(left_half), solve(right_half));
vector<Point> strip;
for (Point p : points) {
    if (abs(p.x - mid_x) < d) strip.push_back(p);
}
sort(strip_by_y);

for (int i = 0; i < strip.size(); ++i) {
    for (int j = i + 1; j < strip.size(); ++j) {
        if (strip[j].y - strip[i].y >= d) break; // Optimizacija
        d = min(d, dist(strip[i], strip[j]));
    }
}
return d;
```

---

## Sweep-line algoritmi

Tehnika "bršuće ravnine" (Sweep-line) zamišlja vertikalnu liniju koja putuje s lijeva na desno preko ravnine i procesuira "događaje" (Events).

### Primjer: Presjek dužina

Zadano je $N$ dužina. Ima li sjecišta?

1. **Događaji:** Početak dužine, kraj dužine, sjecište (ako ga tražimo). Sortiramo točke po $x$.
2. **Stanje (Sweep-line status):** Uređena struktura (npr. `std::set` ili `Treap`) koja sadrži aktivne dužine sortirane po $y$-koordinati na trenutnoj poziciji sweep-linea.
3. **Proces:**
    * Kada naiđemo na lijevi kraj dužine: Ubacimo je u set. Provjerimo sječe li se s neposrednim susjedima u setu (iznad i ispod).
    * Kada naiđemo na desni kraj dužine: Izbacimo je iz seta. Provjerimo sijeku li se sada njezini bivši susjedi (koji postaju novi susjedi).

Složenost: $O(N \log N)$ za detekciju, ili $O((N+K) \log N)$ za ispis svih $K$ sjecišta.

---

## Zadaci za vježbu

### CSES Problem Set (Geometry)

* **[Polygon Lattice Points](https://cses.fi/problemset/task/2193):** Direktna primjena Pickovog teorema. (Pazi na `gcd` za rubne točke).
* **[Minimum Euclidean Distance](https://cses.fi/problemset/task/2194):** Najbliži par točaka. Zahtijeva $O(N \log N)$ implementaciju.
* **[Convex Hull](https://cses.fi/problemset/task/2195):** Iako smo ga radili u osnovama, ovdje je preduvjet za Rotating Calipers.

### Codeforces & Ostalo

* **[Robert Hood (CF 280B)](https://codeforces.com/problemset/problem/633/C):** Traženje najudaljenijeg para točaka (Rotating Calipers). Iako se zadatak zove drugačije, često se koristi kao primjer.
* **[Area of Union of Rectangles](https://cses.fi/problemset/task/1741):** Iako na CSES-u, ovo je klasičan Sweep-line zadatak uz pomoć Segmentnog stabla.

[Povratak na sadržaj](../)
