---
layout: default
parent: PRSP
nav_order: 9
nav_exclude: false
---

# Putovanje kroz graf

## Zadatak 1: Broj otoka

Zadana je $m \times n$ 2D matrica koja predstavlja kartu gdje je '1' kopno i '0' voda, pronađte broj otoka.

Otok je okružen vodom i nastaje spajanjem susjednih kopna vodoravno ili okomito. Možete pretpostaviti da su sva četiri ruba mreže okružena vodom.

**Input:**
U prvom redu unose se vrijednosti $m$ i $n$. U sljedećih $m$ redova nalazi se $n$ vrijednosti koje su $0$ ili $1$.

**Output:**
Broj $n$ koji označava broj otoka.

**Input:**

```console
4 5
1 1 1 1 0
1 1 0 1 0
1 1 0 0 0
0 0 0 0 0
```

**Output:**

```console
1
```

**Input:**

```console
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1
```

**Output:**

```console
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

```console
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

```console
6
```

## Zadatak 3: Okružene regije

S obzirom na $m \times m$ matricu koja sadrži "X" i "O", osvojite sve regije koje su u 4 smjera okružene s "X".

Regija se osvaja pretvaranjem svih 'O' u 'X' u toj okruženoj regiji.

**Input:**

```console
X X X X
X O O X
X X O X
X O X X
```

**Output:**

```console
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

```console
X X X X X X X 
X O O O X X O 
X X X X X O O 
X X O X X O X 
X X X X X X O 
X X X X X X X 
X X X X X X X 
```

**Output:**

```console
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

```console
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

```console
4 2
1 2
3 4
```

**Output:**

```console
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

```console
5 3
1 2
1 3
4 5
```

**Output:**

```console
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

```console
4 5
1 2 1
2 4 1
3 1 1
4 1 -3
4 3 -2
```

**Output:**

```console
YES
1 2 4 1
```

## Zadatak 8:

Postoji $n$ gradova i $m$ cesta između njih. Nažalost, stanje na cestama je toliko loše da se ne mogu koristiti. Vaš zadatak je popraviti neke od cesta kako bi između bilo koja dva grada postojala ruta.

Za svaku cestu znate njenu cijenu popravka i trebali biste pronaći rješenje gdje je ukupni trošak što je moguće manji.

**Input:**
U prvom retku za unos nalaze se dva cijela broja $n$ i $m$: broj gradova i cesta. Gradovi su označeni brojevima $1,2,…,n$.

Nakon toga slijedi $m$ redaka koji opisuju ceste. Svaki red ima tri cijela broja a, b i c koji označava da postoji cesta između gradova a i b, a cijena njezine popravke je c. Sve ceste su dvosmjerne.

Sve ceste su između dva različita grada, a između dva grada postoji najviše jedna cesta.

**Output:**

Ispišite jedan cijeli broj: minimalni ukupni trošak popravka. Međutim, ako nema rješenja, ispišite "NEMOGUĆE".

**Input:**

```console
5 6
1 2 3
2 3 5
2 4 2
3 4 8
5 1 7
5 4 4
```

**Output:**

```console
14
```