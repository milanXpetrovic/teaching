---
layout: default
title: Grafovi
parent: PRSP
has_children: true
has_toc: false
nav_exclude: false
---

# [Grafovi: uvod](https://cses.fi/book/book.pdf#chapter.11)

Mnogi programski problemi mogu se riješiti modeliranjem problema kao problema grafa i korištenjem odgovarajućih algoritmova nad tim grafovima.  Često su grafovi idealni za predstavljanje veza i odnosa među elementima u raznim situacijama. Tipičan primjer grafa je mreža cesta i gradova u zemlji. Ponekad, je graf skriven u problemu i teško ga je otkriti. Ovaj dio vježbi govori o algoritmima nad grafovima.

U sklopu tematske cjeline Grafovi proći ćemo kroz nekoliko ključnih područija koja su:

- [Putovanje kroz graf](../putovanje-kroz-graf)
- [Traženje najkraćeg puta](../najkraci-putovi.md)
- [Stabla](../stabla.md)
- [Razapinjujuća stabla](../razapinjujuca-stabla.md)
- [Usmjereni grafovi](../usmjereni-grafovi.md)
- [Staze i ciklusi](../staze-i-ciklusi.md)
- [Dodatne teme](../grafovi-dodatno.md)


## Osnovni termini

Osnovna terminologija koja se koristi prilikom rada s grafovima:

- **Vrh (čvor):**  Točka u grafu. Može predstavljati entitet ili element.
- **Brid (veza):** Veza između dva vrha. Može imati smjer (usmjerena) ili ne (neusmjerena).
- **Susjedi:** Vrhovi u grafu koji su izravno povezani bridom.
- **Stupanj vrha:**  Broj bridova povezanih s vrhom.
- **Petlja** Brid koji spaja vrh sa samim sobom.
- **Povezan graf** Graf je povezan ako između svaka dva vrha postoji put, u suprotnom
graf je nepovezan.
- **Podgraf:** Graf dobiven iz originalnog grafa izbacivanjem nekih vrhova i/ili bridova.
- **Neusmjereni graf:**  Graf u kojem bridovi nemaju određen smjer.
- **Usmjereni graf:**  Graf u kojem bridovi imaju smjer i povezuju vrhove u jednom smjeru.
- **Težinski graf:**  Graf u kojem svaki brid ima povezanu numeričku vrijednost ili težinu.
- **Staza:** Šetnja u kojoj su svi bridovi različiti (ali moguća su ponavljanja vrhova), dok je
*put* staza u kojoj su svi vrhovi različiti (osim eventualno prvog i zadnjog - takav put nazivamo ciklusom).
- **Ciklus:** Put koji počinje i završava u istom vrhu, prolazeći kroz različite bridove.
- **Stablo:** Graf bez ciklusa, povezan i s jednim vrhom kao korijenom.
- **List:** Vrh stupnja 1.
- **Razapinjujuće stablo:** Podgraf originalnog grafa koji je stablo (bez ciklusa) i povezuje sve vrhove izvornog grafa. Razapinjuće stablo ne smije sadržavati cikluse.
- **Potpun graf:**  Graf u kojem su svi parovi vrhova povezani bridom.
- **Staza:** Slijed vrhova u kojem su susjedni vrhovi povezani bridom. Staza može proći kroz svaki vrh samo jednom.
- **Najkraći put:** Najkraća staza ili put između dva vrha u težinskom grafu. Mjera duljine najkraćeg puta može biti ukupna težina bridova ili broj bridova koje treba proći da bi se došlo od jednog vrha do drugog.
- **Bojanje grafa** Postupak dodjeljivanja boja svakom vrhu grafa tako da susjedni vrhovi imaju različite boje.

## Stvaranje grafa

### Lista susjedstva

U nastavku je dana funkcija za generiranje grafa kao liste susjedstva, ona vraća graf reprezentiran pomoću rječnika. Funkcija `generate_random_adjacency_dict` prima broj čvorova `n` i stvara graf predstavljen kao rječnik čiji su ključevi čvorovi, a vrijednosti su lista susjedstva tih čvorova.

Algoritam stvara graf dodjeljivanjem nasumičnih susjeda svakom čvoru. Broj susjeda koje će svaki čvor imati generira se nasumično između 0 i n.

Na primjer, ako se funkciji `generate_random_adjacency_list` proslijedi broj $5$, rezultat će biti rječnik koji predstavlja graf s 5 čvorova, gdje su susjedni čvorovi nasumično dodijeljeni. Ova implementacija koristi modul `random` za generiranje nasumičnih susjeda za svaki čvor.

Parametar `self_loops` omogućuje ili onemogućuje petlje u grafu, dok `seed` možemo kontrolirati generiranje pseudonasumičnih brojeva kako bismo uvijek dobili isti graf. U Pythonu, funkcija `random.seed()` postavlja početnu vrijednost za generator pseudonasumičnih brojeva. Ova mogućnost može se koristiti pozivanjem funkcije `generate_random_adjacency_list` sa parametrom `seed`, npr. `generate_random_adjacency_list(10, seed=42)`. Ako želmo dodati i petlje u grafu koristimo `generate_random_adjacency_list(10, self_loops=True, seed=42)`.

```python
import random

def generate_random_adjacency_list(n, self_loops=False, seed=None):
    if seed is not None:
        random.seed(seed)

    g = {}
    for i in range(0, n):
        num_neighbours = random.randint(0, n) if self_loops else random.randint(0, n - 1)
        neighbours = random.sample(range(n), num_neighbours)
        if not self_loops and i in neighbours:
            neighbours.remove(i)
        g[str(i)] = [str(x) for x in neighbours]

    return g
```

### Matrica susjedstva

U nastavku je dana funkcija za generiranje grafa kao matrice susjedstva. Funkcija `generate_random_adjacency_matrix` prima broj čvorova n i omogućuje uključivanje ili isključivanje petlji (self-loops) unutar grafa, dok `seed` možemo kontrolirati generiranje pseudonasumičnih brojeva kako bismo uvijek dobili isti graf.

```python
import random

def generate_random_adjacency_matrix(n, self_loops=False, seed=None):
    if seed is not None:
        random.seed(seed)

    g = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        num_neighbours = random.randint(0, n) if self_loops else random.randint(0, n - 1)
        neighbours = random.sample(range(n), num_neighbours)
        if not self_loops and i in neighbours:
            neighbours.remove(i)
        for neighbour in neighbours:
            g[i][neighbour] = 1
            g[neighbour][i] = 1

    return g
```


