---
layout: default
parent: PRSP
nav_order: 17
nav_exclude: false
---

# OVO NIJE SLUZBENA SKRIPTA

# Rješenja zadataka s vježbi

## Utils

```cpp
#include <iostream>
#include <vector>
#include <climits>
using namespace std;
```

```cpp
int main() {
    int n;
    
    cout << "Unesite broj elemenata: ";
    cin >> n;

    vector<int> nums(n);
    cout << "Unesite elemente: ";
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
```

## Uvod

- [Codeforces: Watermelon](https://codeforces.com/problemset/problem/4/A)

```cpp
#include <iostream>
using namespace std;

int main() {

    int n;
    cin>> n;
    if (n == 2 || n % 2 != 0){
        cout << "NO" << endl;
    }
    else
    {
        cout << "YES" << endl;
    }

    return 0;
}
```

- [CSES: Weird Algorithm](https://cses.fi/problemset/task/1068)

```cpp
#include <iostream>
using namespace std;

int main() {
    long long n;
    cin>> n;
    
    while (n > 0){
        if (n == 1){
            cout << n << " ";
            break;
        }
        if (n % 2 != 0){
            cout << n << " ";
            n = (n * 3) + 1;
            }
        else{
            cout << n << " ";
            n = n / 2;
            }
        }
    return 0;
}
```

- [Codeforces: Way Too Long Words](https://codeforces.com/problemset/problem/71/A)

```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
    int n;
    cin >> n; 
    for (int i = 0; i < n; ++i) {
        string word;
        cin >> word; 
        
        if (word.length() > 10) {
            cout << word[0] << word.length() - 2 << word[word.length() - 1] << endl;
        } 
        else {
            cout << word << endl;
        }
    }
    return 0;
}
```

## Vremenska složenost

### [Najveći zbroj podniza](./vjezbe-sadrzaj/vremenska-slozenost.md#najveći-zbroj-podniza)

### [Zadatak 1: $O(n^3)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-1-složenost)

```cpp

int maxSum = INT_MIN;
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        int currentSum = 0;
        for (int k = i; k <= j; k++) {
            currentSum += numbers[k];
        }
        if (currentSum > maxSum) {
            maxSum = currentSum;
        }
    }
}
cout << maxSum << endl;

```

### [Zadatak 2: $O(n^2)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-2-složenost)

```cpp
int maxSum = INT_MIN;
for (int i = 0; i < n; i++) {
    int currentSum = 0;
    for (int j = i; j < n; j++) {
        currentSum += nums[j];
        if (currentSum > maxSum) {
            maxSum = currentSum;
        }
    }
}
```

### [Zadatak 3 $O(n)$ složenost](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-3-složenost)

```cpp
#include <climits>

int maxSum = INT_MIN;
int currentSum = 0;
for (int i = 0; i < n; i++) {
    currentSum += nums[i];
    if (currentSum > maxSum) {
        maxSum = currentSum;
    }
    if (currentSum < 0) {
        currentSum = 0;
    }
}
```

### [Zadatak 4: Lista nasumičnih brojeva](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-4-lista-nasumičnih-brojeva)

```cpp
#include <vector>
#include <cstdlib>
#include <ctime> 

vector<int> generateRandomNumbers(int n) {
    vector<int> nums(n);
    srand(time(0));
    for (int i = 0; i < n; i++) {
        nums[i] = (rand() % 31) - 15;
    }

    return nums;
}
```

### [Zadatak 5: Mjerenje brzine izvođenja](./vjezbe-sadrzaj/vremenska-slozenost.md#zadatak-5-mjerenje-brzine-izvođenja)

```cpp
#include <chrono>

auto start = high_resolution_clock::now();
int maxSum = findMaxSubarraySum(nums);
auto stop = high_resolution_clock::now();
auto duration = duration_cast<microseconds>(stop - start);
cout << "Maximum Subarray Sum: " << maxSum << endl;
cout << "Vrijeme izvodenja: " << duration.count() << " mikrosekundie" << endl;
```

## [Potpuna pretraga](./vjezbe-sadrzaj/potpuno-pretrazivanje.md)

### Zadatak 1: Generiranje podskupova

```cpp
#include <iostream>
#include <vector>

using namespace std;

void generateSubsets(int k, int n, vector<int>& subset, vector<vector<int>>& result) {
    if (k == n) {
        result.push_back(subset);
        return;
    }

    generateSubsets(k + 1, n, subset, result);
    subset.push_back(k);
    generateSubsets(k + 1, n, subset, result);
    subset.pop_back(); 
}

vector<vector<int>> getAllSubsets(int n) {
    vector<vector<int>> result;
    vector<int> subset;
    generateSubsets(0, n, subset, result);
    return result;
}

int main() {
    int n;
    
    cout << "Unesite broj elemenata: ";
    cin >> n;

    vector<vector<int>> subsets = getAllSubsets(n);
    cout << "All possible subsets:" << endl;

    for (const auto& subset : subsets) {
        cout << "[ ";
        for (int num : subset) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }

    return 0;
}

```

### Zadatak 3: K-sum binarno

```cpp
#include <iostream>
#include <vector>

using namespace std;

bool findSubsetWithSum(const vector<int>& l, int k) {
    int n = l.size();
    int totalSubsets = 1 << n; // 2^n podskupova

    // Iteriramo kroz sve moguće podskupove
    for (int i = 0; i < totalSubsets; ++i) {
        vector<int> subset;
        int currentSum = 0;

        // Generiramo podskup za trenutni binarni broj
        for (int j = 0; j < n; ++j) {
            if (i & (1 << j)) {
                subset.push_back(l[j]);  // Dodaj l[j] u podskup
                currentSum += l[j];      // Dodaj u trenutnu sumu
            }
        }

        // Provjeravamo ako suma podskupa odgovara traženoj sumi k
        if (currentSum == k) {
            cout << "Podlista čija suma iznosi " << k << ": ";
            for (int num : subset) {
                cout << num << " ";
            }
            cout << endl;
            return true; // Pronašli smo odgovarajući podskup
        }
    }

    cout << "Nema podliste čija suma iznosi " << k << endl;
    return false; // Nema podskupa koji odgovara sumi
}

int main() {
    int k, n;
    
    // Unos tražene sume k
    cout << "Unesite traženu sumu k: ";
    cin >> k;

    // Unos broja elemenata u listi n
    cout << "Unesite broj elemenata u listi: ";
    cin >> n;

    vector<int> l(n);
    
    // Unos liste elemenata
    cout << "Unesite elemente liste: ";
    for (int i = 0; i < n; ++i) {
        cin >> l[i];
    }

    // Pozivanje funkcije za traženje podliste s traženom sumom
    findSubsetWithSum(l, k);

    return 0;
}
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


## Zadatak 2: Binarna reprezentacija

## Pomaknuti ovaj zdatak u bit manipulation

```cpp
#include <iostream>
#include <vector>

using namespace std;

vector<vector<int>> getAllSubsets(int n) {
    vector<vector<int>> result;
    
    // There are 2^n subsets
    int totalSubsets = 1 << n; // Equivalent to 2^n

    for (int i = 0; i < totalSubsets; ++i) {
        vector<int> subset;
        
        for (int j = 0; j < n; ++j) {
            if (i & (1 << j)) {
                subset.push_back(j); 
            }
        }
        
        result.push_back(subset);
    }

    return result;
}

int main() {
    int n;
    cout << "Enter the value of n: ";
    cin >> n;

    vector<vector<int>> subsets = getAllSubsets(n);

    cout << "All possible subsets:" << endl;
    for (const auto& subset : subsets) {
        cout << "[ ";
        for (int num : subset) {
            cout << num << " ";
        }
        cout << "]" << endl;
    }

    return 0;
}
```


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
