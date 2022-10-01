# Vježbe 4: Greedy algorithms

A greedy algorithm constructs a solution to the problem by always making a choice that looks the best at the moment. A greedy algorithm never takes back its choices, but directly constructs the final solution. For this reason, greedy algorithms are usually very efficient.
The difficulty in designing greedy algorithms is to find a greedy strategy that always produces an optimal solution to the problem. The locally optimal choices in a greedy algorithm should also be globally optimal. It is often difficult to argue that a greedy algorithm works.

- [ ] Uvod: Problem s kovanicama

## Uvod : Problem s kovanicama

Razmatramo problem u kojem nam je dan skup kovanica $\{c_1, c_2, c_3,...,c_k\}$ i naš je zadatak oblikovati svotu novca $n$, pritom svaku kovanicu možemo koristiti koligo kod puta želimo. Koji je minimalan broj potrebnih kovanica?

Na primjer zadane su kovanice : $\{1, 2, 5, 10, 20, 50, 100, 200\}$. Zadatak je pomoću danih kovanica kreirati iznos $n$

Napišite program koji kao ulaz prima cjeli broj $n$ a kao rješenje ispisuje kovanice pomoću koji se može kreirati broj $n$, cilj programa je koristiti najmanji mogući broj kovanica, odnosno pohlepni pristup.

**Input:**
Cjeli broj $n$ $(1 <= n <= 10000)$ koji označava traženu sumu.

**Output:**
Lista vrijednosti na kovanicama $\{c_1, c_2, c_3,...,c_k\}$ na kovanicama.


**Input:**
```
530
```

**Output:**
```
200 200 100 20 10
```

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

## Uvod 2: Kompresija podataka

| character | codeword |
| --------- | -------- |
| A         | 00       |
| B         | 01       |
| C         | 10       |
| D         | 11       |

**Input:**
AABACDACA

**Output:**
000001001011001000


## Zadatak 1:

Organiziraj upis predmeta tako da student upiše maksimalan broj predmeta bez preklapanja.


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

## Zadatak 2

https://codeforces.com/problemset/problem/50/A



## Zadatak 3