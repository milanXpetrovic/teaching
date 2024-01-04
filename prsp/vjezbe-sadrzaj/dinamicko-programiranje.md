---
layout: default
parent: PRSP
nav_order: 5
---

# Dinamičko programiranje

Dinamičko programiranje je tehnika koja kombinira ispravnost potpune pretrage i učinkovitost pohlepnih algoritama. Dinamičko programiranje može se primijeniti ako se problem može podijeliti na preklapajuće podprobleme koji mogu biti samostalno riješeni.

Postoje dvije upotrebe za dinamičko programiranje:
• Pronalaženje optimalnog rješenja: Želimo pronaći rješenje koje je što je moguće veće ili što manje.
• Prebrojavanje broja rješenja: Želimo izračunati ukupan broj mogućih rješenja.

## Zadatak 1: Fibonacci

Napišite funkcije `fib_1(n)`, `fib_2(n)` i `fib_3(n)` koja za zadani broj $n$ izračunava n-ti Fibonaccijev broj.

Zadatak riješite na tri načina:
- Rekurzivno, $O(n)$ vremenska i memorijska složenost.
- Dinamičkim programiranjem, $O(n)$ vremenska i memorijska složenost.
- Dinamičkim programiranjem, $O(n)$ vremenska i $O(1)$ memorijska složenost.

Usporedite vremena izvođenja triju funkcija za $n$ 40.

### Primjer

**Input:**

```
40
```
**Output:**
```
102334155
```

## Zadatak 2: Problem s kovanicama

Problem koji smo rješavali u poglavlju [Pohlepni algoritmi](../pohlepni-algoritmi#zadatak-1-problem-s-kovanicama). Riješili smo problem pomoću pohlepnog algoritma koji uvijek bira najveći mogući novčić. Pohlepni algoritam radi, na primjer, kada kovanice su kovanice eura, ali u općem slučaju pohlepni algoritam ne daje nužno optimalno rješenje, primjerice ako su zadane kovanice $\{1,3,4}\$.

Zadatak je za unesenu listu denominacija kovanica $l$, $\{c_1, c_2, c_3,...,c_k\}$ i svotu $k$ pronaći minimalan broj kovanica potreban za stvoriti svotu $k$. Ako svotu nije moguće stvoriti pomoću zadanih kovanica ispisuje se $-1$.

**Input:**
U prvom redu unosi se cijeli broj $n$ koji označuje traženu svotu. 
U drugom redu unosi se lista $l$ koja sadrži vrijednosti na kovanicama.

**Output:**
Ako je moguće kreirati svotu ispisuje se broj $n$ koji označuje broj kovanica potrebnih za svotu $k$. Ako nije moguće kreirati svotu $k$ ispisuje se $-1$.

### Primjeri

**Input:**
```
1 2 5
11
```
**Output:**
```
3
```

**Input:**
```
5 9
4
```
**Output:**
```
-1
```


## Zadatak 3

Penjete se stubištem. Do vrha je potrebno $n$ stuba. Svaki put se možete popeti 1 ili 2 stube. Na koliko se različitih načina možete popeti do vrha?

### Primjer 1

**Input:**
```
2
```
**Output:**
```
2
```
1. 1  + 1 
2. 2 

### Primjer 2

**Input:**
```
3
```
**Output:**
```
3
```

1. 1  + 1  + 1 
2. 1  + 2 
3. 2  + 1 


## Zadatak 4

Zadan je cjelobrojni niz troškova gdje je `cijena[i]` cijena `i` koraka na stubištu. Nakon što platite troškove, možete se popeti za jednu ili dvije stepenice.

Možete započeti od koraka s indeksom $0$ ili od koraka s indeksom $1$.

Pronađite minimalnu cijenu da biste došli do vrha stubišta.

### Primjer 1

**Input:**
```
10 15 20
```
**Output:**
```
15
```
Počet ćete od indeksa 1.
- Platite 15 i popnite se dvije stepenice do vrha.
Ukupna cijena je 15.

### Primjer 2

**Input:**
```
1 100 1 1 1 100 1 1 100 1
```
**Output:**
```
6
```

Počinje se od indeksa 0.
- Platite 1 i popnite se dvije stepenice do indeksa 2.
- Platite 1 i popnite se dvije stepenice do indeksa 4.
- Platite 1 i popnite se dvije stepenice do indeksa 6.
- Platite 1 i popnite se jednu stepenicu do indeksa 7.
- Platite 1 i popnite se dvije stepenice do indeksa 9.
- Platite 1 i popnite se jednu stepenicu do vrha.
Ukupni trošak je 6.


## Codeforces zadaci

- [Hit the Lottery](https://codeforces.com/problemset/problem/996/A)
- [Maximum Increase](https://codeforces.com/problemset/problem/702/A)