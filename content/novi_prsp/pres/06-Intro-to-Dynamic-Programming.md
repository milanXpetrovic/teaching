---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Uvod u dinamičko programiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title -->

# Uvod u dinamičko programiranje

## Memoizacija, tabulacija i klasični problemi

---

# Sadržaj

1. **Uvod i teorija**
   - Što je DP?
   - Fibonaccijev niz: zašto nam treba DP?
   - Memoizacija vs. tabulacija
   - Recept za rješavanje DP problema
2. **Primjeri zadataka**
   - Problem novčića (minimizacija)
   - Problem novčića (broj načina)
   - Najduži rastući podniz (LIS)
   - Udaljenost uređivanja (Edit Distance)
3. **Analiza CSES zadataka** (detaljna rješenja)

---

# Što je dinamičko programiranje?

**Definicija:** Tehnika za rješavanje problema koji se mogu rastaviti na **preklapajuće podprobleme**.

Spaja najbolje od dva svijeta:

1. **Potpuna pretraga:** točnost (razmatra sve mogućnosti).
2. **Pohlepni algoritmi:** efikasnost.

Efikasnost postiže tako što **svaki podproblem računa samo jednom**.

**Dva ključna svojstva problema:**

1. **Optimalna podstruktura:** Rješenje problema sadrži optimalna rješenja manjih podproblema.
2. **Preklapajući podproblemi:** Isti podproblemi se ponavljaju više puta tijekom izračuna.

---

# Primjer: Fibonaccijev niz

Definicija: $F(n) = F(n-1) + F(n-2)$.

**Naivna rekurzija:**

```cpp
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

**Problem:** Eksponencijalna složenost $O(2^n)$.
Za `fib(5)` računamo `fib(3)` dvaput, `fib(2)` triput...

**Rješenje:** Pamtimo rezultate!

---

# Dva pristupa: top-down vs. bottom-up

**1. Memoizacija (top-down)**

Zadržavamo rekurziju, ali dodajemo "cache" (mapu ili polje).

- Ako je rješenje u cacheu $\to$ vratimo ga.
- Inače $\to$ izračunamo ga, **spremimo** i vratimo.

**2. Tabulacija (bottom-up)**

Iterativno rješavanje od najmanjih problema prema većima.

- Popunjavamo tablicu (polje) redom: `dp[0], dp[1], dp[2]...`
- Kada računamo `dp[i]`, vrijednosti `dp[i-1]` i `dp[i-2]` su već spremne.
- **Standard u natjecateljskom programiranju** (izbjegava overhead rekurzije).

---

# Fibonacci: memoizacija i tabulacija u kodu

```cpp
// Memoizacija (top-down)
long long memo[93];
bool done[93];

long long fib(int n) {
    if (n <= 1) return n;
    if (done[n]) return memo[n];   // Već izračunato
    done[n] = true;
    return memo[n] = fib(n-1) + fib(n-2);
}

// Tabulacija (bottom-up), za n >= 1
vector<long long> dp(n + 1);
dp[0] = 0; dp[1] = 1;
for (int i = 2; i <= n; i++) dp[i] = dp[i-1] + dp[i-2];
```

Obje verzije su $O(n)$. (`long long` drži $F(n)$ do $n = 92$.)

---

# Tabulacija korak po korak

Bazni slučajevi `dp[0] = 0`, `dp[1] = 1`, zatim `dp[i] = dp[i-1] + dp[i-2]` za `i = 2..n`.

<style scoped>
.dp-fib { margin-top: 0.4em; }
.dp-fib .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-fib .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-fib .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-fib .row { display: flex; gap: 8px; }
.dp-fib .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-fib .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-fib .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-fib .cell.todo .val { color: #b5b5b5; }
.dp-fib .cell.src { background: #f5db7e; }
.dp-fib .cell.best { background: #9fdc9f; }
.dp-fib .cell.cur { background: var(--main); color: #fff; }
.dp-fib .cell.cur .idx, .dp-fib .cell.cur .val { color: #fff; }
.dp-fib .line1, .dp-fib .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-fib .line1 { margin-top: 0.7em; }
.dp-fib .line2 { font-weight: bold; }
.dp-fib .ctrl { margin-top: 0.7em; }
.dp-fib button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-fib button:hover { background: var(--main); color: #fff; }
.dp-fib .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dp-fib" data-n="10">
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-fib').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var n = parseInt(root.dataset.n, 10);
    var R = makeRow(root.querySelector('.row'), n + 1);
    var F = [0, 1];
    while (F.length !== n + 1) F.push(F[F.length - 1] + F[F.length - 2]);
    var snaps = [{ upto: 1, i: -1, l1: 'Bazni slučajevi: dp[0] = 0, dp[1] = 1', l2: '' }];
    for (var i = 2; i !== n + 1; i++) {
      snaps.push({ upto: i, i: i,
        l1: 'dp[' + i + '] = dp[' + (i - 1) + '] + dp[' + (i - 2) + '] = ' + F[i - 1] + ' + ' + F[i - 2] + ' = ' + F[i],
        l2: i === n ? 'Gotovo: dp[' + n + '] = ' + F[n] + '   ✓' : '' });
    }
    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = 'cell';
        R.vals[k].textContent = Math.max(k, s.upto) === s.upto ? F[k] : '';
      });
      if (s.i !== -1) {
        R.cells[s.i - 1].classList.add('src');
        R.cells[s.i - 2].classList.add('src');
        R.cells[s.i].classList.add('cur');
      }
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 700); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Koraci u rješavanju DP problema

1. **Definiramo stanje (State):**
   Što jedinstveno opisuje podproblem?
   - Npr. `dp[i]` = rješenje za prvih $i$ elemenata.

2. **Pronađemo prijelaz (Transition):**
   Rekurzivna relacija koja povezuje stanje `dp[i]` s manjim stanjima.
   - Npr. `dp[i] = dp[i-1] + dp[i-2]`.

3. **Postavimo bazne slučajeve (Base cases):**
   Trivijalna rješenja koja znamo unaprijed.
   - Npr. `dp[0] = 0`.

4. **Odredimo redoslijed računanja:**
   Kako iterirati kroz stanja? (Obično `for i = 1 to n`.)

---

# Problem 1: Minimizacija novčića

**Zadatak:** Imamo novčiće $\{c_1, c_2, \dots, c_k\}$ i iznos $N$. Treba naći **minimalan** broj novčića za iznos $N$.

1. **Stanje:** `dp[x]` = min. broj novčića za iznos $x$.
2. **Prijelaz:** Zadnji dodani novčić može biti bilo koji $c_i$.
   $$ dp[x] = 1 + \min_{c \in coins} (dp[x - c]) $$
3. **Baza:** `dp[0] = 0` (0 novčića za iznos 0).
4. **Redoslijed:** $x$ od $1$ do $N$.

---

# Kod: Minimizacija novčića

```cpp
int main() {
    int n; cin >> n;
    vector<int> coins = {1, 3, 4};

    // Inicijaliziramo na "beskonačno"
    vector<int> dp(n + 1, 1e9);
    dp[0] = 0;

    for (int x = 1; x <= n; ++x) {
        for (int c : coins) {
            if (x - c >= 0) {
                dp[x] = min(dp[x], dp[x - c] + 1);
            }
        }
    }

    if (dp[n] == 1e9) cout << "Nemoguće\n";
    else cout << dp[n] << "\n";
}
```

**Složenost:** $O(N \cdot K)$.

---

# Minimizacija novčića korak po korak

`dp[0] = 0`, ostalo ∞. Zatim za svaki `x` i svaki novčić `c ≤ x`: `dp[x] = min(dp[x], dp[x − c] + 1)`.

<style scoped>
.dp-coins { margin-top: 0.4em; }
.dp-coins .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-coins .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-coins .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-coins .row { display: flex; gap: 8px; }
.dp-coins .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-coins .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-coins .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-coins .cell.todo .val { color: #b5b5b5; }
.dp-coins .cell.src { background: #f5db7e; }
.dp-coins .cell.best { background: #9fdc9f; }
.dp-coins .cell.cur { background: var(--main); color: #fff; }
.dp-coins .cell.cur .idx, .dp-coins .cell.cur .val { color: #fff; }
.dp-coins .line1, .dp-coins .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-coins .line1 { margin-top: 0.7em; }
.dp-coins .line2 { font-weight: bold; }
.dp-coins .ctrl { margin-top: 0.7em; }
.dp-coins button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-coins button:hover { background: var(--main); color: #fff; }
.dp-coins .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dp-coins" data-n="10" data-coins="1,3,4">
  <div class="chips">Novčići:</div>
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-coins').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var N = parseInt(root.dataset.n, 10);
    var coins = root.dataset.coins.split(',').map(Number);
    var chipsBox = root.querySelector('.chips');
    var chips = coins.map(function (c) { var s = mk('span', 'chip', c); chipsBox.appendChild(s); return s; });
    var R = makeRow(root.querySelector('.row'), N + 1);

    // Unaprijed izračunamo sve korake (jedan korak = jedan isprobani novčić)
    var dp = [0];
    for (var j = 1; j !== N + 1; j++) dp.push(Infinity);
    var snaps = [{ dp: dp.slice(), x: -1, ci: -1, src: -1,
      l1: 'Početno stanje: dp[0] = 0, sve ostalo ∞', l2: '' }];
    for (var x = 1; x !== N + 1; x++) {
      var cands = [];
      coins.forEach(function (c, ci) {
        var l1, src = -1;
        if (Math.min(c, x) === c) {             // novčić stane u iznos x
          src = x - c;
          var cand = dp[src] + 1;
          var better = cand !== dp[x] ? Math.min(cand, dp[x]) === cand : false;
          l1 = 'c = ' + c + ':  dp[' + x + ' − ' + c + '] + 1 = dp[' + src + '] + 1 = '
            + show(dp[src]) + ' + 1 = ' + show(cand)
            + (better ? '   → novi minimum' : '   → nije bolje');
          if (better) dp[x] = cand;
          cands.push(show(cand));
        } else {
          l1 = 'c = ' + c + ':  novčić je veći od ' + x + ', preskačemo';
        }
        var last = ci === coins.length - 1;
        var parts = cands.slice();
        if (!last) parts.push('…');
        var l2 = 'dp[' + x + '] = min(' + parts.join(', ') + ')';
        if (last) l2 += cands.length ? ' = ' + show(dp[x]) + '   ✓' : ' = ∞ (nemoguće)';
        snaps.push({ dp: dp.slice(), x: x, ci: ci, src: src, l1: l1, l2: l2 });
      });
    }
    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = s.dp[k] === Infinity ? 'cell todo' : 'cell';
        R.vals[k].textContent = show(s.dp[k]);
      });
      chips.forEach(function (ch, ci) { ch.className = ci === s.ci ? 'chip on' : 'chip'; });
      if (s.src !== -1) R.cells[s.src].classList.add('src');
      if (s.x !== -1) R.cells[s.x].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 600); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 2: Broj načina (Coin Combinations)

**Zadatak:** Isti novčići i iznos $N$. Na **koliko načina** možemo formirati iznos $N$? (Redoslijed je bitan: 1+3 i 3+1 su različiti.)

1. **Stanje:** `dp[x]` = broj načina za iznos $x$.
2. **Prijelaz:** Umjesto `min`, sada **zbrajamo** sve mogućnosti.
   $$ dp[x] = \sum_{c \in coins} dp[x - c] $$
3. **Baza:** `dp[0] = 1` (jedan način da dobijemo 0: ne uzmemo ništa).

---

# Kod: Broj načina

```cpp
int main() {
    int n; cin >> n;
    vector<int> coins = {1, 3, 4};
    long long MOD = 1e9 + 7;

    vector<long long> dp(n + 1, 0);
    dp[0] = 1;

    for (int x = 1; x <= n; ++x) {
        for (int c : coins) {
            if (x - c >= 0) {
                dp[x] = (dp[x] + dp[x - c]) % MOD;
            }
        }
    }
    cout << dp[n] << "\n";
}
```

**Razlika:** Samo smo promijenili `min` u `+` i maknuli `+1` (jer ne brojimo novčiće, već načine).
**Ako redoslijed nije bitan** (1+3 = 3+1): zamijenimo petlje, vanjska ide po novčićima, a unutarnja po iznosu.

---

# Broj načina korak po korak

`dp[0] = 1`, ostalo 0. Zatim za svaki `x` i svaki novčić `c ≤ x`: `dp[x] += dp[x − c]`.

<style scoped>
.dp-ways { margin-top: 0.4em; }
.dp-ways .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-ways .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-ways .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-ways .row { display: flex; gap: 8px; }
.dp-ways .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-ways .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-ways .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-ways .cell.todo .val { color: #b5b5b5; }
.dp-ways .cell.src { background: #f5db7e; }
.dp-ways .cell.best { background: #9fdc9f; }
.dp-ways .cell.cur { background: var(--main); color: #fff; }
.dp-ways .cell.cur .idx, .dp-ways .cell.cur .val { color: #fff; }
.dp-ways .line1, .dp-ways .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-ways .line1 { margin-top: 0.7em; }
.dp-ways .line2 { font-weight: bold; }
.dp-ways .ctrl { margin-top: 0.7em; }
.dp-ways button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-ways button:hover { background: var(--main); color: #fff; }
.dp-ways .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dp-ways" data-n="10" data-coins="1,3,4" data-prefix="c = ">
  <div class="chips">Novčići:</div>
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-ways').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var N = parseInt(root.dataset.n, 10);
    var coins = root.dataset.coins.split(',').map(Number);
    var pre = root.dataset.prefix;
    var chipsBox = root.querySelector('.chips');
    var chips = coins.map(function (c) { var s = mk('span', 'chip', c); chipsBox.appendChild(s); return s; });
    var R = makeRow(root.querySelector('.row'), N + 1);

    var dp = [1];
    for (var j = 1; j !== N + 1; j++) dp.push(0);
    var snaps = [{ dp: dp.slice(), upto: 0, x: -1, ci: -1, src: -1,
      l1: 'Početno stanje: dp[0] = 1 (prazan izbor), sve ostalo 0', l2: '' }];
    for (var x = 1; x !== N + 1; x++) {
      var terms = [];
      coins.forEach(function (c, ci) {
        var l1, src = -1;
        if (Math.min(c, x) === c) {
          src = x - c;
          dp[x] += dp[src];
          terms.push(String(dp[src]));
          l1 = pre + c + ':  dp[' + x + '] += dp[' + x + ' − ' + c + '] = dp[' + src + '] = '
            + dp[src] + '   → dp[' + x + '] = ' + dp[x];
        } else {
          l1 = pre + c + ':  ' + c + ' je veće od ' + x + ', preskačemo';
        }
        var last = ci === coins.length - 1;
        var parts = terms.slice();
        if (!last) parts.push('…');
        var l2 = 'dp[' + x + '] = ' + (parts.length ? parts.join(' + ') : '0');
        if (last) l2 += (terms.length === 1 ? '' : ' = ' + dp[x]) + '   ✓';
        snaps.push({ dp: dp.slice(), upto: x, x: x, ci: ci, src: src, l1: l1, l2: l2 });
      });
    }
    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = Math.max(k, s.upto) === s.upto ? 'cell' : 'cell todo';
        R.vals[k].textContent = s.dp[k];
      });
      chips.forEach(function (ch, ci) { ch.className = ci === s.ci ? 'chip on' : 'chip'; });
      if (s.src !== -1) R.cells[s.src].classList.add('src');
      if (s.x !== -1) R.cells[s.x].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 600); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 3: Najduži rastući podniz (LIS)

**Zadatak:** Treba naći duljinu najdužeg podniza (ne nužno uzastopnog) koji je strogo rastući.
Niz: `[6, 2, 5, 1, 7, 4, 8, 3]` $\to$ LIS: `[2, 5, 7, 8]` (duljina 4).

1. **Stanje:** `dp[i]` = duljina LIS-a koji **završava** na indeksu $i$.
2. **Prijelaz:** Gledamo sve prethodne elemente $j < i$. Ako je $A[j] < A[i]$, možemo produžiti niz.
   $$ dp[i] = 1 + \max(\{dp[j] \mid j < i, A[j] < A[i]\} \cup \{0\}) $$
3. **Rješenje:** $\max(dp[0] \dots dp[n-1])$.

---

# Kod: LIS ($O(N^2)$)

```cpp
int main() {
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;

    vector<int> dp(n, 1); // Svaki element je sam za sebe LIS duljine 1

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }

    // Tražimo maksimum u cijelom dp polju
    int ans = 0;
    for (int x : dp) ans = max(ans, x);
    cout << ans << "\n";
}
```

Za $n$ do $2 \cdot 10^5$ (CSES Increasing Subsequence) treba $O(N \log N)$ verzija s binarnim pretraživanjem.

---

# LIS korak po korak

Za svaki `i` gledamo sve `j` prije njega: ako je `a[j]` manji od `a[i]`, kandidat je `dp[j] + 1`.

<style scoped>
.dp-lis { margin-top: 0.4em; }
.dp-lis .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-lis .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-lis .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-lis .row { display: flex; gap: 8px; }
.dp-lis .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-lis .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-lis .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-lis .cell.todo .val { color: #b5b5b5; }
.dp-lis .cell.src { background: #f5db7e; }
.dp-lis .cell.best { background: #9fdc9f; }
.dp-lis .cell.cur { background: var(--main); color: #fff; }
.dp-lis .cell.cur .idx, .dp-lis .cell.cur .val { color: #fff; }
.dp-lis .line1, .dp-lis .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-lis .line1 { margin-top: 0.7em; }
.dp-lis .line2 { font-weight: bold; }
.dp-lis .ctrl { margin-top: 0.7em; }
.dp-lis button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-lis button:hover { background: var(--main); color: #fff; }
.dp-lis .hint { font-size: 16px; color: #6e6e6e; }
.dp-lis .aval { font-size: 26px; height: 40px; line-height: 40px; border-bottom: 1px solid #ccc; }
.dp-lis .lab { width: 70px; text-align: right; color: #6e6e6e; font-weight: bold; }
.dp-lis .lab .idx { border-bottom: 1px solid transparent; }
.dp-lis .lab .aval { font-size: 18px; border-bottom: 1px solid transparent; }
.dp-lis .lab .val { font-size: 18px; }
.dp-lis .cell.todo .val { color: #b5b5b5; }
</style>

<div class="dp-lis" data-arr="6,2,5,1,7,4,8,3">
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-lis').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var a = root.dataset.arr.split(',').map(Number);
    var n = a.length;
    var box = root.querySelector('.row');
    var lab = mk('div', 'lab');
    lab.appendChild(mk('div', 'idx', 'i'));
    lab.appendChild(mk('div', 'aval', 'a[i]'));
    lab.appendChild(mk('div', 'val', 'dp[i]'));
    box.appendChild(lab);
    var R = makeRow(box, n);
    R.cells.forEach(function (c, k) {
      c.insertBefore(mk('div', 'aval', a[k]), c.lastChild);
    });

    var dp = [], par = [];
    for (var t = 0; t !== n; t++) { dp.push(1); par.push(-1); }
    var snaps = [{ dp: dp.slice(), upto: -1, i: -1, j: -1, best: [],
      l1: 'Početno stanje: dp[i] = 1 za svaki i (svaki element je podniz duljine 1)', l2: '' }];
    for (var i = 0; i !== n; i++) {
      if (i === 0) {
        snaps.push({ dp: dp.slice(), upto: 0, i: 0, j: -1, best: [],
          l1: 'i = 0: nema prethodnih elemenata', l2: 'dp[0] = 1   ✓' });
        continue;
      }
      for (var j = 0; j !== i; j++) {
        var l1;
        var ok = a[j] !== a[i] ? Math.min(a[j], a[i]) === a[j] : false;
        if (ok) {
          var cand = dp[j] + 1;
          var better = cand !== dp[i] ? Math.max(cand, dp[i]) === cand : false;
          if (better) { dp[i] = cand; par[i] = j; }
          l1 = 'j = ' + j + ':  a[' + j + '] = ' + a[j] + ' manje od ' + a[i] + '  → dp[' + j + '] + 1 = ' + cand
            + (better ? ', novi maksimum' : ', nije bolje');
        } else {
          l1 = 'j = ' + j + ':  a[' + j + '] = ' + a[j] + ' nije manje od ' + a[i] + ', preskačemo';
        }
        snaps.push({ dp: dp.slice(), upto: i, i: i, j: j, best: [], l1: l1,
          l2: 'i = ' + i + ' (a[i] = ' + a[i] + '):  dp[' + i + '] = ' + dp[i] + (j === i - 1 ? '   ✓' : '') });
      }
    }
    var mx = 0;
    dp.forEach(function (v, k) { if (Math.max(v, dp[mx]) !== dp[mx]) mx = k; });
    var path = [];
    for (var p = mx; p !== -1; p = par[p]) path.unshift(p);
    snaps.push({ dp: dp.slice(), upto: n - 1, i: -1, j: -1, best: path,
      l1: 'Rješenje: max(dp) = ' + dp[mx],
      l2: 'Jedan najduži rastući podniz: ' + path.map(function (k) { return a[k]; }).join(', ') });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = Math.max(k, s.upto) === s.upto ? 'cell' : 'cell todo';
        R.vals[k].textContent = s.dp[k];
      });
      s.best.forEach(function (k) { R.cells[k].classList.add('best'); });
      if (s.j !== -1) R.cells[s.j].classList.add('src');
      if (s.i !== -1) R.cells[s.i].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 600); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Problem 4: Udaljenost uređivanja (Edit Distance)

**Zadatak:** Minimalan broj operacija (umetanje, brisanje, zamjena) da pretvorimo string $A$ u $B$.
$A=$ "LOVE", $B=$ "MOVIE" $\to$ 2 operacije.

1. **Stanje:** `dp[i][j]` = minimalan broj operacija za pretvaranje prvih $i$ znakova od $A$ u prvih $j$ znakova od $B$.
2. **Prijelaz:**
   - Ako je `A[i-1] == B[j-1]`: `dp[i][j] = dp[i-1][j-1]` (nema cijene).
   - Inače: `dp[i][j]` $= 1 + \min$ od:
     - `dp[i-1][j]` (brisanje)
     - `dp[i][j-1]` (umetanje)
     - `dp[i-1][j-1]` (zamjena)

---

# Kod: Edit Distance ($O(N \cdot M)$)

```cpp
vector<vector<int>> dp(n + 1, vector<int>(m + 1));

// Inicijalizacija: dp[i][0] = i (brisanja), dp[0][j] = j (umetanja)
for (int i = 0; i <= n; ++i) dp[i][0] = i;
for (int j = 0; j <= m; ++j) dp[0][j] = j;

for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
        if (A[i-1] == B[j-1]) {
            dp[i][j] = dp[i-1][j-1];
        } else {
            dp[i][j] = 1 + min({
                dp[i-1][j],    // Brisanje
                dp[i][j-1],    // Umetanje
                dp[i-1][j-1]   // Zamjena
            });
        }
    }
}
cout << dp[n][m] << "\n";
```

---

# Edit Distance korak po korak

↑ brisanje, ← umetanje, dijagonala = zamjena. Isti znakovi: prepišemo dijagonalu bez cijene.

<style scoped>
.dp-edit { margin-top: 0.4em; }
.dp-edit .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-edit .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-edit .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-edit .row { display: flex; gap: 8px; }
.dp-edit .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-edit .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-edit .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-edit .cell.todo .val { color: #b5b5b5; }
.dp-edit .cell.src { background: #f5db7e; }
.dp-edit .cell.best { background: #9fdc9f; }
.dp-edit .cell.cur { background: var(--main); color: #fff; }
.dp-edit .cell.cur .idx, .dp-edit .cell.cur .val { color: #fff; }
.dp-edit .line1, .dp-edit .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-edit .line1 { margin-top: 0.7em; }
.dp-edit .line2 { font-weight: bold; }
.dp-edit .ctrl { margin-top: 0.7em; }
.dp-edit button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-edit button:hover { background: var(--main); color: #fff; }
.dp-edit .hint { font-size: 16px; color: #6e6e6e; }
.dp-edit .tbl { display: grid; gap: 6px; }
.dp-edit .th { height: 42px; line-height: 42px; text-align: center; font-size: 24px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.dp-edit .th.hl { background: var(--main); color: #fff; }
.dp-edit .tc { height: 42px; line-height: 38px; text-align: center; font-size: 24px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-edit .tc.src { background: #f5db7e; }
.dp-edit .tc.cur { background: var(--main); color: #fff; }
</style>

<div class="dp-edit" data-a="LOVE" data-b="MOVIE">
  <div class="tbl"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-edit').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var A = root.dataset.a, B = root.dataset.b;
    var n = A.length, m = B.length;
    var tbl = root.querySelector('.tbl');
    tbl.style.gridTemplateColumns = 'repeat(' + (m + 2) + ', 62px)';
    var colH = [], rowH = [], T = [];
    tbl.appendChild(mk('div', 'th', ''));
    tbl.appendChild(mk('div', 'th', '∅'));
    colH.push(null);
    for (var j = 0; j !== m; j++) { var h = mk('div', 'th', B[j]); tbl.appendChild(h); colH.push(h); }
    for (var i = 0; i !== n + 1; i++) {
      var rh = mk('div', 'th', i === 0 ? '∅' : A[i - 1]);
      tbl.appendChild(rh); rowH.push(rh);
      var r = [];
      for (var j2 = 0; j2 !== m + 1; j2++) { var tc = mk('div', 'tc'); tbl.appendChild(tc); r.push(tc); }
      T.push(r);
    }

    var dp = [];
    for (var a1 = 0; a1 !== n + 1; a1++) {
      var rr = [];
      for (var b1 = 0; b1 !== m + 1; b1++) rr.push(a1 === 0 ? b1 : (b1 === 0 ? a1 : null));
      dp.push(rr);
    }
    function copy() { return dp.map(function (r) { return r.slice(); }); }
    var snaps = [{ dp: copy(), i: -1, j: -1, src: [],
      l1: 'Bazni slučajevi: dp[i][0] = i (brišemo sve), dp[0][j] = j (umećemo sve)', l2: '' }];
    for (var x = 1; x !== n + 1; x++) {
      for (var y = 1; y !== m + 1; y++) {
        var ca = A[x - 1], cb = B[y - 1], l1, src;
        if (ca === cb) {
          dp[x][y] = dp[x - 1][y - 1];
          src = [[x - 1, y - 1]];
          l1 = '„' + ca + '“ i „' + cb + '“ su jednaki  → prepišemo ↖ dp[' + (x - 1) + '][' + (y - 1) + '] = ' + dp[x][y];
        } else {
          var del = dp[x - 1][y], ins = dp[x][y - 1], rep = dp[x - 1][y - 1];
          dp[x][y] = 1 + Math.min(del, ins, rep);
          src = [[x - 1, y], [x, y - 1], [x - 1, y - 1]];
          l1 = '„' + ca + '“ i „' + cb + '“ su različiti  → 1 + min(↑ ' + del + ', ← ' + ins + ', ↖ ' + rep + ')';
        }
        var fin = x === n ? y === m : false;
        snaps.push({ dp: copy(), i: x, j: y, src: src, l1: l1,
          l2: 'dp[' + x + '][' + y + '] = ' + dp[x][y] + (fin ? '   ✓ (udaljenost „' + A + '“ → „' + B + '“)' : '') });
      }
    }
    function draw(s) {
      T.forEach(function (r, i) {
        r.forEach(function (c, j) {
          c.className = 'tc';
          c.textContent = s.dp[i][j] === null ? '' : s.dp[i][j];
        });
      });
      rowH.forEach(function (h) { h.className = 'th'; });
      colH.forEach(function (h) { if (h) h.className = 'th'; });
      s.src.forEach(function (p) { T[p[0]][p[1]].classList.add('src'); });
      if (s.i !== -1) {
        T[s.i][s.j].classList.add('cur');
        rowH[s.i].classList.add('hl');
        colH[s.j].classList.add('hl');
      }
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 700); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

# Odgovarajući CSES zadaci

- **[Minimizing Coins](https://cses.fi/problemset/task/1634):** Problem 1.
- **[Coin Combinations I](https://cses.fi/problemset/task/1635):** Problem 2 (redoslijed je bitan).
- **[Coin Combinations II](https://cses.fi/problemset/task/1636):** Problem 2 (redoslijed nije bitan).
- **[Increasing Subsequence](https://cses.fi/problemset/task/1145):** Problem 3 ($O(N \log N)$).
- **[Edit Distance](https://cses.fi/problemset/task/1639):** Problem 4.

---

<!-- _class: title -->
# Analiza: CSES zadaci

## Primjena naučenog na konkretnim problemima

---

<!-- _class: title -->
# 1. Dice Combinations (CSES)

## Varijacija problema novčića

---

# Analiza: Dice Combinations (1/2)

**Problem:**
Želimo dobiti zbroj $N$ bacanjem kocke (vrijednosti 1-6). Na koliko načina to možemo učiniti?
Npr. $N=3$: `1+1+1`, `1+2`, `2+1`, `3`. (Ukupno 4.)

**Intuicija:**
Zamislimo da želimo dobiti zbroj $i$. Koje je bilo **zadnje** bacanje?
Moglo je biti 1, 2, 3, 4, 5 ili 6.

- Ako je zadnje bacanje bilo **1**, prethodni zbroj je morao biti $i-1$.
- Ako je zadnje bacanje bilo **2**, prethodni zbroj je morao biti $i-2$.
- ...
- Ako je zadnje bacanje bilo **6**, prethodni zbroj je morao biti $i-6$.

Ukupan broj načina za $i$ je zbroj načina za sva ta prethodna stanja.

---

# Analiza: Dice Combinations (2/2)

**Definicija DP stanja:**
`dp[i]` = broj načina da dobijemo zbroj $i$.

**Rekurzivna veza (prijelaz):**
$$ dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6] $$
*(Uzimamo u obzir samo članove čiji je indeks $\ge 0$.)*

**Bazni slučaj:**
`dp[0] = 1`. Postoji točno jedan način da dobijemo zbroj 0 (tako da kocku ne bacimo nijednom).

---

# Implementacija: Dice Combinations

```cpp
int n; cin >> n;
vector<long long> dp(n + 1, 0);
dp[0] = 1;
long long MOD = 1e9 + 7;

for (int i = 1; i <= n; ++i) {
    // Pokušavamo svaku moguću vrijednost kocke (1 do 6)
    for (int j = 1; j <= 6; ++j) {
        if (i - j >= 0) {
            dp[i] = (dp[i] + dp[i - j]) % MOD;
        }
    }
}
cout << dp[n] << "\n";
```

**Složenost:** $O(N)$ (unutarnja petlja je konstantna, vrti se 6 puta).

---

# Dice Combinations korak po korak

`dp[0] = 1`. Za svaki zbroj `i` i svako zadnje bacanje `k = 1..6` (ako je `k ≤ i`): `dp[i] += dp[i − k]`.

<style scoped>
.dp-dice { margin-top: 0.4em; }
.dp-dice .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-dice .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-dice .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-dice .row { display: flex; gap: 8px; }
.dp-dice .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-dice .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-dice .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-dice .cell.todo .val { color: #b5b5b5; }
.dp-dice .cell.src { background: #f5db7e; }
.dp-dice .cell.best { background: #9fdc9f; }
.dp-dice .cell.cur { background: var(--main); color: #fff; }
.dp-dice .cell.cur .idx, .dp-dice .cell.cur .val { color: #fff; }
.dp-dice .line1, .dp-dice .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-dice .line1 { margin-top: 0.7em; }
.dp-dice .line2 { font-weight: bold; }
.dp-dice .ctrl { margin-top: 0.7em; }
.dp-dice button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-dice button:hover { background: var(--main); color: #fff; }
.dp-dice .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dp-dice" data-n="8" data-coins="1,2,3,4,5,6" data-prefix="bacanje ">
  <div class="chips">Kocka:</div>
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-dice').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var N = parseInt(root.dataset.n, 10);
    var coins = root.dataset.coins.split(',').map(Number);
    var pre = root.dataset.prefix;
    var chipsBox = root.querySelector('.chips');
    var chips = coins.map(function (c) { var s = mk('span', 'chip', c); chipsBox.appendChild(s); return s; });
    var R = makeRow(root.querySelector('.row'), N + 1);

    var dp = [1];
    for (var j = 1; j !== N + 1; j++) dp.push(0);
    var snaps = [{ dp: dp.slice(), upto: 0, x: -1, ci: -1, src: -1,
      l1: 'Početno stanje: dp[0] = 1 (ne bacimo ništa), sve ostalo 0', l2: '' }];
    for (var x = 1; x !== N + 1; x++) {
      var terms = [];
      coins.forEach(function (c, ci) {
        var l1, src = -1;
        if (Math.min(c, x) === c) {
          src = x - c;
          dp[x] += dp[src];
          terms.push(String(dp[src]));
          l1 = pre + c + ':  dp[' + x + '] += dp[' + x + ' − ' + c + '] = dp[' + src + '] = '
            + dp[src] + '   → dp[' + x + '] = ' + dp[x];
        } else {
          l1 = pre + c + ':  ' + c + ' je veće od ' + x + ', preskačemo';
        }
        var last = ci === coins.length - 1;
        var parts = terms.slice();
        if (!last) parts.push('…');
        var l2 = 'dp[' + x + '] = ' + (parts.length ? parts.join(' + ') : '0');
        if (last) l2 += (terms.length === 1 ? '' : ' = ' + dp[x]) + '   ✓';
        snaps.push({ dp: dp.slice(), upto: x, x: x, ci: ci, src: src, l1: l1, l2: l2 });
      });
    }
    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = Math.max(k, s.upto) === s.upto ? 'cell' : 'cell todo';
        R.vals[k].textContent = s.dp[k];
      });
      chips.forEach(function (ch, ci) { ch.className = ci === s.ci ? 'chip on' : 'chip'; });
      if (s.src !== -1) R.cells[s.src].classList.add('src');
      if (s.x !== -1) R.cells[s.x].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 450); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

<!-- _class: title -->
# 2. Removing Digits (CSES)

## Pohlepno ili DP?

---

# Analiza: Removing Digits (1/2)

**Problem:**
Imamo broj $N$. U jednom koraku možemo oduzeti bilo koju znamenku koja se trenutno nalazi u broju.
Cilj: doći do 0 u **minimalnom** broju koraka.
Npr. $27 \to 27-7=20 \to 20-2=18 \dots$

**Intuicija:**
Ovo je problem minimizacije. Iz trenutnog stanja (broj $i$) možemo prijeći u više novih stanja.
Ako broj $i$ ima znamenke $\{d_1, d_2, \dots\}$, možemo prijeći u stanja $i-d_1, i-d_2, \dots$.
Budući da tražimo minimum, želimo odabrati potez koji nas najbrže vodi do 0.

---

# Analiza: Removing Digits (2/2)

**Pristupi:**

1. **Pohlepni pristup:** Uvijek oduzmemo **najveću** znamenku.
   - Za ovaj problem pohlepno daje optimalno rješenje, ali dokaz nije trivijalan.
   - Oprez: intuicija "najbrže smanjujemo broj" ista je ona koja je pala kod novčića $\{1, 3, 4\}$.

2. **DP pristup (sigurniji i općenitiji):**
   - **Stanje:** `dp[i]` = min. broj koraka od $i$ do 0.
   - **Prijelaz:** `dp[i] = 1 + min(dp[i - d])` za svaku znamenku $d$ u broju $i$.
   - **Baza:** `dp[0] = 0`.

---

# Implementacija: Removing Digits (DP)

```cpp
int n; cin >> n;
vector<int> dp(n + 1, 1e9); // Inicijalizacija na beskonačno
dp[0] = 0;

for (int i = 1; i <= n; ++i) {
    // Izdvajanje znamenki broja i
    int temp = i;
    while (temp > 0) {
        int digit = temp % 10;
        temp /= 10;

        // Prijelaz: ako oduzmemo 'digit', dolazimo u stanje 'i - digit'
        // i treba nam 1 korak više nego za to stanje.
        if (digit > 0) {
            dp[i] = min(dp[i], dp[i - digit] + 1);
        }
    }
}
cout << dp[n] << "\n";
```

---

# Removing Digits korak po korak

`dp[0] = 0`, ostalo ∞. Za svaki `i` i svaku znamenku `d` broja `i` (osim 0): `dp[i] = min(dp[i], dp[i − d] + 1)`.

<style scoped>
.dp-digits { margin-top: 0.4em; }
.dp-digits .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-digits .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-digits .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-digits .row { display: flex; gap: 8px; }
.dp-digits .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-digits .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-digits .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-digits .cell.todo .val { color: #b5b5b5; }
.dp-digits .cell.src { background: #f5db7e; }
.dp-digits .cell.best { background: #9fdc9f; }
.dp-digits .cell.cur { background: var(--main); color: #fff; }
.dp-digits .cell.cur .idx, .dp-digits .cell.cur .val { color: #fff; }
.dp-digits .line1, .dp-digits .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-digits .line1 { margin-top: 0.7em; }
.dp-digits .line2 { font-weight: bold; }
.dp-digits .ctrl { margin-top: 0.7em; }
.dp-digits button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-digits button:hover { background: var(--main); color: #fff; }
.dp-digits .hint { font-size: 16px; color: #6e6e6e; }
.dp-digits .row { flex-wrap: wrap; row-gap: 10px; }
.dp-digits .cell { width: 72px; }
.dp-digits .val { font-size: 26px; height: 40px; line-height: 40px; }
.dp-digits .chips { min-height: 1.6em; }
</style>

<div class="dp-digits" data-n="27">
  <div class="chips"></div>
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-digits').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var N = parseInt(root.dataset.n, 10);
    var chipsBox = root.querySelector('.chips');
    var R = makeRow(root.querySelector('.row'), N + 1);
    var dp = [0], ch = [0];
    for (var j = 1; j !== N + 1; j++) { dp.push(Infinity); ch.push(0); }
    var snaps = [{ dp: dp.slice(), x: -1, src: -1, digs: [], di: -1, best: [],
      l1: 'Početno stanje: dp[0] = 0, sve ostalo ∞', l2: '' }];
    for (var i = 1; i !== N + 1; i++) {
      var digs = [], t = i;
      while (t !== 0) { digs.unshift(t % 10); t = Math.floor(t / 10); }
      var cands = [];
      digs.forEach(function (d, di) {
        var l1, src = -1;
        if (d === 0) {
          l1 = 'znamenka 0: ne mijenja broj, preskačemo';
        } else {
          src = i - d;
          var cand = dp[src] + 1;
          var better = cand !== dp[i] ? Math.min(cand, dp[i]) === cand : false;
          if (better) { dp[i] = cand; ch[i] = d; }
          l1 = 'znamenka ' + d + ':  dp[' + i + ' − ' + d + '] + 1 = dp[' + src + '] + 1 = ' + show(dp[src]) + ' + 1 = '
            + show(cand) + (better ? '   → novi minimum' : '   → nije bolje');
          cands.push(show(cand));
        }
        var last = di === digs.length - 1;
        var parts = cands.slice();
        if (!last) parts.push('…');
        snaps.push({ dp: dp.slice(), x: i, src: src, digs: digs, di: di, best: [], l1: l1,
          l2: 'dp[' + i + '] = min(' + parts.join(', ') + ')' + (last ? ' = ' + show(dp[i]) + '   ✓' : '') });
      });
    }
    var path = [N];
    for (var p = N; p !== 0; p = p - ch[p]) path.push(p - ch[p]);
    snaps.push({ dp: dp.slice(), x: -1, src: -1, digs: [], di: -1, best: path,
      l1: 'Rješenje: dp[' + N + '] = ' + dp[N] + ' koraka',
      l2: 'Put: ' + path.join(' → ') });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = s.dp[k] === Infinity ? 'cell todo' : 'cell';
        R.vals[k].textContent = show(s.dp[k]);
      });
      chipsBox.textContent = s.x === -1 ? '' : 'Znamenke broja ' + s.x + ':';
      s.digs.forEach(function (d, di) { chipsBox.appendChild(mk('span', di === s.di ? 'chip on' : 'chip', d)); });
      s.best.forEach(function (k) { R.cells[k].classList.add('best'); });
      if (s.src !== -1) R.cells[s.src].classList.add('src');
      if (s.x !== -1) R.cells[s.x].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 400); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

<!-- _class: title -->
# 3. Grid Paths I (CSES)

## 2D dinamičko programiranje

---

# Analiza: Grid Paths I (1/2)

**Problem:**
Mreža $N \times N$. Neka polja su prazna (`.`), neka su zamke (`*`).
Možemo se kretati samo **dolje** i **desno**.
Na koliko načina možemo doći od $(0,0)$ do $(N-1, N-1)$?

**Intuicija:**
Na polje $(i, j)$ možemo doći samo iz dva smjera:

1. **Odozgo:** s polja $(i-1, j)$.
2. **Slijeva:** s polja $(i, j-1)$.

Dakle, broj načina da dođemo do $(i, j)$ jednak je zbroju načina da dođemo do gornjeg i do lijevog polja.

---

# Analiza: Grid Paths I (2/2)

**Definicija DP stanja:**
`dp[i][j]` = broj putova od $(0,0)$ do $(i,j)$.

**Prijelaz:**

- Ako je `grid[i][j] == '*'`: `dp[i][j] = 0` (ne možemo stati na zamku).
- Inače: `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
  *(Pazite na rubove matrice gdje je $i=0$ ili $j=0$.)*

**Baza:**

- Ako je `grid[0][0] == '.'`, onda je `dp[0][0] = 1`.
- Inače je `dp[0][0] = 0`.

---

# Implementacija: Grid Paths I

```cpp
int n; cin >> n;
vector<string> grid(n);
for (int i = 0; i < n; ++i) cin >> grid[i];

vector<vector<int>> dp(n, vector<int>(n, 0));
long long MOD = 1e9 + 7;

// Baza: ako start nije zamka, postoji 1 način da budemo na startu
if (grid[0][0] == '.') dp[0][0] = 1;

for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
        if (grid[i][j] == '*') {
            dp[i][j] = 0; // Zamka - ne možemo doći ovdje
        } else {
            // Zbrajamo putove odozgo i slijeva
            if (i > 0) dp[i][j] = (dp[i][j] + dp[i-1][j]) % MOD;
            if (j > 0) dp[i][j] = (dp[i][j] + dp[i][j-1]) % MOD;
        }
    }
}
cout << dp[n-1][n-1] << "\n";
```

---

# Grid Paths I korak po korak

Polje računamo red po red: `dp[i][j] = dp[i-1][j] + dp[i][j-1]` (odozgo + slijeva), a zamke ✱ imaju 0.

<style scoped>
.dp-grid { margin-top: 0.4em; }
.dp-grid .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-grid .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-grid .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-grid .row { display: flex; gap: 8px; }
.dp-grid .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-grid .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-grid .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-grid .cell.todo .val { color: #b5b5b5; }
.dp-grid .cell.src { background: #f5db7e; }
.dp-grid .cell.best { background: #9fdc9f; }
.dp-grid .cell.cur { background: var(--main); color: #fff; }
.dp-grid .cell.cur .idx, .dp-grid .cell.cur .val { color: #fff; }
.dp-grid .line1, .dp-grid .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-grid .line1 { margin-top: 0.7em; }
.dp-grid .line2 { font-weight: bold; }
.dp-grid .ctrl { margin-top: 0.7em; }
.dp-grid button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-grid button:hover { background: var(--main); color: #fff; }
.dp-grid .hint { font-size: 16px; color: #6e6e6e; }
.dp-grid .tbl { display: grid; gap: 8px; }
.dp-grid .tc { height: 62px; line-height: 58px; text-align: center; font-size: 30px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-grid .tc.trap { background: #141414; color: #fff; }
.dp-grid .tc.src { background: #f5db7e; }
.dp-grid .tc.cur { background: var(--main); color: #fff; }
</style>

<div class="dp-grid" data-grid="....|.*..|...*|*...">
  <div class="tbl"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-grid').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var G = root.dataset.grid.split('|');
    var n = G.length;
    var tbl = root.querySelector('.tbl');
    tbl.style.gridTemplateColumns = 'repeat(' + n + ', 76px)';
    var T = [];
    for (var i = 0; i !== n; i++) {
      var r = [];
      for (var j = 0; j !== n; j++) { var c = mk('div', 'tc'); tbl.appendChild(c); r.push(c); }
      T.push(r);
    }
    var dp = [];
    for (var a1 = 0; a1 !== n; a1++) { var rr = []; for (var b1 = 0; b1 !== n; b1++) rr.push(null); dp.push(rr); }
    dp[0][0] = G[0][0] === '*' ? 0 : 1;
    function copy() { return dp.map(function (r) { return r.slice(); }); }
    var snaps = [{ dp: copy(), i: 0, j: 0, src: [],
      l1: 'Start (0, 0) nije zamka  → dp[0][0] = 1', l2: '' }];
    for (var x = 0; x !== n; x++) {
      for (var y = 0; y !== n; y++) {
        if (x === 0 ? y === 0 : false) continue;
        var l1, src = [];
        if (G[x][y] === '*') {
          dp[x][y] = 0;
          l1 = '(' + x + ', ' + y + ') je zamka  → dp = 0';
        } else {
          var up = x === 0 ? null : dp[x - 1][y];
          var left = y === 0 ? null : dp[x][y - 1];
          if (up !== null) src.push([x - 1, y]);
          if (left !== null) src.push([x, y - 1]);
          dp[x][y] = (up === null ? 0 : up) + (left === null ? 0 : left);
          l1 = '(' + x + ', ' + y + '):  odozgo ' + (up === null ? '—' : up) + ' + slijeva ' + (left === null ? '—' : left) + ' = ' + dp[x][y];
        }
        var fin = x === n - 1 ? y === n - 1 : false;
        snaps.push({ dp: copy(), i: x, j: y, src: src, l1: l1,
          l2: 'dp[' + x + '][' + y + '] = ' + dp[x][y] + (fin ? '   ✓ broj putova do cilja' : '') });
      }
    }
    function draw(s) {
      T.forEach(function (r, i) {
        r.forEach(function (c, j) {
          var trap = G[i][j] === '*';
          c.className = trap ? 'tc trap' : 'tc';
          c.textContent = trap ? '✱' : (s.dp[i][j] === null ? '' : s.dp[i][j]);
        });
      });
      s.src.forEach(function (p) { T[p[0]][p[1]].classList.add('src'); });
      T[s.i][s.j].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 700); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

<!-- _class: title -->
# 4. Book Shop (CSES)

## 0-1 Knapsack Problem

---

# Analiza: Book Shop (1/2)

**Problem:**
Imamo $N$ knjiga. Svaka ima cijenu $price_i$ i broj stranica $pages_i$.
Imamo budžet $X$. Želimo kupiti knjige tako da maksimiziramo ukupan broj stranica, a da ne prijeđemo budžet.

**Tip problema:**
Ovo je školski primjer **0-1 Knapsack problema**.

- "0-1" znači da svaku knjigu možemo uzeti ili ne uzeti (ne možemo uzeti pola, niti više komada iste knjige).

**Pohlepni pristup ne radi:**
Ne možemo samo uzimati knjige s najboljim omjerom stranica/cijena.

---

# Analiza: Book Shop (2/2)

**DP stanje:**
`dp[w]` = maksimalan broj stranica koje možemo dobiti uz potrošnju **najviše** $w$.

**Prijelaz:**
Kada razmatramo novu knjigu s cijenom $P$ i stranicama $S$, za svaki mogući budžet $w$ imamo dvije opcije:

1. **Ne kupimo knjigu:** broj stranica ostaje `dp[w]`.
2. **Kupimo knjigu:** trošimo $P$, pa nam ostaje $w-P$. Broj stranica je `dp[w-P] + S`.

Uzimamo maksimum: `dp[w] = max(dp[w], dp[w-P] + S)`.

**Ključni trik:**
Da bismo koristili 1D niz, moramo iterirati po budžetu **unatrag** (od $X$ do $P$). Ako idemo unaprijed, mogli bismo istu knjigu iskoristiti više puta.

---

# Implementacija: Book Shop

```cpp
int n, x; cin >> n >> x;
vector<int> price(n), pages(n);
for (int &p : price) cin >> p;
for (int &p : pages) cin >> p;

// dp[w] = max stranica uz potrošnju najviše w
vector<int> dp(x + 1, 0);

for (int i = 0; i < n; ++i) {
    // Iteracija unatrag je KLJUČNA za 0-1 Knapsack s 1D nizom!
    // Osigurava da svaku knjigu koristimo najviše jednom.
    for (int w = x; w >= price[i]; --w) {
        dp[w] = max(dp[w], dp[w - price[i]] + pages[i]);
    }
}
cout << dp[x] << "\n";
```

**Složenost:** $O(N \cdot X)$.

---

# Book Shop korak po korak

Za svaku knjigu (cijena `P`, stranica `S`) budžet `w` ide **unatrag** od `X` do `P`: `dp[w] = max(dp[w], dp[w − P] + S)`.

<style scoped>
.dp-book { margin-top: 0.4em; }
.dp-book .chips { font-size: 20px; margin-bottom: 0.5em; }
.dp-book .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.dp-book .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.dp-book .row { display: flex; gap: 8px; }
.dp-book .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.dp-book .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.dp-book .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.dp-book .cell.todo .val { color: #b5b5b5; }
.dp-book .cell.src { background: #f5db7e; }
.dp-book .cell.best { background: #9fdc9f; }
.dp-book .cell.cur { background: var(--main); color: #fff; }
.dp-book .cell.cur .idx, .dp-book .cell.cur .val { color: #fff; }
.dp-book .line1, .dp-book .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.dp-book .line1 { margin-top: 0.7em; }
.dp-book .line2 { font-weight: bold; }
.dp-book .ctrl { margin-top: 0.7em; }
.dp-book button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.dp-book button:hover { background: var(--main); color: #fff; }
.dp-book .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="dp-book" data-x="10" data-price="4,8,5,3" data-pages="5,12,8,1">
  <div class="chips">Knjige:</div>
  <div class="row"></div>
  <div class="line1"></div>
  <div class="line2"></div>
  <div class="ctrl">
    <button data-act="prev">← Korak</button><button data-act="next">Korak →</button><button data-act="auto">Auto</button><button data-act="reset">Reset</button>
    <span class="hint">← / → koračaju kroz animaciju, Shift + ← / → mijenja slajd</span>
  </div>
</div>

<script>
(function () {
  // Ovaj blok namjerno ne sadrži znakove manje-od, veće-od ni ampersand,
  // jer ih build pretvara u HTML entitete i ruši skriptu.
  document.querySelectorAll('.dp-book').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function show(v) { return v === Infinity ? '∞' : String(v); }
    function makeRow(box, count) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }

    var X = parseInt(root.dataset.x, 10);
    var price = root.dataset.price.split(',').map(Number);
    var pages = root.dataset.pages.split(',').map(Number);
    var chipsBox = root.querySelector('.chips');
    var chips = price.map(function (p, b) {
      var s = mk('span', 'chip', '#' + (b + 1) + ': ' + p + ' kn, ' + pages[b] + ' str');
      chipsBox.appendChild(s);
      return s;
    });
    var R = makeRow(root.querySelector('.row'), X + 1);
    var dp = [];
    for (var j = 0; j !== X + 1; j++) dp.push(0);
    var snaps = [{ dp: dp.slice(), b: -1, w: -1, src: -1,
      l1: 'Početno stanje: dp[w] = 0 za svaki budžet w (nismo kupili ništa)', l2: '' }];
    price.forEach(function (P, b) {
      var S = pages[b];
      if (Math.min(P, X) !== P) {
        snaps.push({ dp: dp.slice(), b: b, w: -1, src: -1,
          l1: 'knjiga #' + (b + 1) + ' je skuplja od budžeta, preskačemo', l2: '' });
        return;
      }
      for (var w = X; w !== P - 1; w--) {
        var old = dp[w], cand = dp[w - P] + S;
        var take = cand !== old ? Math.max(cand, old) === cand : false;
        if (take) dp[w] = cand;
        var fin = b === price.length - 1 ? w === P : false;
        snaps.push({ dp: dp.slice(), b: b, w: w, src: w - P,
          l1: '#' + (b + 1) + ', w = ' + w + ':  max(' + old + ', dp[' + (w - P) + '] + ' + S + ' = ' + cand + ')'
            + (take ? '  → kupujemo, dp[' + w + '] = ' + cand : '  → ne isplati se'),
          l2: fin ? 'Rješenje: dp[' + X + '] = ' + dp[X] + ' stranica   ✓'
                  : 'w ide unatrag, pa dp[' + (w - P) + '] još ne sadrži knjigu #' + (b + 1) });
      }
    });
    function draw(s) {
      R.cells.forEach(function (c, k) {
        c.className = 'cell';
        R.vals[k].textContent = s.dp[k];
      });
      chips.forEach(function (ch, b) { ch.className = b === s.b ? 'chip on' : 'chip'; });
      if (s.src !== -1) R.cells[s.src].classList.add('src');
      if (s.w !== -1) R.cells[s.w].classList.add('cur');
    }

    var step = 0, timer = null, lastStep = snaps.length - 1;
    function render() {
      var s = snaps[step];
      draw(s);
      line1.textContent = s.l1;
      line2.textContent = s.l2;
    }
    function stopAuto() { clearInterval(timer); timer = null; }
    function next() { if (step !== lastStep) { step++; render(); return true; } stopAuto(); return false; }
    function prev() { if (step !== 0) { step--; render(); return true; } return false; }
    function reset() { stopAuto(); step = 0; render(); }
    var actions = {
      next: next, prev: prev, reset: reset,
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 600); }
    };

    root.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation(); b.blur(); actions[b.dataset.act]();
      });
    });

    // Strelice / razmaknica / klikač prvo koračaju kroz animaciju, a tek na kraju mijenjaju slajd
    window.addEventListener('keydown', function (e) {
      if (e.shiftKey || !slide || !slide.classList.contains('bespoke-marp-active')) return;
      var fwd = ['ArrowRight', 'ArrowDown', 'PageDown', ' '].indexOf(e.key) !== -1;
      var back = ['ArrowLeft', 'ArrowUp', 'PageUp'].indexOf(e.key) !== -1;
      var moved = false;
      if (fwd) moved = next();
      if (back) moved = prev();
      if (moved) {
        e.preventDefault();
        e.stopImmediatePropagation();
      }
    }, true);

    render();
  });
})();
</script>

---

<!-- _class: lead -->

# Pitanja?
