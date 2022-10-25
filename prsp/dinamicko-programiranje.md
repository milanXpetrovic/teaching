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

## SRTBOT
SRTBOT - Paradigma za dizajniranje rekurzivnih algoritama:

- Subproblem definition - problem koji rješavamo rastavljamo na jednostavnije podprobleme (Subproblem definition). 
- Relate - Povezanost različitih rješenja podproblema s nekom rekurzivnom strukturom (Recurrence relation).
- Topological order- Prikažemo li rješavanje problema kao graf, onda će podproblemi biti čvorovi u tom grafu, a veze su ovisnosti među njima. Ono što želimo postići je da je naš graf Usmjeren ackilički graf (DAG).
- Base case - Zadan osnovni slučaj u rekurzivnoj strukturi.
- Original problem - Želimo riješiti orginalni problem pomoću rastavljanja na podprobleme.
- Time analysis - Analiza vremena izvodđenja.



## Zadatak 1: Fibonacci
Napišite funkcije `fib_1(n)`, `fib_2(n)` i `fib_3(n)` koja za zadani broj $n$ izračunava n-ti Fibbonaccijev broj.

Zadatak rješite na tri načina:
- Rekurzivno, $O(n)$ vremenska i memorijska složenost.
- Dinamičkim programiranjem, $O(n)$ vremenska i memorijska složenost.
- Dinamičkim programiranjem, $O(n)$ vremenska i $O(1)$ memorijska složenost.

Usporedite vremena izvođenja triju rješenja za 

### Primjer
**Input:**
```
9
```
**Output:**
```
34
```

## Zadatak 2: Problem s kovanicama
Problem koji smo rješavali u poglavlju [Pohlepni algoritmi](../pohlepni-algoritmi#zadatak-1-problem-s-kovanicama). Riješili smo problem pomoću pohlepnog algoritma koji uvijek bira najveći mogući novčić. Pohlepni algoritam radi, na primjer, kada kovanice su kovanice eura, ali u općem slučaju pohlepni algoritam ne daje nužno optimalno rješenje, primjerice ako su zadane kovanice $\{1,3,4}\$.

Zadatak je za unesenu listu denominacija kovanica $l$, $\{c_1, c_2, c_3,...,c_k\}$ i svotu $k$ pronaći minimalan broj kovanica potreban za stvoriti svotu $k$. Ako svotu nije moguće stvoriti pomoću zadanih kovanica ispisuje se $-1$.

**Input:**
U prvom redu unosi se cjeli broj $n$ koji označuje traženu svotu. 
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



## Zadatak 2: Knapsack
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
```

## Zadatak 3: Popločavanje
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
```

## Zadatak 4
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
```

## Zadatak 5
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
```

## Zadatak 6
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
```