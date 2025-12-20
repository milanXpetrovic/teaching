---
nav_exclude: true
---

# Osnove računalne geometrije

## Sadržaj
1. [Uvod i problemi s preciznošću](#uvod-i-problemi-s-preciznošću)
2. [Točke, Vektori i Vektorski produkt](#točke-vektori-i-vektorski-produkt)
3. [Presjek dužina](#presjek-dužina)
4. [Površina poligona](#površina-poligona)
5. [Konveksna ljuska (Convex Hull)](#konveksna-ljuska-convex-hull)
6. [Zadaci za vježbu](#zadaci-za-vježbu)

---

## Uvod i problemi s preciznošću

Računalna geometrija bavi se rješavanjem geometrijskih problema algoritamskim putem. Iako su formule često jednostavne, implementacija je puna zamki zbog **preciznosti**.

### Zlatno pravilo geometrije u natjecanjima:
**Izbjegavaj `double` i `float` kad god je to moguće!**

Koristi cjelobrojnu aritmetiku (`long long`) za koordinate. Mnogi problemi se mogu riješiti bez decimalnih brojeva sve do samog kraja. Ako baš moraš koristiti decimalne brojeve:
1.  Koristi `long double`.
2.  Nikada ne uspoređuj s `==` ili `!=`. Koristi mali epsilon ($\epsilon \approx 10^{-9}$).
    *   $a == b \implies |a - b| < \epsilon$
    *   $a < b \implies a < b - \epsilon$

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 29: *Geometry* (Odličan uvod u vektorski produkt i kompleksne brojeve).
    *   Poglavlje 30: *Sweep-line algorithms*.
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 33: *Computational Geometry*.
*   **CP-Algorithms:**
    *   Sekcija *Geometry* (Detaljni članci o osnovnim operacijama).

---

## Točke, Vektori i Vektorski produkt

Osnovni gradivni element je točka, koju često poistovjećujemo s vektorom od ishodišta $(0,0)$ do te točke.

```cpp
struct Point {
    long long x, y;
    
    // Operator oduzimanja za dobivanje vektora između dvije točke
    Point operator-(const Point& other) const {
        return {x - other.x, y - other.y};
    }
};
```

### Vektorski produkt (Cross Product)
Ovo je **najvažnija** operacija u 2D geometriji. Za dva vektora $\vec{a} = (x_1, y_1)$ i $\vec{b} = (x_2, y_2)$, vektorski produkt (u 2D smislu) je:

$$ \vec{a} \times \vec{b} = x_1 y_2 - x_2 y_1 $$

**Svojstva i primjena:**
1.  **Površina:** Apsolutna vrijednost produkta je površina paralelograma razapetog vektorima $\vec{a}$ i $\vec{b}$. (Površina trokuta je pola toga).
2.  **Orijentacija (CCW - Counter Clockwise):**
    Promatrajmo skretanje pri putovanju od točke $A$ do $B$, pa do $C$. Računamo produkt vektora $\vec{AB}$ i $\vec{BC}$ (ili $\vec{AC}$).
    Neka je $val = (B.x - A.x)(C.y - A.y) - (B.y - A.y)(C.x - A.x)$.
    *   **$val > 0$:** Skretanje ulijevo (**Counter-Clockwise**).
    *   **$val < 0$:** Skretanje udesno (**Clockwise**).
    *   **$val = 0$:** Točke su kolinearne (na istom pravcu).

```cpp
long long cross_product(Point a, Point b, Point c) {
    // Vraća CP vektora AB i AC
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}
```

---

## Presjek dužina

Jedan od klasičnih problema je provjeriti sijeku li se dvije dužine $AB$ i $CD$.
Problem je složeniji nego što se čini zbog rubnih slučajeva (kolinearnost).

**Opći slučaj:**
Dužine se sijeku ako i samo ako:
1.  Točke $C$ i $D$ leže na suprotnim stranama pravca $AB$.
2.  Točke $A$ i $B$ leže na suprotnim stranama pravca $CD$.

Ovo provjeravamo pomoću orijentacije (vektorskog produkta).

**Rubni slučaj (Kolinearnost):**
Ako su sve četiri točke na istom pravcu, dužine se sijeku ako se preklapaju (tj. ako je $x$-projekcija ili $y$-projekcija jedne dužine unutar druge).

---

## Površina poligona

Površina bilo kojeg jednostavnog poligona (ne presijeca sam sebe) s vrhovima $(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)$ može se izračunati pomoću **Shoelace formule** (Formule vezica):

$$ Area = \frac{1}{2} | \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i) | $$
*(Gdje je $(x_{n+1}, y_{n+1}) = (x_1, y_1)$)*.

Ovo je zapravo suma vektorskih produkata susjednih vrhova.

```cpp
long long area_2x(const vector<Point>& p) {
    long long area = 0;
    int n = p.size();
    for (int i = 0; i < n; i++) {
        area += (p[i].x * p[(i+1)%n].y - p[(i+1)%n].x * p[i].y);
    }
    return abs(area); // Vraća 2 * Površina (da ostanemo u integerima)
}
```
*Napomena: Pickov teorem povezuje površinu poligona s cjelobrojnim točkama na rubu i unutar poligona: $A = I + \frac{B}{2} - 1$.*

---

## Konveksna ljuska (Convex Hull)

Konveksna ljuska skupa točaka je najmanji konveksni poligon koji sadrži sve točke skupa (zamisli gumicu nategnutu oko čavala).

Standardni algoritam je **Monotone Chain (Andrew's Algorithm)** koji radi u $O(N \log N)$ (zbog sortiranja).

### Algoritam:
1.  Sortiraj točke po $x$-koordinati (pa po $y$).
2.  Izgradi **gornju ljusku**: Iteriraj kroz točke. Dok god zadnje tri točke čine skretanje ulijevo (ili ravno), izbaci srednju točku (jer nije dio ljuske, nego je unutra). Želimo samo skretanja udesno.
3.  Izgradi **donju ljusku**: Isto, ali tražimo skretanja ulijevo.
4.  Spoji ljuske.

```cpp
// Pomoćna funkcija za orijentaciju
long long cross_product(Point a, Point b, Point c) { ... }

vector<Point> convex_hull(vector<Point>& pts) {
    int n = pts.size(), k = 0;
    if (n <= 2) return pts;
    vector<Point> h(2 * n);

    sort(pts.begin(), pts.end(), [](Point a, Point b) {
        return a.x < b.x || (a.x == b.x && a.y < b.y);
    });

    // Donja ljuska
    for (int i = 0; i < n; ++i) {
        while (k >= 2 && cross_product(h[k-2], h[k-1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }

    // Gornja ljuska
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross_product(h[k-2], h[k-1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }

    h.resize(k - 1); // Zadnja točka je duplikat prve
    return h;
}
```

---

## Zadaci za vježbu

### CSES Problem Set (Geometry)
Ova sekcija na CSES-u je izvrsna za svladavanje osnova.

*   **[Point Location Test](https://cses.fi/problemset/task/2189):** Odredi s koje strane pravca se nalazi točka (Direktna primjena vektorskog produkta).
*   **[Line Segment Intersection](https://cses.fi/problemset/task/2190):** Provjeri sijeku li se dvije dužine (Pazi na kolinearne slučajeve!).
*   **[Polygon Area](https://cses.fi/problemset/task/2191):** Izračunaj površinu (Shoelace formula).
*   **[Point in Polygon](https://cses.fi/problemset/task/2192):** Je li točka unutar, van ili na rubu poligona? (Ray casting algoritam).
*   **[Convex Hull](https://cses.fi/problemset/task/2195):** Implementiraj Monotone Chain algoritam.

### Codeforces
*   Traži zadatke s tagom `geometry` i težinom 1200-1600.
*   **[Water Lily](https://codeforces.com/problemset/problem/1199/B):** Jednostavna geometrija (Pitagorin poučak).
*   **[New Year and Curling](https://codeforces.com/problemset/problem/908/C):** Presjek krugova i udaljenosti.

[Sljedeća lekcija: Završni savjeti i trikovi](../content/19-Final-Tips) *(Kraj gradiva)*