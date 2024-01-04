---
layout: default
title: Obilazak grafa
parent: Grafovi
nav_order: 1
nav_exclude: false
---

# Obilazak grafa

DFS (Depth-First Search) je algoritam obilaska grafa koji se temelji na ideji putovanja u dubinu iz odabranog početnog čvora (granu po granu). Počevši od korijena, ovaj algoritam istražuje što dublje u grafu prije nego se vrati unatrag kako bi istražio druge grane. Često se koristi stog (stack) kao memorijska struktura za praćenje puta i čvorova. DFS je koristan za pronalaženje rješenja problema kao što su topološko sortiranje, pretraga rute u mrežama ili pronalazak putanja u grafu.

## Depth first search (DFS) – pretraživanje u dubinu

```python
def dfs(graph, start):
    visited, stack = [], [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            stack.extend([i for i in graph[vertex] if i not in visited])
    return visited
```

## Breadth first search (BFS) – pretraživanje u širinu

BFS (Breadth-First Search) je algoritam obilaska grafa, koji radi na principu širenja u dubinu od zadanog početnog čvora. Počevši od korijena, ovaj algoritam istražuje sve čvorove na jednoj razini dubine prije nego što prijeđe na čvorove na sljedećoj razini. Često se korišti reda (queue) kao memorijska struktura za pamćenje čvorova koje treba posjetiti. Ovaj algoritam je koristan kada se traži put s najmanje koraka od početnog do odredišnog čvora i provjeri povezanosti u mrežama.

**Pseudokod za BFS algoritam**

```

```

U nastavku je prikazan kod koji implementira BFS (Breadth-First Search) algoritam za obilazak grafa počevši od odabranog čvora `start`. Funkcija `bfs` koristi skup `visited` za praćenje posjećenih čvorova i red `queue` za provjeru susjednih čvorova. Petlja se izvršava dok god postoji čvor u redu `queue`. Funkcija vraća skup posjećenih čvorova `visited`.

```python
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend([i for i in graph[vertex] if i not in list(visited)])

    return visited
```



## Zadaci za vježbu

- Isprobajte BFS i DFS algoritam nad grafom veličine 50.

- Ispišite ako u vašem grafu postoje čvorovi iz kojih možemo posjetiti sve ostale čvorove. Ako ne onda ispišite -1.

- Provjerite ako je vaš graf potpuno povezan. Graf je potpuno povezan ako iz svakog čvora možemo posjetiti sve ostale čvorove u grafu.

- Konstruirajte algoritam za bojanje vrhova u vašem grafu, pokušajte odrediti najmanji broj boja potreban za pobojati graf.

- Pronađite najdulji put u vašem grafu.



# [Putovanje kroz graf](https://cses.fi/book/book.pdf#chapter.12)

## Zadatak 1: Broj otoka

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađite broj otoka.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava broj otoka.

**Input:**

```text
4 5
1 1 1 1 0
1 1 0 1 0
1 1 0 0 0
0 0 0 0 0
```

**Output:**

```text
1
```

**Input:**

```text
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

**Output:**

```text
3
```

## Zadatak 2: Najveći otok

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađite otok s najvećom površinom, ako nema otoka vratite 0.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava površinu najvećeg otoka.

**Input:**

```text
8 13
0 0 1 0 0 0 0 1 0 0 0 0 0 
0 0 0 0 0 0 0 1 1 1 0 0 0 
0 1 1 0 1 0 0 0 0 0 0 0 0 
0 1 0 0 1 1 0 0 1 0 1 0 0 
0 1 0 0 1 1 0 0 1 1 1 0 0 
0 0 0 0 0 0 0 0 0 0 1 0 0 
0 0 0 0 0 0 0 1 1 1 0 0 0 
0 0 0 0 0 0 0 1 1 0 0 0 0
```

**Output:**

```text
6
```

## Zadatak 3: Okružene regije

S obzirom na $m \times m$ matricu koja sadrži "X" i "O", osvojite sve regije koje su u 4 smjera okružene s "X".

Regija se osvaja pretvaranjem svih 'O' u 'X' u toj okruženoj regiji.

**Input:**

```text
X X X X
X O O X
X X O X
X O X X
```

**Output:**

```text
X X X X
X X X X
X X X X
X O X X
```

**Objašnjenje**:
Primijetite da se 'O' ne smije osvojiti jedino ako:

- Nalazi se na rubu matrice
- Nalazi se uz "O" koji se ne može osvojiti.

**Input:**

```text
X X X X X X X 
X O O O X X O 
X X X X X O O 
X X O X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

**Output:**

```text
X X X X X X X 
X X X X X X O 
X X X X X O O 
X X X X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

## Zadatak 4: Vrijeme putovanja

Martica $m \times m$ prikazuje vrijeme putovanja između gradova. Za zadani grad $n$ potrebno je pronaći najkraće vrijeme putovanja do svih ostalih, ako se svi gradovi u grafu ne mogu posjetiti, ispišite $-1$.

**Input:**
$n$ oznaka grada, $m$ ukupan broj gradova.
Slijedi $m$ redaka s $m$ cjelobrojnih vrijednosti.

**Output:**
Ispis udaljenosti do svih gradova ili $-1$ ako to nije moguće.

**Input:**

```text
3 5
0 5 3 2 5 
9 0 4 0 0 
7 6 0 2 8 
2 0 1 0 3 
0 7 5 5 0 
```

## Zadatak 5: Izgradnja cesta

Zemlja ima $n$ gradova i $m$ cesta između njih. Cilj je izgraditi nove ceste tako da postoji ruta između bilo koja dva grada.

Vaš zadatak je saznati minimalan broj potrebnih cesta, te odrediti koje ceste treba izgraditi.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj gradova i cesta. Gradovi su označeni brojevima $1,2,…,n$.

Nakon toga slijedi $m$ redaka koji opisuju ceste. Svaki red ima dva cijela broja $a$ i $b$: ako postoji cesta između tih gradova.

Cesta uvijek povezuje dva različita grada, a između bilo koja dva grada postoji najviše jedna cesta.

**Output:**
Prvo ispišite cijeli broj $k$: broj potrebnih cesta.

Zatim ispišite $k$ redaka koji opisuju nove ceste. Možete ispisati bilo koje valjano rješenje.

**Input:**

```text
4 2
1 2
3 4
```

**Output:**

```text
1
2 3
```

## Zadatak 6: Timovi

U razredu ima $n$ učenika i $m$ prijateljstava među njima. Vaš zadatak je podijeliti učenike u dva tima na način da dva učenika u timu nisu prijatelji. Možete slobodno odabrati veličinu timova.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj učenika i prijateljstava. Zjenice su označene brojevima $1,2,…,n$.

Zatim sljedi $m$ redaka koji opisuju prijateljstva. Svaki red ima dva cijela broja $a$ i $b$: učenici $a$ i $b$ su prijatelji.

Svako prijateljstvo je između dva različita učenika i postoji najviše jedno prijateljstvo iymeđu ta dva učenika.

**Output:**
Ispišite primjer kako sastaviti timove. Za svakog učenika ispišite "1" ili "2" ovisno u koju će ekipu učenik biti dodijeljen.

Ako nema rješenja ispisati "NEMA".

**Input:**

```text
5 3
1 2
1 3
4 5
```

**Output:**

```text
1 2 2 1 2
```

## Zadatak 7: Ciklus

Dobili ste usmjereni graf, a vaš zadatak je otkriti sadrži li negativan ciklus te dati primjer takvog ciklusa.

**Input:**
Prvi ulazni red ima dva cijela broja $n$ i $m$: broj čvorova i bridova. Čvorovi su označeni brojevima $1,2,…,n$.

Nakon toga, ulaz ima $m$ redaka koji opisuju veze. Svaki redak ima tri cijela broja $a$, $b$ i $c$ koji oynačuju da postoji brid od čvora $a$ do čvora $b$ čija je duljina $c$.

**Output:**
Ako graf sadrži negativan ciklus, ispišite prvo "YES", a zatim čvorove u ciklusu ispravnim redoslijedom. Ako postoji više negativnih ciklusa, možete ispisati bilo koji od njih. Ako nema negativnih ciklusa, ispišite "NE".

**Input:**

```text
4 5
1 2 1
2 4 1
3 1 1
4 1 -3
4 3 -2
```

**Output:**

```text
YES
1 2 4 1
```

## Zadatak 8: Popravak ceste

Postoji $n$ gradova i $m$ cesta između njih. Nažalost, stanje na cestama je toliko loše da se ne mogu koristiti. Vaš zadatak je popraviti neke od cesta kako bi između bilo koja dva grada postojala ruta.

Za svaku cestu znate njenu cijenu popravka i trebali biste pronaći rješenje gdje je ukupni trošak što je moguće manji.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj gradova i cesta. Gradovi su označeni brojevima $1,2,…,n$.

Nakon toga slijedi $m$ redaka koji opisuju ceste. Svaki red ima tri cijela broja a, b i c koji označava da postoji cesta između gradova a i b, a cijena njezine popravke je c. Sve ceste su dvosmjerne.

Sve ceste su između dva različita grada, a između dva grada postoji najviše jedna cesta.

**Output:**

Ispišite jedan cijeli broj: minimalni ukupni trošak popravka. Međutim, ako nema rješenja, ispišite "NEMOGUĆE".

**Input:**

```text
5 6
1 2 3
2 3 5
2 4 2
3 4 8
5 1 7
5 4 4
```

**Output:**

```text
14
```

## Zadatak 9: Upis predmeta

U zadanom usmjerenom grafu, vrhovi predstavljaju predmete, neki od tih predmeta imaju predmete koji prethodno moraju biti položeni da bi se mogli upisati što je predstavljeno vezama. Odnosno, veza iz vrha A u vrh B nam predstavlja da je predmet A preduvjet za upisati predmet B.

Pomoću topološkog sortiranja ispišite redosljed polaganja predmeta tako da se ne dogodi problem s upisom predmeta a da pritom nije položen predmet koji je preduvjet.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj predmeta, nakon toga slijedi $m$ redaka koji navode veze.

**Output:**
Ispišite topološki sortirani graf.

**Input:**

```text
A B
A C
B D
B E
C F
```

**Output:**

```text
A C F B E D
```
