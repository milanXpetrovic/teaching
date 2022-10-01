# Vjezbe 2: Vremenska složenost

## [Najveć zbroj podniza](https://en.wikipedia.org/wiki/Maximum_subarray_problem)


{: .important }
> 📘 Zadatak
>
> A paragraph with a custom title callout


**The Cauchy-Schwarz Inequality**
$$\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)$$

This sentence uses `$` delimiters to show math inline: $\sqrt{3x-1}+(1+x)^2$


Zadan je niz od $n$ brojeva, naš zadatak je izračunati najveći zbroj podniza , tj. najveći mogući zbroj niza uzastopnih vrijednosti u nizu.

U zadanom nizu:

|     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2   | -3  | 1   | 5   | -2  | 3   | 5   | -2   |

Najveći zbroj podniza iznosi **12**.

|     |     |       |       |        |       |       |     |
| --- | --- | ----- | ----- | ------ | ----- | ----- | --- |
| 2   | -3  | **1** | **5** | **-2** | **3** | **5** | -2  |



**Primjer rješenja u c++**
```cpp
int best = 0;
for (int a = 0; a < n; a++) {
	for (int b = a; b < n; b++) {
		int sum = 0;
		for (int k = a; k <= b; k++) {
			sum += array[k];
		}
	best = max(best,sum);
	}
}
cout << best << "\n";
```

### Zadatak 1.1

Pomoću prethodnog primjera danog u C++ napišite Python kod koji traži vrijednost najvećeg zbroja podniza i ima složenost od $O(n^3)$.

**Input:**
Lista $l$ koja sadržava $n$ cjelih brojeva $k$ $$( -\infty < k < \infty)$$

**Output:**
Iznos maksimalnog zbroja podniza, cjeli broj.

#### Primjer

**Input:**
```
-1 2 4 -3 5 2 -5 2
```

**Output:**
```
10
```

### Zadatak 1.2

Optimizirajte prethodni algoritam tako da njegova složenost iznosi $O(n^2)$.


### Zadatak 1.3

Ovaj problem moguće je i riješiti samo jednom iteracijom kroz listu, odnosno sa složenosti $O(n)$ pomoću [Kadane algoritma](https://en.wikipedia.org/wiki/Joseph_Born_Kadane).

Ideja je izračunati, za svaku poziciju niza, maksimalni zbroj podniza koji završava na toj poziciji. Nakon ovoga potrebno je pronaći maksimalnu vrijednost od tih zbrojeva. Ako razmotrimo podproblem pronalaženja podniza maksimalnog zbroja koji završava na položaju $k$. Postoje dvije mogućnosti:
1. Podniz sadrži samo element na poziciji $k$.
2. Podniz se sastoji od podniza koji završava na poziciji $k-1$, nakon čega slijedi
element na poziciji $k$.

U drugom slučaju, budući da želimo pronaći podniz s maksimalnim zbrojem, podniz koji završava na poziciji $k-1$ također treba imati maksimalni zbroj. Tako, problem možemo učinkovito riješiti izračunavanjem maksimalnog zbroja podniza za svaku krajnju poziciju s lijeva na desno.

**Implementacije navedenog algoritma:**

```cpp
int best = 0, sum = 0;
for (int k = 0; k < n; k++) {
	sum = max(array[k],sum+array[k]);
	best = max(best,sum);
}
cout << best << "\n";
```

Napišite Python kod koji traži najveć zbroj podniza sa vremenskom složenosti $O(n^2)$.

### Zadatak 2

Kreirajte funkciju koja generira listu $l$ čiji su elementi nasumično odabrani cjeli brojevi $k$ $( - 10 < k < 10)$.



**Input**
Duljina liste $n$, određuje broj elemenata u listi.

**Output**
Lista $l$ koja sadržava $n$ elemenata.

#### Primjer

**Input:**
```
15
```

**Output:**
```
[-1, 4, -9, -2, -1, 3, -6, 5, 8, 0, 3, -8, 6, 7, 3]
```

**Dodatak:**

Za generiranje pseudo-random brojeva možete koristi Python modul [random](https://docs.python.org/3/library/random.html).

### Zadatak 3

Usporedite brzine izvođenja prethodno definiranih algoritama.

**Input**
Duljina liste $$n$$, određuje broj elemenata u listi.

**Output**
Vremena $t_1$, $t_2$ i $t_3$ koja označavaju vrijeme izvođenja algoritama.

**Input:**
```
1000
```

**Output:**
```
9.2702
0.0670
0.0010
```

**Dodatak**
Za mjerenje vremena izvođenja programa možete koristiti Python modul [time](https://docs.python.org/3/library/time.html).