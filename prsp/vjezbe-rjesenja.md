---
layout: default
parent: PRSP
nav_order: 17
nav_exclude: false
---

# Rješenja zadataka s vježbi

## Vremenska složenost

### [Najveći zbroj podniza](./vjezbe-sadrzaj/vremenska-slozenost.md#najveći-zbroj-podniza)

```python
```

### [Zadatak 1: $O(n^3)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-1-složenost)

```python
```

### [Zadatak 2: $O(n^2)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-2-složenost)

```python
```

### [Zadatak 3 $O(n)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-3-složenost)

```python
```

### [Zadatak 4: Lista nasumičnih brojeva](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-4-lista-nasumičnih-brojeva)

```python
```

### [Zadatak 5: Mjerenje brzine izvođenja](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-5-mjerenje-brzine-izvođenja)

```python
```

## [Potpuna pretraga](./vjezbe-sadrzaj/potpuno-pretrazivanje.md)

### Zadatak 1: Generiranje podskupova

```python
def search(k, n, subset):
    if k == n:
        print(subset)

    else:
        search(k+1, n, subset)
        subset.append(k)
        search(k+1, n, subset)
        subset.pop()

## primjer za n=3
n = 3 
subset = []
search(0, n, subset)
```

## Zadatak 2: Binarna reprezentacija

```python
bins = [format(i, "b").zfill(n) for i in range(2**n)]
```

### Zadatak 3: K-sum binarno

```python
bins = [format(i, "b").zfill(n) for i in range(2**n)]

for sel in bins:
    total = 0
    
    for i, b in enumerate(sel):
        if b=="1":
            total+=l[i]

    if total == k:
        for i, b in enumerate(sel):
            if b=="1":
                print(l[i])
```

### Zadatak 4: K-sum Meet in the middle

```python
```

### Zadatak 5: Različite znamenke

```python
```

## Pohlepni algoritmi

### Zadatak 1: Problem s kovanicama

```python
n = int(input())

def find_largest_close(n):
    coins = [1, 2, 5, 10, 20, 50, 100, 200]
    largest = False
    for c in coins:
        if c <= n:
            largest = c

    return largest


while True:
    v = find_largest_close(n)
    if not v:
        break
    else:
        print(v, end=" ")
        n-=v 
```

### Zadatak 2: Kompresija podataka

```python

```

### Zadatak 3:Zakazivanje aktivnosti

```python
def myFoo(e):
    return e[1]

cls_l = [[8, 9],
        [11, 13],
        [9, 10],
        [8, 14],
        [15, 17],
        [10, 12],
        [8, 10]
        ]

# lista.sort(key=myFoo)
# lista.sort(key = lambda x: x[1])

predmeti.sort(key = lambda x: (x[1], x[0]))

c = 0 # najveci broj mogucih predmeta
enroll = [] #predmeti
end = -1 #zadnje vrijeme

for cls in cls_l:
    if end <= cls[0]:
        end = cls[1]
        count+=1
        enroll.append(cls)
```

## Dinamičko programiranje

## Zadatak 1: Fibonacci

```python
def fib_rec(n):
    in n <= 1:
        return n
    else:
        return fib_rec(n-1) + fib_rec(n-2)
```

```python
def fib_dyn(n):
    mem = [0, 1]
    for i in range(2, n+1):
        mem.append(mem[i-1]+mem[i-2])
    return(mem[n])
```

```python
def fib_dyn_opti(n):
    a = 0
    b = 1

    if n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n+1):
            c = a+b
            a = b
            b = c
        return b
```

### Zadatak 2: Problem s kovanicama

```python

```

### Zadatak 3: Stube

```python

```

### Zadatak 4: Stube s troškovima

```python

```

## Bit manipulation

### Zadatak 1: Element bez ponavljanja

```python
l = [int(x) for x in input().split(" ")]
res = 0
for b in l:
    res ^= b
print(res)
```

### Zadatak 2: Hammingova težina

```python
s = input()
n = int(s,2)
print(n)

res = 0
while n:
    res += n%2
    n = n >> 1

print(res)
```

### Zadatak 3: Nedostaje broj

```python
l1 = [0, 1, 3]
l2 = list(range(0, len(l1)+1))
## solution 1
res = 0
for num in l1:
    res ^= num
for num in l2:
    res ^= num
print(res)

## solution 2
l1 = [0, 1, 3]
l2 = list(range(0, len(l1)+1))
print(sum(l2)-sum(l1))
```

## Grafovi

## Putovanje kroz graf

### Zadatak 1: Broj otoka

```python
```

### Zadatak 2: Najveći otok

```python
```
