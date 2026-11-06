---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Složenost i sortiranje"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!-- _paginate: false -->
<!-- _class: title  -->
# Složenost i sortiranje

Programiranje za rješavanje složenih problema

---

# Sadržaj

1. **Vremenska složenost**
   - Big O notacija
   - Procjena vremena izvođenja
2. **Primjer: Najveći zbroj podniza**
   - Od $O(n^3)$ do $O(n)$
3. **Mjerenje vremena**
4. **Sortiranje**
   - `std::sort`
   - Custom comparators
5. **Zadaci za vježbu**

---

<!-- _class: lead -->
# Vremenska složenost

## Kako procijeniti brzinu algoritma?

---

# Big O notacija

Opisuje kako vrijeme izvođenja raste s veličinom ulaza ($n$).

- **$O(1)$**: Konstantno vrijeme (pristup elementu niza).
- **$O(\log n)$**: Logaritamsko (binarno pretraživanje).
- **$O(n)$**: Linearno (prolaz kroz niz).
- **$O(n \log n)$**: Linearno-logaritamsko (efikasno sortiranje).
- **$O(n^2)$**: Kvadratno (ugniježđene petlje).

**Pravilo palca:**
Moderno računalo izvodi $\approx 10^8$ operacija u sekundi.
Ako je limit 1s, a $n=10^5$, algoritam mora biti $O(n)$ ili $O(n \log n)$.

---

<!-- _class: lead -->
# Primjer: Najveći zbroj podniza

## Optimizacija algoritma

---

# Problem: Najveći zbroj podniza

**Zadatak:**
Zadan je niz od $n$ brojeva. Treba pronaći najveći mogući zbroj uzastopnih elemenata.

**Primjer:**
Niz: `2, -3, 1, 5, -2, 3, 5, -2`
Najveći zbroj: **12** (podniz `1, 5, -2, 3, 5`)

U primjerima koda niz je učitan u `vector<long long> a(n)`.

---

# Rješenje 1: $O(n^3)$

Provjeravamo sve moguće podnizove $(i, j)$ i za svaki računamo sumu.

```cpp
long long best = LLONG_MIN;
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        long long sum = 0;
        for (int k = i; k <= j; k++) {
            sum += a[k];
        }
        best = max(best, sum);
    }
}
cout << best << "\n";
```

- Tri ugniježđene petlje.
- Za $n=1000$, $n^3 = 10^9$ (presporo za 1s).

---

# Rješenje 2: $O(n^2)$

Možemo računati sumu u hodu, bez treće petlje.

```cpp
long long best = LLONG_MIN;
for (int i = 0; i < n; i++) {
    long long sum = 0;
    for (int j = i; j < n; j++) {
        sum += a[j];
        best = max(best, sum);
    }
}
cout << best << "\n";
```

- Dvije ugniježđene petlje.
- Za $n=10^4$, $n^2 = 10^8$ (prolazi).
- Za $n=10^5$, $n^2 = 10^{10}$ (presporo).

---

# Rješenje 3: $O(n)$ - Kadaneov algoritam

**Ideja:**
Za svaku poziciju $k$, koji je maksimalni zbroj podniza koji **završava** na toj poziciji?

Ili je to samo element na poziciji $k$, ili produžujemo prethodni podniz.

```cpp
long long best = LLONG_MIN;
long long sum = 0;

for (int k = 0; k < n; k++) {
    // Nastavljamo niz ili krećemo ispočetka od a[k]
    sum = max(a[k], sum + a[k]);
    best = max(best, sum);
}
cout << best << "\n";
```

- Jedna petlja.
- Za $n=10^6$, $10^6$ operacija (trenutno).

---

# Kadaneov algoritam korak po korak

`sum` je najbolji zbroj podniza koji završava na poziciji `k`. Plavo je trenutni podniz, a zeleno na kraju najbolji.

<style scoped>
.cx-kadane { margin-top: 0.3em; }
.cx-kadane .chips { font-size: 20px; margin-bottom: 0.4em; }
.cx-kadane .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.cx-kadane .chip.take { background: #9fdc9f; }
.cx-kadane .chip.skip, .cx-kadane .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.cx-kadane .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.cx-kadane .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.cx-kadane .row { display: flex; gap: 6px; }
.cx-kadane .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-kadane .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.cx-kadane .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.cx-kadane .cell.todo .val { color: #b5b5b5; }
.cx-kadane .cell.rng { background: #d6e6f5; }
.cx-kadane .cell.best { background: #9fdc9f; }
.cx-kadane .cell.src { background: #f5db7e; }
.cx-kadane .cell.cur { background: var(--main); color: #fff; }
.cx-kadane .cell.cur .idx, .cx-kadane .cell.cur .val { color: #fff; }
.cx-kadane .rows .row { margin-bottom: 6px; }
.cx-kadane .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.cx-kadane .prow { margin-top: -4px; }
.cx-kadane .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.cx-kadane .cell.dim { opacity: .3; }
.cx-kadane .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.cx-kadane .wrap { display: flex; gap: 28px; align-items: flex-start; }
.cx-kadane .side { padding-top: 6px; }
.cx-kadane .gsvg { display: block; overflow: visible; }
.cx-kadane .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.cx-kadane .e polygon { fill: #9a9a9a; }
.cx-kadane .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-kadane .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.cx-kadane .e.tree polygon { fill: #2f9e44; }
.cx-kadane .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.cx-kadane .e.off polygon { fill: #d5d5d5; }
.cx-kadane .e.off .w { fill: #b5b5b5; }
.cx-kadane .e.hid { opacity: 0; }
.cx-kadane .e.bad line { stroke: #e03131; stroke-width: 6; }
.cx-kadane .e.bad polygon { fill: #e03131; }
.cx-kadane .e.on line { stroke: var(--main); stroke-width: 6; }
.cx-kadane .e.on polygon { fill: var(--main); }
.cx-kadane .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.cx-kadane .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.cx-kadane .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-kadane .n.c1 circle { fill: #ffd8a8; } .cx-kadane .n.c2 circle { fill: #a5d8ff; } .cx-kadane .n.c3 circle { fill: #b2f2bb; }
.cx-kadane .n.c4 circle { fill: #fcc2d7; } .cx-kadane .n.c5 circle { fill: #d0bfff; } .cx-kadane .n.c6 circle { fill: #ffec99; }
.cx-kadane .n.done circle { fill: #9fdc9f; }
.cx-kadane .n.src circle { fill: #f5db7e; }
.cx-kadane .n.cur circle { fill: var(--main); stroke: var(--main); }
.cx-kadane .n.cur .id { fill: #fff; }
.cx-kadane .tbl { display: grid; gap: 5px; }
.cx-kadane .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.cx-kadane .th.hl { background: var(--main); color: #fff; }
.cx-kadane .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-kadane .tc.none { border-color: transparent; }
.cx-kadane .tc.k { background: #e3ecf6; }
.cx-kadane .tc.best { background: #9fdc9f; }
.cx-kadane .tc.src { background: #f5db7e; }
.cx-kadane .tc.cur { background: var(--main); color: #fff; }
.cx-kadane .line1, .cx-kadane .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.cx-kadane .line1 { margin-top: 0.5em; }
.cx-kadane .line2 { font-weight: bold; }
.cx-kadane .ctrl { margin-top: 0.5em; }
.cx-kadane button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.cx-kadane button:hover { background: var(--main); color: #fff; }
.cx-kadane .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="cx-kadane" data-arr="2,-3,1,5,-2,3,5,-2">
  <div class="rows"></div>
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
  document.querySelectorAll('.cx-kadane').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var a = root.dataset.arr.split(',').map(Number);
    var n = a.length;
    var box = root.querySelector('.rows');
    var A = lrow(box, 'a[k]', n, 0, true);
    var P = prow(box, n);
    var S = lrow(box, 'sum', n, 0, false);
    var B = lrow(box, 'best', n, 0, false);
    var sum = 0, best = -Infinity, start = 0, bs = 0, be = -1;
    var sums = [], bests = [];
    var snaps = [{ k: -1, run: [], win: [], sums: [], bests: [], l1: 'sum = 0 (najbolji zbroj koji završava na prethodnoj poziciji), best = −∞', l2: 'Za svaki k: sum = max(a[k], sum + a[k]), best = max(best, sum)' }];
    for (var k = 0; k !== n; k++) {
      var ext = sum + a[k], extend = le(a[k], ext);
      var l1 = 'k = ' + k + ':  sum = max(a[k], sum + a[k]) = max(' + a[k] + ', ' + sum + ' + ' + fw(a[k]) + ') = ' + Math.max(a[k], ext)
        + (extend ? '  → produžujemo podniz' : '  → krećemo ispočetka od a[' + k + ']');
      if (!extend) start = k;
      sum = Math.max(a[k], ext);
      var better = lt(best, sum);
      if (better) { best = sum; bs = start; be = k; }
      sums.push(sum); bests.push(best);
      var run = [], win = [];
      for (var t = start; t !== k + 1; t++) run.push(t);
      for (var t2 = bs; t2 !== be + 1; t2++) win.push(t2);
      snaps.push({ k: k, start: start, run: run, win: [], sums: sums.slice(), bests: bests.slice(), l1: l1,
        l2: 'best = max(best, ' + sum + ') = ' + best + (better ? '   (novi rekord)' : '') });
    }
    var w = [];
    for (var t3 = bs; t3 !== be + 1; t3++) w.push(t3);
    snaps.push({ k: -1, run: [], win: w, sums: sums.slice(), bests: bests.slice(),
      l1: 'Jedan prolaz kroz niz: O(n)',
      l2: 'Najveći zbroj = ' + best + ', podniz ' + w.map(function (t) { return a[t]; }).join(', ') + '   ✓' });
    function draw(s) {
      for (var i = 0; i !== n; i++) {
        var c = 'cell';
        if (s.run.indexOf(i) !== -1) c += ' rng';
        if (s.win.indexOf(i) !== -1) c += ' best';
        if (i === s.k) c += ' cur';
        setc(A.cells[i], c);
        A.vals[i].textContent = a[i];
        var have = Math.max(i, s.sums.length - 1) === s.sums.length - 1;
        setc(S.cells[i], have ? (i === s.k ? 'cell src' : 'cell') : 'cell todo');
        S.vals[i].textContent = have ? s.sums[i] : '';
        setc(B.cells[i], have ? 'cell' : 'cell todo');
        B.vals[i].textContent = have ? s.bests[i] : '';
      }
      setPtrs(P, s.k === -1 ? [] : [['k', s.k], ['start', s.start === s.k ? -1 : s.start]]);
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 900); }
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

# Mjerenje brzine izvođenja

Kako provjeriti je li naš algoritam stvarno brži?

```cpp
#include <chrono>

auto start = chrono::high_resolution_clock::now();

// ... kod koji mjerimo ...

auto stop = chrono::high_resolution_clock::now();
auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);

cout << "Vrijeme: " << duration.count() << " mikrosekundi" << "\n";
```

---

<!-- _class: lead -->
# Sortiranje

## Uređivanje podataka

---

# Zašto sortirati?

Mnogi problemi postaju jednostavniji ako su podaci sortirani.

- Binarno pretraživanje ($O(\log n)$).
- Pohlepni algoritmi (npr. raspored aktivnosti).
- Pronalaženje duplikata ili jedinstvenih elemenata.

**Složenost sortiranja:**
Merge Sort i Heap Sort jamče $O(n \log n)$, a Quick Sort to postiže u prosjeku (najgori slučaj $O(n^2)$).
U C++ koristimo `std::sort`, koji jamči **$O(n \log n)$**.

---

# Korištenje `std::sort`

```cpp
#include <algorithm>
#include <vector>

vector<int> v = {4, 2, 5, 3, 5, 8, 3};

// Sortiranje u rastućem poretku
sort(v.begin(), v.end());

// Sortiranje u padajućem poretku
sort(v.rbegin(), v.rend());
```

---

# Custom Comparator (Usporedba)

Što ako želimo sortirati strukture ili po posebnom kriteriju?

```cpp
struct Point {
    int x, y;
};

// Sortiraj po x, ako su x isti, onda po y
bool comparePoints(const Point& a, const Point& b) {
    if (a.x != b.x) return a.x < b.x;
    return a.y < b.y;
}

vector<Point> points = { {1, 2}, {3, 1}, {1, 5} };
sort(points.begin(), points.end(), comparePoints);
```

---

# Napomene o komparatoru

**Komparator mora biti strog:** koristite `<`, nikad `<=`.

- S `<=` je ponašanje `std::sort` nedefinirano.
- Na nizovima s jednakim elementima program se može srušiti (**Runtime Error**).

**Parovi se već sortiraju leksikografski:**

```cpp
vector<pair<int, int>> points = { {1, 2}, {3, 1}, {1, 5} };
sort(points.begin(), points.end()); // po x, zatim po y
```

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES Sorting and Searching

---

# Zadaci

1. **[Maximum Subarray Sum](https://cses.fi/problemset/task/1643)**
   - Kadaneov algoritam s današnjih vježbi.
   - *Hint:* Vrijednosti su do $10^9$, koristite `long long`.
2. **[Distinct Numbers](https://cses.fi/problemset/task/1621)**
   - Koliko različitih brojeva ima u nizu?
   - *Hint:* Sortirajte pa prebrojite promjene ili koristite `set`.
3. **[Apartments](https://cses.fi/problemset/task/1084)**
   - Dodjela stanova podstanarima (pohlepno + sortiranje).
4. **[Ferris Wheel](https://cses.fi/problemset/task/1090)**
   - Optimalno sparivanje (dva pokazivača na sortiranom nizu).

---

<!-- _class: title -->
# Distinct Numbers (CSES)

## Analiza i rješenje

---

# Analiza: Distinct Numbers

**Problem:**
Zadan je niz od $n$ cijelih brojeva. Treba izračunati koliko ima **različitih** vrijednosti.

**Ograničenja:** $n \le 2 \cdot 10^5$.

**Pristup 1: `std::set`**

- Ubacimo sve brojeve u `set`, koji automatski miče duplikate. Rješenje je `s.size()`.
- Složenost: $O(n \log n)$ zbog strukture stabla.

**Pristup 2: sortiranje** (brže i manje memorije)

- Nakon sortiranja isti su brojevi jedan do drugog (npr. `1, 1, 2, 2, 2, 5`).
- Prebrojimo koliko se puta broj promijeni u odnosu na prethodni.

---

# Implementacija: Distinct Numbers

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> x(n);
    for (int i = 0; i < n; i++) cin >> x[i];

    sort(x.begin(), x.end()); // O(n log n)

    int distinct_count = 1; // Prvi broj je uvijek jedinstven (n >= 1)
    for (int i = 1; i < n; i++) {
        // Ako je trenutni broj različit od prethodnog, našli smo novi
        if (x[i] != x[i-1]) {
            distinct_count++;
        }
    }
    cout << distinct_count << "\n";
    return 0;
}
```

---

# Distinct Numbers korak po korak

Nakon sortiranja dovoljno je usporediti svaki broj s prethodnim. Zeleni brojevi su prvi primjerci različitih vrijednosti.

<style scoped>
.cx-distinct { margin-top: 0.3em; }
.cx-distinct .chips { font-size: 20px; margin-bottom: 0.4em; }
.cx-distinct .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.cx-distinct .chip.take { background: #9fdc9f; }
.cx-distinct .chip.skip, .cx-distinct .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.cx-distinct .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.cx-distinct .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.cx-distinct .row { display: flex; gap: 6px; }
.cx-distinct .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-distinct .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.cx-distinct .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.cx-distinct .cell.todo .val { color: #b5b5b5; }
.cx-distinct .cell.rng { background: #d6e6f5; }
.cx-distinct .cell.best { background: #9fdc9f; }
.cx-distinct .cell.src { background: #f5db7e; }
.cx-distinct .cell.cur { background: var(--main); color: #fff; }
.cx-distinct .cell.cur .idx, .cx-distinct .cell.cur .val { color: #fff; }
.cx-distinct .rows .row { margin-bottom: 6px; }
.cx-distinct .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.cx-distinct .prow { margin-top: -4px; }
.cx-distinct .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.cx-distinct .cell.dim { opacity: .3; }
.cx-distinct .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.cx-distinct .wrap { display: flex; gap: 28px; align-items: flex-start; }
.cx-distinct .side { padding-top: 6px; }
.cx-distinct .gsvg { display: block; overflow: visible; }
.cx-distinct .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.cx-distinct .e polygon { fill: #9a9a9a; }
.cx-distinct .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-distinct .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.cx-distinct .e.tree polygon { fill: #2f9e44; }
.cx-distinct .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.cx-distinct .e.off polygon { fill: #d5d5d5; }
.cx-distinct .e.off .w { fill: #b5b5b5; }
.cx-distinct .e.hid { opacity: 0; }
.cx-distinct .e.bad line { stroke: #e03131; stroke-width: 6; }
.cx-distinct .e.bad polygon { fill: #e03131; }
.cx-distinct .e.on line { stroke: var(--main); stroke-width: 6; }
.cx-distinct .e.on polygon { fill: var(--main); }
.cx-distinct .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.cx-distinct .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.cx-distinct .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-distinct .n.c1 circle { fill: #ffd8a8; } .cx-distinct .n.c2 circle { fill: #a5d8ff; } .cx-distinct .n.c3 circle { fill: #b2f2bb; }
.cx-distinct .n.c4 circle { fill: #fcc2d7; } .cx-distinct .n.c5 circle { fill: #d0bfff; } .cx-distinct .n.c6 circle { fill: #ffec99; }
.cx-distinct .n.done circle { fill: #9fdc9f; }
.cx-distinct .n.src circle { fill: #f5db7e; }
.cx-distinct .n.cur circle { fill: var(--main); stroke: var(--main); }
.cx-distinct .n.cur .id { fill: #fff; }
.cx-distinct .tbl { display: grid; gap: 5px; }
.cx-distinct .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.cx-distinct .th.hl { background: var(--main); color: #fff; }
.cx-distinct .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-distinct .tc.none { border-color: transparent; }
.cx-distinct .tc.k { background: #e3ecf6; }
.cx-distinct .tc.best { background: #9fdc9f; }
.cx-distinct .tc.src { background: #f5db7e; }
.cx-distinct .tc.cur { background: var(--main); color: #fff; }
.cx-distinct .line1, .cx-distinct .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.cx-distinct .line1 { margin-top: 0.5em; }
.cx-distinct .line2 { font-weight: bold; }
.cx-distinct .ctrl { margin-top: 0.5em; }
.cx-distinct button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.cx-distinct button:hover { background: var(--main); color: #fff; }
.cx-distinct .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="cx-distinct" data-arr="5,2,3,5,2,2,8,3,5,1">
  <div class="rows"></div>
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
  document.querySelectorAll('.cx-distinct').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var x = root.dataset.arr.split(',').map(Number);
    var n = x.length;
    var box = root.querySelector('.rows');
    var A = lrow(box, 'x', n, 0, true);
    var P = prow(box, n);
    var snaps = [{ arr: x.slice(), i: -1, nw: [], cnt: null, l1: 'Ulazni niz (nesortiran)', l2: 'Isti brojevi su razbacani po nizu' }];
    var s = x.slice().sort(function (p, q) { return p - q; });
    var nw = [0], cnt = 1;
    snaps.push({ arr: s, i: -1, nw: [], cnt: null, l1: 'sort(x.begin(), x.end()): isti brojevi su sada jedan do drugog', l2: 'O(n log n)' });
    snaps.push({ arr: s, i: 0, nw: nw.slice(), cnt: cnt, l1: 'Prvi broj je uvijek novi', l2: 'distinct_count = 1' });
    for (var i = 1; i !== n; i++) {
      var diff = s[i] !== s[i - 1];
      if (diff) { cnt++; nw.push(i); }
      snaps.push({ arr: s, i: i, nw: nw.slice(), cnt: cnt,
        l1: 'x[' + i + '] = ' + s[i] + (diff ? ' različit je od ' : ' jednak je ') + 'x[' + (i - 1) + '] = ' + s[i - 1] + (diff ? '  → novi broj' : '  → duplikat'),
        l2: 'distinct_count = ' + cnt + (i === n - 1 ? '   ✓' : '') });
    }
    function draw(st) {
      for (var i = 0; i !== n; i++) {
        var c = 'cell';
        if (st.nw.indexOf(i) !== -1) c += ' best';
        if (i === st.i - 1) c += ' src';
        if (i === st.i) c += ' cur';
        setc(A.cells[i], c);
        A.vals[i].textContent = st.arr[i];
      }
      setPtrs(P, st.i === -1 ? [] : [['i', st.i], ['i − 1', st.i - 1]]);
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
# Apartments (CSES)

## Pohlepni pristup i dva pokazivača

---

# Analiza: Apartments

**Problem:**
Imamo $n$ podstanara i $m$ stanova.

- Podstanar želi stan veličine $a$, ali prihvaća bilo što u rasponu $[a-k, a+k]$.
- Svaki stan ima fiksnu veličinu $b$.
- Cilj: Dodijeliti stanove tako da usrećimo **maksimalan broj** ljudi.

---

# Intuicija: Apartments (Greedy)

Trebamo li malom stanu pridružiti nekoga tko traži mali stan ili veliki?

Logično je da **najmanji stan** pokušamo dati onome tko traži **najmanju kvadraturu**. Ako njemu ne odgovara (jer je stan premalen), nikome drugome neće odgovarati (jer svi ostali traže još veće stanove).

**Strategija:**

1. Sortiramo želje podstanara.
2. Sortiramo veličine stanova.
3. Koristimo dva pokazivača (`i` za ljude, `j` za stanove).

---

# Algoritam s dva pokazivača

Neka su `applicants` i `apartments` sortirani nizovi.

Iteriramo dok imamo ljudi i stanova:

1. Ako je stan `j` **premalen** za osobu `i` (`apartments[j] < applicants[i] - k`):
   - Taj stan ne može uzeti nitko (jer ostali traže još više). Odbacujemo stan (`j++`).
2. Ako je stan `j` **prevelik** za osobu `i` (`apartments[j] > applicants[i] + k`):
   - Ovoj osobi ne možemo naći stan (jer su ostali stanovi još veći). Odbacujemo osobu (`i++`).
3. Inače (stan je taman):
   - **Match!** Dodjeljujemo stan, povećavamo brojač i pomičemo oba pokazivača (`i++`, `j++`).

---

# Implementacija: Apartments

```cpp
sort(applicants.begin(), applicants.end());
sort(apartments.begin(), apartments.end());

int i = 0, j = 0, matches = 0;

while (i < n && j < m) {
    // Stan je premalen za trenutnog podstanara
    if (apartments[j] < applicants[i] - k) {
        j++;
    }
    // Stan je prevelik za trenutnog podstanara
    else if (apartments[j] > applicants[i] + k) {
        i++;
    }
    // Stan odgovara!
    else {
        matches++;
        i++;
        j++;
    }
}
cout << matches << "\n";
```

---

# Apartments korak po korak

Primjer iz CSES-a. Pokazivač `i` ide po željama podstanara, `j` po stanovima; oba niza su sortirana.

<style scoped>
.cx-apart { margin-top: 0.3em; }
.cx-apart .chips { font-size: 20px; margin-bottom: 0.4em; }
.cx-apart .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.cx-apart .chip.take { background: #9fdc9f; }
.cx-apart .chip.skip, .cx-apart .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.cx-apart .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.cx-apart .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.cx-apart .row { display: flex; gap: 6px; }
.cx-apart .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-apart .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.cx-apart .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.cx-apart .cell.todo .val { color: #b5b5b5; }
.cx-apart .cell.rng { background: #d6e6f5; }
.cx-apart .cell.best { background: #9fdc9f; }
.cx-apart .cell.src { background: #f5db7e; }
.cx-apart .cell.cur { background: var(--main); color: #fff; }
.cx-apart .cell.cur .idx, .cx-apart .cell.cur .val { color: #fff; }
.cx-apart .rows .row { margin-bottom: 6px; }
.cx-apart .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.cx-apart .prow { margin-top: -4px; }
.cx-apart .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.cx-apart .cell.dim { opacity: .3; }
.cx-apart .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.cx-apart .wrap { display: flex; gap: 28px; align-items: flex-start; }
.cx-apart .side { padding-top: 6px; }
.cx-apart .gsvg { display: block; overflow: visible; }
.cx-apart .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.cx-apart .e polygon { fill: #9a9a9a; }
.cx-apart .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-apart .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.cx-apart .e.tree polygon { fill: #2f9e44; }
.cx-apart .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.cx-apart .e.off polygon { fill: #d5d5d5; }
.cx-apart .e.off .w { fill: #b5b5b5; }
.cx-apart .e.hid { opacity: 0; }
.cx-apart .e.bad line { stroke: #e03131; stroke-width: 6; }
.cx-apart .e.bad polygon { fill: #e03131; }
.cx-apart .e.on line { stroke: var(--main); stroke-width: 6; }
.cx-apart .e.on polygon { fill: var(--main); }
.cx-apart .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.cx-apart .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.cx-apart .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-apart .n.c1 circle { fill: #ffd8a8; } .cx-apart .n.c2 circle { fill: #a5d8ff; } .cx-apart .n.c3 circle { fill: #b2f2bb; }
.cx-apart .n.c4 circle { fill: #fcc2d7; } .cx-apart .n.c5 circle { fill: #d0bfff; } .cx-apart .n.c6 circle { fill: #ffec99; }
.cx-apart .n.done circle { fill: #9fdc9f; }
.cx-apart .n.src circle { fill: #f5db7e; }
.cx-apart .n.cur circle { fill: var(--main); stroke: var(--main); }
.cx-apart .n.cur .id { fill: #fff; }
.cx-apart .tbl { display: grid; gap: 5px; }
.cx-apart .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.cx-apart .th.hl { background: var(--main); color: #fff; }
.cx-apart .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-apart .tc.none { border-color: transparent; }
.cx-apart .tc.k { background: #e3ecf6; }
.cx-apart .tc.best { background: #9fdc9f; }
.cx-apart .tc.src { background: #f5db7e; }
.cx-apart .tc.cur { background: var(--main); color: #fff; }
.cx-apart .line1, .cx-apart .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.cx-apart .line1 { margin-top: 0.5em; }
.cx-apart .line2 { font-weight: bold; }
.cx-apart .ctrl { margin-top: 0.5em; }
.cx-apart button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.cx-apart button:hover { background: var(--main); color: #fff; }
.cx-apart .hint { font-size: 16px; color: #6e6e6e; }
.cx-apart .rl { width: 130px; }
</style>

<div class="cx-apart" data-a="60,45,80,60" data-b="30,60,75" data-k="5">
  <div class="rows"></div>
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
  document.querySelectorAll('.cx-apart').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var ap = root.dataset.a.split(',').map(Number).sort(function (p, q) { return p - q; });
    var st = root.dataset.b.split(',').map(Number).sort(function (p, q) { return p - q; });
    var K = Number(root.dataset.k), n = ap.length, m = st.length;
    var box = root.querySelector('.rows');
    var A = lrow(box, 'podstanari', n, 0, true);
    var PA = prow(box, n);
    var B = lrow(box, 'stanovi', m, 0, true);
    var PB = prow(box, m);
    var i = 0, j = 0, matches = 0, mA = [], mB = [], dA = [], dB = [];
    function snap(o) {
      var s = { i: i, j: j, mA: mA.slice(), mB: mB.slice(), dA: dA.slice(), dB: dB.slice(), l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      return s;
    }
    var snaps = [snap({ l1: 'Oba niza su sortirana, k = ' + K + '. Podstanar s željom a prihvaća stan iz [a − k, a + k].', l2: 'matches = 0' })];
    while (lt(i, n) ? lt(j, m) : false) {
      var lo = ap[i] - K, hi = ap[i] + K, l1;
      if (lt(st[j], lo)) { l1 = 'Stan ' + st[j] + ' je premalen za [' + lo + ', ' + hi + ']  → nitko ga neće uzeti, j++'; dB.push(j); j++; }
      else if (lt(hi, st[j])) { l1 = 'Stan ' + st[j] + ' je prevelik za [' + lo + ', ' + hi + ']  → ovaj podstanar ostaje bez stana, i++'; dA.push(i); i++; }
      else { matches++; l1 = 'Stan ' + st[j] + ' je u [' + lo + ', ' + hi + ']  → match! i++, j++'; mA.push(i); mB.push(j); i++; j++; }
      snaps.push(snap({ l1: l1, l2: 'matches = ' + matches }));
    }
    snaps.push(snap({ l1: 'Jedan od pokazivača je stigao do kraja.', l2: 'Odgovor: ' + matches + '   ✓' }));
    function paint(R, vals, arr, ptr, mt, dd) {
      R.cells.forEach(function (c, k) {
        var cl = 'cell';
        if (mt.indexOf(k) !== -1) cl += ' best';
        if (dd.indexOf(k) !== -1) cl += ' dim';
        if (k === ptr) cl += ' cur';
        setc(c, cl);
        R.vals[k].textContent = arr[k];
      });
    }
    function draw(s) {
      paint(A, null, ap, s.i, s.mA, s.dA);
      paint(B, null, st, s.j, s.mB, s.dB);
      setPtrs(PA, [['i', lt(s.i, n) ? s.i : -1]]);
      setPtrs(PB, [['j', lt(s.j, m) ? s.j : -1]]);
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 1000); }
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
# Ferris Wheel (CSES)

## Optimizacija parova

---

# Analiza: Ferris Wheel

**Problem:**
Imamo $n$ djece s težinama $p_i$. Gondola nosi **maksimalno dvoje** djece i ima limit težine $X$.
Cilj: Minimizirati broj gondola.

**Intuicija:**
Najkritičnije je **najteže dijete**. Ono sigurno mora ići u neku gondolu.
Pitanje je: *Može li itko ići s njim?*

Ako najteže dijete može ići s ikim, najbolje je da ide s **najlakšim** djetetom.

- Ako najteži + najlakši $\le X$, super! Riješili smo dvoje djece jednom gondolom.
- Ako najteži + najlakši $> X$, onda najteži ne može ići ni s kim (jer je najlakši bio najbolja šansa). Najteži ide sam.

---

# Algoritam (Two Pointers)

1. Sortiramo djecu po težini.
2. Postavimo pokazivač `i` na početak (najlakši) i `j` na kraj (najteži).
3. Dok se pokazivači ne susretnu (`i <= j`):
   - Uvijek uzimamo najtežeg (`j`).
   - Provjerimo stane li i najlakši (`i`) s njim: `p[i] + p[j] <= X`.
     - Ako stane, uzimamo i njega (`i++`).
   - U svakom slučaju najteži odlazi (`j--`) i koristimo jednu gondolu (`gondolas++`).

---

# Implementacija: Ferris Wheel

```cpp
sort(p.begin(), p.end());

int i = 0;          // Pokazivač na najlakše dijete
int j = n - 1;      // Pokazivač na najteže dijete
int gondolas = 0;

while (i <= j) {
    // Ako su najlakši i najteži zajedno unutar limita
    if (p[i] + p[j] <= x) {
        i++; // Uzimamo i najlakšeg
        j--; // Uzimamo i najtežeg
    } else {
        // Najteži mora ići sam
        j--;
    }
    gondolas++; // U svakom koraku jedna gondola odlazi
}
cout << gondolas << "\n";
```

**Zaključak:** Sortiranje nam je omogućilo da pohlepno donosimo optimalne odluke s krajeva niza. Složenost: $O(n \log n)$.

---

# Ferris Wheel korak po korak

Najteže dijete uvijek ulazi u gondolu; najlakše ide s njim samo ako zajedno ne prelaze limit.

<style scoped>
.cx-ferris { margin-top: 0.3em; }
.cx-ferris .chips { font-size: 20px; margin-bottom: 0.4em; }
.cx-ferris .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin: 0 0 6px 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; }
.cx-ferris .chip.take { background: #9fdc9f; }
.cx-ferris .chip.skip, .cx-ferris .chip.stale { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.cx-ferris .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.cx-ferris .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.cx-ferris .row { display: flex; gap: 6px; }
.cx-ferris .cell { width: 62px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-ferris .idx { font-size: 15px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.cx-ferris .val { font-size: 24px; height: 38px; line-height: 38px; font-weight: bold; }
.cx-ferris .cell.todo .val { color: #b5b5b5; }
.cx-ferris .cell.rng { background: #d6e6f5; }
.cx-ferris .cell.best { background: #9fdc9f; }
.cx-ferris .cell.src { background: #f5db7e; }
.cx-ferris .cell.cur { background: var(--main); color: #fff; }
.cx-ferris .cell.cur .idx, .cx-ferris .cell.cur .val { color: #fff; }
.cx-ferris .rows .row { margin-bottom: 6px; }
.cx-ferris .rl { width: 110px; flex: none; font-size: 18px; font-weight: bold; color: #6e6e6e; text-align: right; padding-right: 8px; align-self: center; }
.cx-ferris .prow { margin-top: -4px; }
.cx-ferris .pc { width: 66px; flex: none; text-align: center; font-weight: bold; color: var(--main); font-size: 17px; min-height: 24px; }
.cx-ferris .cell.dim { opacity: .3; }
.cx-ferris .lbl { font-size: 18px; font-weight: bold; color: #6e6e6e; margin: 0.4em 0 0.2em; }
.cx-ferris .wrap { display: flex; gap: 28px; align-items: flex-start; }
.cx-ferris .side { padding-top: 6px; }
.cx-ferris .gsvg { display: block; overflow: visible; }
.cx-ferris .e line { stroke: #9a9a9a; stroke-width: 3; transition: stroke .25s; }
.cx-ferris .e polygon { fill: #9a9a9a; }
.cx-ferris .e .w { font-size: 19px; font-weight: bold; fill: #141414; text-anchor: middle; dominant-baseline: central; paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-ferris .e.tree line { stroke: #2f9e44; stroke-width: 6; }
.cx-ferris .e.tree polygon { fill: #2f9e44; }
.cx-ferris .e.off line { stroke: #d5d5d5; stroke-dasharray: 6 6; }
.cx-ferris .e.off polygon { fill: #d5d5d5; }
.cx-ferris .e.off .w { fill: #b5b5b5; }
.cx-ferris .e.hid { opacity: 0; }
.cx-ferris .e.bad line { stroke: #e03131; stroke-width: 6; }
.cx-ferris .e.bad polygon { fill: #e03131; }
.cx-ferris .e.on line { stroke: var(--main); stroke-width: 6; }
.cx-ferris .e.on polygon { fill: var(--main); }
.cx-ferris .n circle { fill: #fff; stroke: #141414; stroke-width: 2.5; transition: fill .25s; }
.cx-ferris .n .id { font-size: 21px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: #141414; }
.cx-ferris .n .sub { font-size: 19px; font-weight: bold; text-anchor: middle; dominant-baseline: central; fill: var(--main); paint-order: stroke; stroke: #fff; stroke-width: 6px; }
.cx-ferris .n.c1 circle { fill: #ffd8a8; } .cx-ferris .n.c2 circle { fill: #a5d8ff; } .cx-ferris .n.c3 circle { fill: #b2f2bb; }
.cx-ferris .n.c4 circle { fill: #fcc2d7; } .cx-ferris .n.c5 circle { fill: #d0bfff; } .cx-ferris .n.c6 circle { fill: #ffec99; }
.cx-ferris .n.done circle { fill: #9fdc9f; }
.cx-ferris .n.src circle { fill: #f5db7e; }
.cx-ferris .n.cur circle { fill: var(--main); stroke: var(--main); }
.cx-ferris .n.cur .id { fill: #fff; }
.cx-ferris .tbl { display: grid; gap: 5px; }
.cx-ferris .th { height: 40px; line-height: 40px; text-align: center; font-size: 20px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.cx-ferris .th.hl { background: var(--main); color: #fff; }
.cx-ferris .tc { height: 40px; line-height: 36px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.cx-ferris .tc.none { border-color: transparent; }
.cx-ferris .tc.k { background: #e3ecf6; }
.cx-ferris .tc.best { background: #9fdc9f; }
.cx-ferris .tc.src { background: #f5db7e; }
.cx-ferris .tc.cur { background: var(--main); color: #fff; }
.cx-ferris .line1, .cx-ferris .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.cx-ferris .line1 { margin-top: 0.5em; }
.cx-ferris .line2 { font-weight: bold; }
.cx-ferris .ctrl { margin-top: 0.5em; }
.cx-ferris button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.cx-ferris button:hover { background: var(--main); color: #fff; }
.cx-ferris .hint { font-size: 16px; color: #6e6e6e; }
.cx-ferris .gond { margin-top: 0.6em; }
</style>

<div class="cx-ferris" data-p="2,9,4,7,8,3,5,6" data-x="10">
  <div class="rows"></div>
  <div class="gond chips"></div>
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
  document.querySelectorAll('.cx-ferris').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    var NS = 'http://www.w3.org/2000/svg';
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function sv(tag, attrs, parent) {
      var e = document.createElementNS(NS, tag);
      Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
      if (parent) parent.appendChild(e);
      return e;
    }
    function setc(el, cls) { el.setAttribute('class', cls); }
    function show(v) { return v === Infinity ? '∞' : (v === -Infinity ? '−∞' : String(v)); }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
    function le(a, b) { return Math.min(a, b) === a; }
    function fw(w) { return lt(w, 0) ? '(' + w + ')' : String(w); }
    function makeRow(box, count, base) {
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        box.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals };
    }
    // Redak s oznakom: [oznaka] [ćelija] [ćelija] ...
    function lrow(box, label, count, base, idx) {
      var r = mk('div', 'row');
      r.appendChild(mk('div', 'rl', label));
      box.appendChild(r);
      var cells = [], vals = [];
      for (var k = 0; k !== count; k++) {
        var cell = mk('div', 'cell');
        if (idx) cell.appendChild(mk('div', 'idx', k + (base || 0)));
        var v = mk('div', 'val');
        cell.appendChild(v);
        r.appendChild(cell);
        cells.push(cell);
        vals.push(v);
      }
      return { cells: cells, vals: vals, row: r };
    }
    // Redak pokazivača ispod niza (l, mid, r, i, j ...)
    function prow(box, count) {
      var r = mk('div', 'row prow');
      r.appendChild(mk('div', 'rl', ''));
      box.appendChild(r);
      var cells = [];
      for (var k = 0; k !== count; k++) cells.push(r.appendChild(mk('div', 'pc')));
      return cells;
    }
    function setPtrs(cells, pairs) {
      var m = {};
      pairs.forEach(function (p) { if (p[1] !== -1) m[p[1]] = m[p[1]] ? m[p[1]] + ', ' + p[0] : p[0]; });
      cells.forEach(function (c, k) { c.textContent = m[k] || ''; });
    }
    function parsePos(s) {
      return s.trim().split(/\s+/).map(function (p) {
        var q = p.split(',').map(Number);
        return { x: q[0], y: q[1] };
      });
    }
    function parseEdges(s) {
      return s.split(',').map(function (t) {
        var q = t.trim().split(':'), ab = q[0].split('-');
        return { a: Number(ab[0]), b: Number(ab[1]), w: q.length === 2 ? Number(q[1]) : 0 };
      });
    }
    // Crta graf u SVG-u: čvorovi su numerirani od 1, bridovi su {a, b, w}
    function drawGraph(box, pos, edges, opt) {
      var R = opt.r || 22;
      var svg = sv('svg', { viewBox: '0 0 ' + opt.w + ' ' + opt.h, width: opt.w, height: opt.h, 'class': 'gsvg' }, box);
      var gE = sv('g', {}, svg), gN = sv('g', {}, svg);
      var E = edges.map(function (e) {
        var A = pos[e.a - 1], B = pos[e.b - 1];
        var dx = B.x - A.x, dy = B.y - A.y, L = Math.sqrt(dx * dx + dy * dy);
        var ux = dx / L, uy = dy / L;
        var x1 = A.x + ux * R, y1 = A.y + uy * R, x2 = B.x - ux * R, y2 = B.y - uy * R;
        var g = sv('g', { 'class': 'e' }, gE);
        sv('line', { x1: x1, y1: y1, x2: x2, y2: y2 }, g);
        if (opt.directed) {
          var bx = x2 - ux * 15, by = y2 - uy * 15;
          sv('polygon', { points: x2 + ',' + y2 + ' ' + (bx - uy * 7) + ',' + (by + ux * 7) + ' ' + (bx + uy * 7) + ',' + (by - ux * 7) }, g);
        }
        if (opt.weights) {
          var t = sv('text', { x: (A.x + B.x) / 2 - uy * 15, y: (A.y + B.y) / 2 + ux * 15, 'class': 'w' }, g);
          t.textContent = e.w;
        }
        return { g: g };
      });
      var N = pos.map(function (p, i) {
        var g = sv('g', { 'class': 'n' }, gN);
        sv('circle', { cx: p.x, cy: p.y, r: R }, g);
        var t = sv('text', { x: p.x, y: p.y, 'class': 'id' }, g);
        t.textContent = i + 1;
        var sub = sv('text', { x: p.x + (opt.subdx || 0), y: p.y + (opt.subdy === undefined ? -R - 13 : opt.subdy), 'class': 'sub' }, g);
        return { g: g, sub: sub };
      });
      return { E: E, N: N, svg: svg };
    }

    var p = root.dataset.p.split(',').map(Number);
    var X = Number(root.dataset.x), n = p.length;
    var box = root.querySelector('.rows');
    var A = lrow(box, 'težine', n, 0, true);
    var P = prow(box, n);
    var gBox = root.querySelector('.gond');
    var snaps = [{ arr: p.slice(), i: -1, j: -1, gone: [], g: [], l1: 'Ulaz (nesortiran), limit gondole X = ' + X, l2: 'Gondola nosi najviše dvoje djece' }];
    p = p.slice().sort(function (a, b) { return a - b; });
    var i = 0, j = n - 1, gone = [], g = [];
    snaps.push({ arr: p, i: i, j: j, gone: [], g: [], l1: 'Sortiramo: i pokazuje na najlakše, j na najteže dijete', l2: 'gondolas = 0' });
    while (le(i, j)) {
      var l1;
      if (i === j) { l1 = 'Ostalo je samo jedno dijete (' + p[j] + '), ide samo'; g.push([p[j]]); gone.push(j); j--; }
      else if (le(p[i] + p[j], X)) { l1 = 'p[i] + p[j] = ' + p[i] + ' + ' + p[j] + ' = ' + (p[i] + p[j]) + ' ≤ ' + X + '  → idu zajedno, i++, j--'; g.push([p[i], p[j]]); gone.push(i, j); i++; j--; }
      else { l1 = 'p[i] + p[j] = ' + p[i] + ' + ' + p[j] + ' = ' + (p[i] + p[j]) + ' veće je od ' + X + '  → najteži (' + p[j] + ') ide sam, j--'; g.push([p[j]]); gone.push(j); j--; }
      snaps.push({ arr: p, i: i, j: j, gone: gone.slice(), g: g.slice(), last: g.length - 1, l1: l1, l2: 'gondolas = ' + g.length });
    }
    snaps[snaps.length - 1].l2 += '   ✓';
    function draw(s) {
      var act = le(s.i, s.j) ? s.i !== -1 : false;
      A.cells.forEach(function (c, k) {
        var cl = 'cell';
        if (s.gone.indexOf(k) !== -1) cl += ' dim';
        if (act ? (k === s.i ? true : k === s.j) : false) cl += ' cur';
        setc(c, cl);
        A.vals[k].textContent = s.arr[k];
      });
      setPtrs(P, act ? [['i', s.i], ['j', s.j]] : []);
      gBox.textContent = 'Gondole:';
      if (s.g.length === 0) gBox.appendChild(mk('span', 'muted', 'još nijedna'));
      s.g.forEach(function (q, k) { gBox.appendChild(mk('span', k === s.last ? 'chip on' : 'chip take', q.join(' + '))); });
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
      auto: function () { if (timer) stopAuto(); else timer = setInterval(next, 1000); }
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
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **Analiza složenosti je ključna:**
   - Prije pisanja koda procijenite hoće li algoritam proći vremensko ograničenje.
   - $10^8$ operacija $\approx 1$ sekunda.

2. **Sortiranje je moćan alat:**
   - Mnogi problemi postaju trivijalni na sortiranom nizu (npr. *Distinct Numbers*).
   - Omogućuje korištenje **pohlepnih algoritama** i **tehnike dva pokazivača** (*Apartments*, *Ferris Wheel*).

3. **Efikasnost C++-a:**
   - `std::sort` je brz ($O(n \log n)$).
   - Koristite `vector` i reference (`&`) za prosljeđivanje velikih struktura.

---

# Zlatna pravila za rješavanje zadataka

- **Provjerite ograničenja ($n$):**
  - Ako je $n=10^5$, rješenje mora biti $O(n)$ ili $O(n \log n)$. $O(n^2)$ neće proći.
- **Pazite na overflow:**
  - Ako zbrajate puno brojeva ili množite, koristite `long long`.
- **Rubni slučajevi:**
  - Što ako je niz prazan? Što ako su svi brojevi isti? Što ako je $n=1$?
- **Ne komplicirajte:**
  - Ako postoji jednostavno rješenje (npr. sortiranje), vjerojatno je bolje od komplicirane strukture podataka.
  