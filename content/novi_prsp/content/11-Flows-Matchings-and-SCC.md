---
---

# Tjedan 11: Mrežni Tokovi, Uparivanja i Jake Komponente

## Sadržaj
1.  [Uvod i Motivacija](#uvod-i-motivacija)
    *   [Protok materijala, podataka i resursa](#protok-materijala-podataka-i-resursa)
    *   [Problem uparivanja i dodjele](#problem-uparivanja-i-dodjele)
    *   [Struktura usmjerenih grafova: Jake komponente](#struktura-usmjerenih-grafova-jake-komponente)
    *   [Preporučena Literatura](#preporučena-literatura)
2.  [Maksimalni Tok (Maximum Flow)](#maksimalni-tok-maximum-flow)
    *   [Definicija Mrežnog Toka i Reidualnog Grafa](#definicija-mrežnog-toka-i-reidualnog-grafa)
    *   [Ford-Fulkerson Metoda i Povećavajući Putevi](#ford-fulkerson-metoda-i-povećavajući-putevi)
    *   [Edmonds-Karp Algoritam (BFS pristup)](#edmonds-karp-algoritam-bfs-pristup)
    *   [Teorem o Maksimalnom Toku i Minimalnom Rezu](#teorem-o-maksimalnom-toku-i-minimalnom-rezu)
3.  [Maksimalno Uparivanje u Bipartitnim Grafovima (Maximum Bipartite Matching)](#maksimalno-uparivanje-u-bipartitnim-grafovima-maximum-bipartite-matching)
    *   [Definicija i Primjena](#definicija-i-primjena)
    *   [Rješavanje pomoću Maksimalnog Toka](#rješavanje-pomoću-maksimalnog-toka)
4.  [Jako Povezane Komponente (Strongly Connected Components - SCC)](#jako-povezane-komponente-strongly-connected-components---scc)
    *   [Definicija i Graf Komponenata](#definicija-i-graf-komponenata)
    *   [Kosarajuov Algoritam](#kosarajuov-algoritam)
    *   [Primjena: 2-SAT Problem](#primjena-2-sat-problem)
5.  [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Protok materijala, podataka i resursa
Zamislite mrežu cijevi (s ograničenim kapacitetima) kroz koju želite poslati što više vode od izvora do ponora. Ovo je problem **maksimalnog toka**. Ova apstrakcija modelira mnoge stvarne probleme:
-   Protok podataka u računalnim mrežama.
-   Protok vozila u prometnoj mreži.
-   Protok proizvoda u lancu opskrbe.

### Problem uparivanja i dodjele
Imate grupu kandidata i grupu poslova. Svaki kandidat je kvalificiran za neke poslove. Kako dodijeliti poslove kandidatima tako da što više poslova bude pokriveno? Ovo je problem **maksimalnog uparivanja u bipartitnom grafu**. Pokazat ćemo kako se ovaj, naizgled drugačiji problem, može elegantno svesti na problem maksimalnog toka.

### Struktura usmjerenih grafova: Jake komponente
Usmjereni grafovi mogu imati složenu strukturu ciklusa. **Jako povezana komponenta (SCC)** je podskup čvorova u kojem postoji put od svakog čvora do svakog drugog čvora unutar tog podskupa. Rastavljanje grafa na SCC-ove otkriva njegovu temeljnu **acikličku** strukturu, što nam omogućuje primjenu DP-a ili topološkog sortiranja na "grafu komponenata".

### Preporučena Literatura
*   **CPH (Competitive Programmer's Handbook):**
    *   Poglavlje 20: *Flows and cuts*
    *   Poglavlje 17: *Strong connectivity*
*   **CLRS (Introduction to Algorithms):**
    *   Poglavlje 26: *Maximum Flow*
    *   Poglavlje 22.5: *Strongly connected components*

---

## Maksimalni Tok (Maximum Flow)

### Definicija Mrežnog Toka i Reidualnog Grafa
-   **Mrežni tok:** Usmjereni graf s izvorom `s` i ponorom `t`. Svaki brid `(u, v)` ima **kapacitet** `c(u, v)`.
-   **Tok:** Funkcija `f(u, v)` koja svakom bridu dodjeljuje vrijednost protoka, poštujući:
    1.  **Ograničenje kapaciteta:** `0 <= f(u, v) <= c(u, v)`.
    2.  **Očuvanje toka:** Za svaki čvor `u` (osim `s` i `t`), ukupan ulazni tok jednak je ukupnom izlaznom toku.
-   **Vrijednost toka:** Ukupan tok koji izlazi iz izvora `s`.
-   **Rezidualni graf `G_f`:** Ključan koncept. Predstavlja preostale kapacitete. Za svaki brid `(u, v)` u originalnom grafu, u `G_f` imamo:
    *   **"Forward" brid `(u, v)`** s kapacitetom `c(u, v) - f(u, v)`.
    *   **"Backward" brid `(v, u)`** s kapacitetom `f(u, v)`. Ovaj brid omogućuje "poništavanje" prethodno poslanog toka.

### Ford-Fulkerson Metoda i Povećavajući Putevi
Ford-Fulkerson je općenita metoda za pronalaženje maksimalnog toka.
**Ideja:** Počni s nultim tokom. Dok god postoji **povećavajući put** (augmenting path) od `s` do `t` u rezidualnom grafu, povećaj tok duž tog puta.

**Algoritam:**
1.  Inicijaliziraj tok `f` na 0 za sve bridove.
2.  `while` (postoji put `p` od `s` do `t` u `G_f` s pozitivnim kapacitetima):
    *   Pronađi **kapacitet puta** `c_p = min(c_f(u, v))` za sve bridove na putu `p`.
    *   Za svaki brid `(u, v)` na putu `p`:
        *   Smanji kapacitet `c_f(u, v)` za `c_p`.
        *   Povećaj kapacitet `c_f(v, u)` za `c_p`.
    *   Povećaj ukupni tok za `c_p`.

### Edmonds-Karp Algoritam (BFS pristup)
Ford-Fulkerson metoda ne specificira kako pronaći povećavajući put. Ako koristimo DFS, algoritam može biti spor. **Edmonds-Karp** algoritam specificira da se povećavajući put traži pomoću **BFS-a**. Ovo garantira da uvijek pronalazimo najkraći povećavajući put (u smislu broja bridova).

**Implementacija:**
BFS se koristi za pronalaženje puta u rezidualnom grafu. Kapaciteti se pamte u matrici ili `map`-i.
```cpp
// ... (inicijalizacija kapaciteta, grafa, toka)
long long max_flow = 0;
while (true) {
    // Pronađi povećavajući put pomoću BFS-a
    vector<int> parent(n + 1, 0);
    queue<pair<int, int>> q;
    q.push({s, INF});
    parent[s] = s;

    while (!q.empty()) {
        int u = q.front().first;
        int flow = q.front().second;
        q.pop();

        for (int v : adj[u]) {
            if (parent[v] == 0 && capacity[u][v] > 0) {
                parent[v] = u;
                int new_flow = min(flow, capacity[u][v]);
                if (v == t) {
                    // Pronađen put, vrati tok
                    // ... (implementacija povratka toka)
                }
                q.push({v, new_flow});
            }
        }
    }
    
    // Ako nema više povećavajućih puteva, izađi iz petlje
    if (parent[t] == 0) break;

    // Ažuriraj tok i rezidualni graf
    long long path_flow = ...; // dobiven iz BFS-a
    int v = t;
    while (v != s) {
        int u = parent[v];
        // f[u][v] += path_flow;
        // f[v][u] -= path_flow;
        capacity[u][v] -= path_flow;
        capacity[v][u] += path_flow;
        v = u;
    }
    max_flow += path_flow;
}
cout << max_flow << '\n';
```
**Složenost:** **O(V * E²)**. U praksi je često brži.

### Teorem o Maksimalnom Toku i Minimalnom Rezu
-   **Rez (Cut):** Podjela čvorova `V` na dva skupa, `S` i `T`, tako da `s` pripada `S`, a `t` pripada `T`.
-   **Kapacitet reza:** Zbroj kapaciteta svih bridova koji idu iz `S` u `T`.
-   **Minimalni rez:** Rez s najmanjim mogućim kapacitetom.
**Teorem:** Vrijednost maksimalnog toka u mreži jednaka je kapacitetu minimalnog reza.
Ovo je jedan od najvažnijih teorema u kombinatoričkoj optimizaciji. Nakon što Ford-Fulkerson završi, skup čvorova dostižnih iz `s` u rezidualnom grafu formira `S` stranu minimalnog reza.

---

## Maksimalno Uparivanje u Bipartitnim Grafovima (Maximum Bipartite Matching)

### Definicija i Primjena
-   **Bipartitni graf:** Graf čiji se čvorovi mogu podijeliti u dva disjunktna skupa, `L` i `R`, tako da svaki brid povezuje čvor iz `L` s čvorom iz `R`.
-   **Uparivanje (Matching):** Skup bridova u kojem nijedan čvor nije incidentan s više od jednog brida.
-   **Maksimalno uparivanje:** Uparivanje s najvećim mogućim brojem bridova.

### Rješavanje pomoću Maksimalnog Toka
Problem možemo svesti na maksimalni tok:
1.  Kreiraj novi graf. Dodaj novi izvor `s` i ponor `t`.
2.  Za svaki čvor `u` iz `L`, dodaj usmjereni brid `(s, u)` s kapacitetom 1.
3.  Za svaki čvor `v` iz `R`, dodaj usmjereni brid `(v, t)` s kapacitetom 1.
4.  Za svaki originalni brid `(u, v)` gdje je `u` u `L` i `v` u `R`, dodaj usmjereni brid `(u, v)` s kapacitetom 1 (ili ∞).
5.  Maksimalni tok u ovoj mreži jednak je veličini maksimalnog uparivanja.

**Složenost:** Ista kao i za maksimalni tok. Za bipartitne grafove, postoje i brži specijalizirani algoritmi poput Hopcroft-Karp (`O(E * sqrt(V))`), ali Ford-Fulkerson je često dovoljan.

---

## Jako Povezane Komponente (Strongly Connected Components - SCC)

### Definicija i Graf Komponenata
-   **Jako povezana komponenta (SCC):** Maksimalan podskup čvorova `C` takav da za svaka dva čvora `u, v` u `C` postoji put od `u` do `v` i put od `v` do `u`.
-   **Graf komponenata:** Ako svaku SCC sažmemo u jedan "meta-čvor", dobivamo novi usmjereni graf koji je **uvijek aciklički (DAG)**.

### Kosarajuov Algoritam
Elegantan i efikasan algoritam za pronalaženje svih SCC-ova u `O(n + m)` vremenu.
**Algoritam:**
1.  **Korak 1 (Prvi DFS):** Pokreni DFS na originalnom grafu `G`. Zabilježi vremena završetka (`f-time`) za svaki čvor, ili jednostavnije, spremaj čvorove u listu (ili stog) kako DFS završava obradu. Rezultat je lista čvorova sortirana po vremenu završetka u opadajućem redoslijedu.
2.  **Korak 2 (Drugi DFS):** Konstruiraj **transponirani graf** `G_T` (svi bridovi su obrnuti).
3.  Prođi kroz listu čvorova dobivenu u koraku 1 (od najvećeg `f-time` prema najmanjem). Za svaki čvor `u` koji još nije posjećen:
    *   Pokreni DFS iz `u` na `G_T`.
    *   Svi čvorovi posjećeni u ovom DFS-u čine jednu jako povezanu komponentu.

**Zašto ovo radi?** Prvi DFS pronalazi "kasno završene" čvorove, koji su obično korijeni (ili blizu korijena) SCC-ova u grafu komponenata. Drugi DFS, na transponiranom grafu, istražuje "unatrag" i uspijeva izolirati točno jednu komponentu prije nego što "pobjegne" u drugu.

### Primjena: 2-SAT Problem
Problem 2-SAT pita je li moguće zadovoljiti bulovsku formulu u 2-CNF obliku, npr. `(x1 ∨ ¬x2) ∧ (¬x1 ∨ x3)`. Ovo se može svesti na problem SCC-a:
1.  Napravi graf s `2n` čvorova, po jedan za svaki literal (`xi` i `¬xi`).
2.  Svaka klauzula `(a ∨ b)` je ekvivalentna dvjema implikacijama: `(¬a ⇒ b)` i `(¬b ⇒ a)`. Dodaj usmjerene bridove `(¬a, b)` i `(¬b, a)`.
3.  Formula je **nezadovoljiva** ako i samo ako neki literal `xi` i njegova negacija `¬xi` pripadaju **istoj jako povezanoj komponenti**.

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* **Police Chase:** Klasičan problem maksimalnog toka / minimalnog reza.
* **Distinct Routes:** Pronalaženje puteva nakon što se izračuna maksimalni tok.
* **School Dance:** Maksimalno bipartitno uparivanje.
* **Flight Route Check:** Provjera jake povezanosti (je li cijeli graf jedna SCC).
* **Planets and Kingdoms:** Pronalaženje i brojanje SCC-ova.
* **Coin Collector:** DP na grafu komponenata. Nakon što se pronađu SCC-ovi, zadatak se rješava na rezultirajućem DAG-u.

### Codeforces

*   **Police Stations** (Problem 371D): Zanimljiv problem koji se može modelirati kao mrežni tok, iako postoji i jednostavnije rješenje.
*   **Fox and Names** (Problem 510C): Zadan je skup stringova koji su leksikografski sortirani. Treba otkriti redoslijed slova. Ovo je klasičan problem topološkog sortiranja.
*   **Weakly Connected Components** (na raznim platformama): Problem koji zahtijeva razumijevanje razlike između slabe i jake povezanosti.```
