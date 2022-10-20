---
layout: default
parent: PRSP
nav_order: 5
nav_exclude: true
---


# Vježbe 5: Dinamičko programiranje


## SRTBOT
SRTBOT - Paradigma za dizajniranje rekurzivnih algoritama:

- Subproblem definition - problem koji rješavamo rastavljamo na jednostavnije podprobleme (Subproblem definition). 
- Relate - Povezanost različitih rješenja podproblema s nekom rekurzivnom strukturom (Recurrence relation).
- Topological order- Prikažemo li rješavanje problema kao graf, onda će podproblemi biti čvorovi u tom grafu, a veze su ovisnosti među njima. Ono što želimo postići je da je naš graf Usmjeren ackilički graf (DAG).
- Base case - Zadan osnovni slučaj u rekurzivnoj strukturi.
- Original problem - Želimo riješiti orginalni problem pomoću rastavljanja na podprobleme.
- Time analysis - Analiza vremena izvodđenja.


**Primjer: Merge sort**

Želimo sortirati polje $A$, tako da sortiramo neka podpolja $A[i:j]$. Time će podproblem biti definiran kao $S(i,j)$ u orginalanom problemu $S(0, n)$ gdje je $n$ veličina polja $A$. Povezanost podproblema s rekurzivnom strukturom nam je definirana kao $S(i,j) = \textrm{merge}(S(i,m), S(m,j))$. Gdje spajamo (*merge*) dva sortirana podpolja $S(i,m)$ i $S(m,j)$ gdje je $m$ središnji element koji se dobije pomoću $m= \lfloor \frac{i+j}{2} \rfloor$. Iz ovoga proizlazi da ako damo riješenja za dva manja podproblema konstruirati ćemo rješenje za podproblem  $S(i,j)$, pritom si moramo osigurati da je podproblem  $S(i,j)$ veći od podproblema $S(i,m)$ i $S(m,j)$ da izbjegnemo beskonačno izvođenje algoritma, ovo si osiguravamo povećanjem veličine podpolja kojeg sortiramo pomoću $j-i$.

- Subproblems: $S(i,j)$ = sorted array on $A[i:j]$
- Relate: $S(i,j) = merge(S(i,m), S(m,j))$ where is $m= \lfloor \frac{i+j}{2} \rfloor$
- Topological order: increasing $j-i$
- Base case: $S(i,j)=\left[\;\;\right]$
- Original problem: $S(0, n)$
- Time analysis: $T(n) = 2T(\frac{n}{2})+O(n)=O(n \log n)$


## Zadatak 1: Fibonacci


## Zadatak 1: Problem s kovanicama
**Input:**
**Output:**
### Primjer
**Input:**
```
```
**Output:**
```
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