---
nav_exclude: true
---

# Tjedan 4: Pohlepni Algoritmi (Greedy Algorithms)

## Sadržaj

1. [Uvod i Motivacija](#uvod-i-motivacija)
    * [Što je pohlepni algoritam?](#što-je-pohlepni-algoritam)
    * [Pohlepni Algoritmi vs. Dinamičko Programiranje](#pohlepni-algoritmi-vs-dinamičko-programiranje)
    * [Ključna Svojstva](#ključna-svojstva)
    * [Preporučena Literatura](#preporučena-literatura)
2. [Primjeri Zadataka i Objašnjenja](#primjeri-zadataka-i-objašnjenja)
    * [Problem 1: Problem novčića (Coin Problem)](#problem-1-problem-novčića-coin-problem)
    * [Problem 2: Raspoređivanje događaja (Activity Selection)](#problem-2-raspoređivanje-događaja-activity-selection)
    * [Problem 3: Huffmanovo kodiranje (Data Compression)](#problem-3-huffmanovo-kodiranje-data-compression)
3. [Zadaci za Vježbu](#zadaci-za-vježbu)

---

## Uvod i Motivacija

### Što je pohlepni algoritam?

**Pohlepni algoritam** je strategija za rješavanje optimizacijskih problema koja na svakom koraku donosi **lokalno optimalan izbor** u nadi da će taj izbor dovesti do **globalno optimalnog rješenja**.

Ključna karakteristika je da pohlepni algoritam nikada ne preispituje svoje odluke. Jednom kada napravi izbor, on je konačan. Zbog te jednostavnosti, pohlepni algoritmi su često vrlo brzi (obično O(n) ili O(n log n) nakon sortiranja) i jednostavni za implementaciju.

Najveći izazov kod pohlepnih algoritama nije implementacija, već **dokazivanje njihove točnosti**. Intuitivno "pohlepno" rješenje koje se čini ispravnim može lako pasti na specifičnim primjerima.

### Pohlepni Algoritmi vs. Dinamičko Programiranje

Obje tehnike se koriste za optimizacijske probleme i oslanjaju se na svojstvo **optimalne podstrukture** (optimalno rješenje problema sadrži optimalna rješenja podproblema). Međutim, fundamentalno se razlikuju u načinu donošenja odluka:

* **Dinamičko programiranje:** Rješava sve podprobleme, a zatim donosi odluku na temelju njihovih rješenja. Radi "bottom-up" (od manjih prema većim problemima).
* **Pohlepni algoritam:** Donosi odluku koja se čini najboljom u tom trenutku, a zatim rješava **jedan preostali podproblem**. Radi "top-down" i ne razmatra sve moguće opcije.

Ako pohlepna strategija radi, gotovo uvijek je brža i jednostavnija od dinamičkog programiranja.

### Ključna Svojstva

Da bi pohlepni algoritam bio točan, problem obično mora imati sljedeća dva svojstva:

1. **Svojstvo pohlepnog izbora (Greedy-choice property):** Globalno optimalno rješenje može se postići donošenjem lokalno optimalnih izbora. Drugim riječima, izbor koji se čini najboljim u trenutku ne smije nas spriječiti da dođemo do globalnog optimuma.
2. **Optimalna podstruktura (Optimal substructure):** Nakon što napravimo pohlepni izbor, preostali problem je manja verzija originalnog problema, a optimalno rješenje tog podproblema, u kombinaciji s pohlepnim izborom, daje optimalno rješenje originalnog problema.

### Preporučena Literatura

* **CPH (Competitive Programmer's Handbook):**
  * Poglavlje 6: *Greedy algorithms*
* **CLRS (Introduction to Algorithms):**
  * Poglavlje 16: *Greedy Algorithms*

---

## Primjeri Zadataka i Objašnjenja

### Problem 1: Problem novčića (Coin Problem)

**Zadatak:** Zadan je skup denominacija novčića i ciljani iznos `n`. Pronađi minimalan broj novčića potreban za formiranje iznosa `n`. Svaku denominaciju možemo koristiti neograničen broj puta.

#### Pohlepna Strategija

Na svakom koraku, odaberi najveći novčić čija je vrijednost manja ili jednaka preostalom iznosu.

#### Kada radi?

Ova strategija radi za kanonske sustave novčića, kao što su euro (`{1, 2, 5, 10, 20, 50, ...}`) ili američki dolar.

**Primjer (EUR):** Iznos = 48, Kovanice = `{1, 2, 5, 10, 20, 50}`

1. Uzmi 20 (preostalo 28)
2. Uzmi 20 (preostalo 8)
3. Uzmi 5 (preostalo 3)
4. Uzmi 2 (preostalo 1)
5. Uzmi 1 (preostalo 0)
Rješenje: 5 novčića (`20+20+5+2+1`). Ovo je optimalno.

#### Kada ne radi?

Pohlepna strategija **ne radi** za proizvoljne sustave novčića.

**Kontraprimjer:** Iznos = 6, Kovanice = `{1, 3, 4}`

* **Pohlepno rješenje:**
    1. Uzmi 4 (preostalo 2)
    2. Uzmi 1 (preostalo 1)
    3. Uzmi 1 (preostalo 0)
    Rješenje: 3 novčića (`4+1+1`).
* **Optimalno rješenje:**
    1. Uzmi 3 (preostalo 3)
    2. Uzmi 3 (preostalo 0)
    Rješenje: 2 novčića (`3+3`).

Ovaj primjer pokazuje da lokalno optimalan izbor (uzeti najveći novčić) nije doveo do globalno optimalnog rješenja. Općeniti problem novčića rješava se dinamičkim programiranjem (kao što smo vidjeli prošli tjedan).

### Problem 2: Raspoređivanje događaja (Activity Selection)

**Zadatak:** Zadan je skup od `n` događaja, svaki s vremenom početka i završetka. Potrebno je odabrati maksimalan broj događaja koji se međusobno ne preklapaju.

**Primjer:** Događaji (početak, kraj): `(1, 4), (3, 5), (0, 6), (5, 7), (8, 9)`

#### Pohlepna Strategija

Intuitivno, mogli bismo probati:

1. **Odabrati najkraći događaj:** Ne radi. Kratak događaj može blokirati dva duža, ali nepreklapajuća.
2. **Odabrati događaj koji počinje najranije:** Ne radi. Događaj koji rano počne, ali dugo traje, može blokirati mnoge druge.

**Ispravna strategija:** Na svakom koraku, odaberi događaj koji **završava najranije**.

**Algoritam:**

1. Sortiraj događaje po vremenu završetka.
2. Odaberi prvi događaj iz sortirane liste.
3. Prođi kroz ostatak liste i odaberi svaki sljedeći događaj koji počinje nakon što je prethodno odabrani završio.

**Zašto ovo radi?** Odabirom događaja koji najranije završava, oslobađamo resurs što je prije moguće, čime maksimiziramo vrijeme dostupno za ostale događaje. Ovo je klasičan dokaz svojstva pohlepnog izbora.

**Kod:**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <utility>

struct Event {
    int start, end;
};

// Funkcija za sortiranje po vremenu završetka
bool compareEvents(const Event& a, const Event& b) {
    return a.end < b.end;
}

int main() {
    // ... Brzi I/O ...
    int n;
    cin >> n;
    vector<Event> events(n);
    for (int i = 0; i < n; ++i) {
        cin >> events[i].start >> events[i].end;
    }

    sort(events.begin(), events.end(), compareEvents);

    int count = 0;
    int last_finish_time = -1;

    if (n > 0) {
        count = 1;
        last_finish_time = events.end;

        for (int i = 1; i < n; ++i) {
            if (events[i].start >= last_finish_time) {
                count++;
                last_finish_time = events[i].end;
            }
        }
    }

    cout << count << '\n';
    return 0;
}
```

**Složenost:** O(n log n) zbog sortiranja. Pohlepni odabir nakon toga traje O(n).

### Problem 3: Huffmanovo kodiranje (Data Compression)

**Zadatak:** Zadan je skup znakova i njihove frekvencije pojavljivanja. Dizajniraj **prefiksni kod** (gdje nijedan kod nije prefiks drugog) tako da ukupna duljina kodiranog teksta bude minimalna.

**Pohlepna Strategija:** Na svakom koraku, spoji dva znaka (ili podstabla) s najmanjim frekvencijama.

**Algoritam (Huffmanov algoritam):**

1. Za svaki znak, kreiraj list stabla s njegovom frekvencijom kao težinom.
2. Stavi sve listove u prioritetni red (min-heap), gdje je prioritet određen frekvencijom.
3. Dok u redu ima više od jednog čvora:
    * Izvadi dva čvora s najmanjim frekvencijama (`A` i `B`).
    * Kreiraj novi interni čvor `C` čija je frekvencija zbroj frekvencija od `A` i `B`.
    * Postavi `A` i `B` kao djecu od `C`.
    * Vrati `C` u prioritetni red.
4. Preostali čvor je korijen Huffmanovog stabla. Kodovi se čitaju prateći put od korijena (0 za lijevo, 1 za desno).

**Zašto ovo radi?** Pohlepni izbor spajanja dva najmanje frekventna znaka `x` i `y` je uvijek siguran. Može se dokazati da postoji optimalno stablo u kojem su `x` i `y` braća na najnižoj razini.

**Implementacija:** Za efikasno pronalaženje dva najmanja elementa, koristimo `priority_queue` u C++.

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <string>

// Čvor u Huffmanovom stablu
struct MinHeapNode {
    char data;
    unsigned freq;
    MinHeapNode *left, *right;

    MinHeapNode(char data, unsigned freq) {
        left = right = nullptr;
        this->data = data;
        this->freq = freq;
    }
};

// Usporedba za prioritetni red
struct compare {
    bool operator()(MinHeapNode* l, MinHeapNode* r) {
        return (l->freq > r->freq);
    }
};

void printCodes(MinHeapNode* root, string str) {
    if (!root) return;
    if (root->data != '$') { // '$' označava interni čvor
        cout << root->data << ": " << str << "\n";
    }
    printCodes(root->left, str + "0");
    printCodes(root->right, str + "1");
}

void HuffmanCodes(vector<char>& data, vector<unsigned>& freq, int size) {
    MinHeapNode *left, *right, *top;
    priority_queue<MinHeapNode*, vector<MinHeapNode*>, compare> minHeap;

    for (int i = 0; i < size; ++i)
        minHeap.push(new MinHeapNode(data[i], freq[i]));

    while (minHeap.size() != 1) {
        left = minHeap.top(); minHeap.pop();
        right = minHeap.top(); minHeap.pop();

        top = new MinHeapNode('$', left->freq + right->freq);
        top->left = left;
        top->right = right;
        minHeap.push(top);
    }
    printCodes(minHeap.top(), "");
}
```

**Složenost:** O(n log n), gdje `n` je broj različitih znakova. U svakom od `n-1` koraka, radimo dvije `pop` i jednu `push` operaciju na prioritetnom redu, od kojih svaka traje O(log n).

---

## Zadaci za Vježbu

### CSES Problem Set ([https://cses.fi/problemset/](https://cses.fi/problemset/))

* **Movie Festival:** Klasičan primjer problema odabira aktivnosti.
* **Tasks and Deadlines:** Problem koji ima jednostavno pohlepno rješenje nakon sortiranja. Razmislite po kojem kriteriju treba sortirati.
* **Stick Lengths:** Cilj je minimizirati sumu apsolutnih razlika. Pohlepni izbor je odabrati medijan.
* **Towers:** Zanimljiv problem koji se rješava pohlepno korištenjem strukture podataka (npr. `multiset`) za praćenje vrhova tornjeva.

### Codeforces

* **Ciel and Receipt** (Problem 320A): Problem povrata novca koji se može riješiti pohlepnim odabirom najveće moguće potencije broja 2.
* **Lecture Sleep** (Problem 961B): Pohlepna ideja se kombinira s tehnikom kliznog prozora (sliding window).
* **Boats Competition** (Problem 1399C): Sortiraj natjecatelje i koristi tehniku dva pokazivača kako bi pohlepno formirao timove.


[Sljedeća lekcija: ](){: .btn .btn-purple .float-right}
