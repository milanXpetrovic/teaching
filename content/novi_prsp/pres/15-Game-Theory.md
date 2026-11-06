---
marp: true
theme: uniri-beam
size: 16:9
paginate: true
math: mathjax
header: "Teorija igara"
footer: "Programiranje za rješavanje složenih problema | Vježbe"
---

<!--
Konvencije za ovaj kolegij:
- Bilješke (npr. prijedlozi za slike) idu u HTML komentar, ne na slajd.
- Bez "---" na kraju datoteke (stvara prazan slajd).
- Obraćanje studentima na "vi"; opisi algoritama u 1. licu množine.
- U kodu "\n" umjesto endl.
- Ne koristiti globalna imena koja se sudaraju sa std:: (count, end, array,
  distance, size, log): ans, er/ec, a, dist, sz, logs.
- Unutar slajda podnaslovi kao **bold**, ne ##/###.
- Prazan redak prije teksta koji slijedi nakon liste.
-->

<!--
Prijedlozi za slike (dodati ručno):

1. Igra Nim (slajd "Igra Nim: pravila"):
   pretraga "Nim game heaps matchsticks illustration".
2. Graf stanja igre s djeliteljima (slajd "Primjer: igra s djeliteljima"):
   CPH, poglavlje 25.1, slika grafa stanja 1-9.
3. Staircase Nim (slajd "Analiza: Stair Game (1/2)"):
   pretraga "staircase nim diagram".
4. Grundy's game (slajd "Analiza: Grundy's Game (1/2)"):
   https://en.wikipedia.org/wiki/Grundy%27s_game
-->

<!-- _paginate: false -->
<!-- _class: title -->
# Teorija igara

## Pobjednička stanja, Nim i Sprague-Grundy teorem

---

# Sadržaj

1. **Uvod u kombinatorne igre**
   - Nepristrane igre i normalna igra
2. **Pobjednička i gubitnička stanja**
   - W/L analiza, igra kao graf stanja
3. **Igra Nim**
   - Nim suma (XOR) i pobjednička strategija
4. **Sprague-Grundy teorem**
   - Funkcija mex, Grundyjevi brojevi, zbroj igara
5. **Zadaci za vježbu**
   - CSES: Stick Game, Nim Game I i II, Stair Game, Grundy's Game, Another Game

---

<!-- _class: lead -->
# Uvod u kombinatorne igre

## Tko pobjeđuje ako oba igrača igraju optimalno?

---

# Što je kombinatorna igra?

U natjecateljskom programiranju najčešće analiziramo **nepristrane kombinatorne igre** (impartial combinatorial games).

**Svojstva:**

- Igraju **dva igrača** koji naizmjence povlače poteze.
- Oba igrača vide **cijelo stanje** igre: nema skrivenih informacija ni slučajnosti (kockica, karata).
- Dozvoljeni potezi ovise **samo o stanju**, a ne o tome koji je igrač na potezu.
- Igra uvijek završava nakon **konačno mnogo** poteza.
- **Normalna igra (normal play):** igrač koji ne može povući potez **gubi**.

Šah nije nepristrana igra: bijeli smije micati samo bijele figure, a crni samo crne.

---

# Kakva pitanja postavljaju zadaci?

Tipičan zadatak glasi: *"Tko pobjeđuje ako oba igrača igraju optimalno?"*

- Igrači su "savršeni": svaki uvijek bira najbolji mogući potez.
- Ne simuliramo partiju, nego **klasificiramo stanja**.
- Ponekad treba ispisati i **pobjednički potez**.

**Ključna ideja:**
Ishod ovisi samo o **trenutnom stanju** igre. Zato svako stanje možemo unaprijed označiti kao pobjedničko ili gubitničko za igrača koji je **na potezu**.

---

# Preporučena literatura

- **CPH (Competitive Programmer's Handbook):**
  - Poglavlje 25: *Game theory* (stanja igre, Nim, Sprague-Grundy teorem)
- **CP-Algorithms:**
  - *Games on arbitrary graphs*, *Sprague-Grundy theorem. Nim*
- **Thomas S. Ferguson: Game Theory:**
  - Part I: *Impartial Combinatorial Games* (besplatno dostupno online)
- **Berlekamp, Conway, Guy: Winning Ways for your Mathematical Plays:**
  - "Biblija" kombinatorne teorije igara

---

<!-- _class: lead -->
# Pobjednička i gubitnička stanja

## W/L analiza

---

# Pobjednička (W) i gubitnička (L) stanja

Stanje uvijek promatramo iz perspektive igrača koji je **na potezu**.

- **L (losing):** **svi** potezi vode u W stanja (ili potez uopće ne postoji).
- **W (winning):** postoji **barem jedan** potez koji vodi u L stanje.

**Rekurzivno pravilo:**

1. Stanje bez poteza je **L** (igrač na potezu je izgubio).
2. Ako iz stanja možemo doći u neko **L** stanje, stanje je **W**.
3. Ako svi potezi vode u **W** stanja, stanje je **L**.

Igrač u W stanju uvijek igra potez u L stanje, pa protivnik nikad ne izlazi iz gubitničkih stanja.

---

# Primjer: igra oduzimanja

Na stolu je hrpa od $n$ žetona. Igrač na potezu uzima **1, 2 ili 3** žetona. Tko uzme zadnji žeton, pobjeđuje.

| $n$ | potezi vode u | stanje |
| :-: | :-- | :-: |
| 0 | nema poteza | **L** |
| 1 | 0 (L) | **W** |
| 2 | 1 (W), 0 (L) | **W** |
| 3 | 2 (W), 1 (W), 0 (L) | **W** |
| 4 | 3 (W), 2 (W), 1 (W) | **L** |
| 5 | 4 (L), 3 (W), 2 (W) | **W** |

**Uzorak:** $n$ je L stanje točno kada je $n$ djeljiv s 4.
Općenito, za poteze $\{1, 2, \dots, k\}$ vrijedi: $n$ je L $\iff n \equiv 0 \pmod{k+1}$.

---

# Kod: W/L stanja (DP)

Stanja računamo **od manjih prema većima**, jer potez uvijek smanjuje broj žetona.

```cpp
vector<int> moves = {1, 2, 3};
vector<bool> win(n + 1, false); // win[0] = false: nema poteza, L stanje

for (int x = 1; x <= n; x++) {
    for (int m : moves) {
        // Ako potez m vodi u L stanje, x je W stanje
        if (m <= x && !win[x - m]) {
            win[x] = true;
            break;
        }
    }
}
```

**Složenost:** $O(n \cdot k)$, gdje je $k$ broj različitih poteza.

---

# Igra oduzimanja korak po korak

Zelena polja su W, crvena L. Žuti obrub: stanja dostižna jednim potezom. Crveni obrub: L stanje u koje igramo.

<style scoped>
.gt-wl { margin-top: 0.4em; }
.gt-wl .chips { font-size: 20px; margin-bottom: 0.6em; }
.gt-wl .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gt-wl .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gt-wl .chip.skip { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gt-wl .row { display: flex; gap: 8px; }
.gt-wl .cell { width: 72px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s, box-shadow .25s; }
.gt-wl .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gt-wl .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gt-wl .cell.todo .val { color: #b5b5b5; }
.gt-wl .cell.w { background: #b2f2bb; }
.gt-wl .cell.l { background: #ffc9c9; }
.gt-wl .cell.src { box-shadow: 0 0 0 4px #f5b400; }
.gt-wl .cell.tgt { box-shadow: 0 0 0 4px #e03131; }
.gt-wl .cell.cur { background: var(--main); color: #fff; }
.gt-wl .cell.cur .idx, .gt-wl .cell.cur .val { color: #fff; }
.gt-wl .line1, .gt-wl .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gt-wl .line1 { margin-top: 0.8em; }
.gt-wl .line2 { font-weight: bold; }
.gt-wl .ctrl { margin-top: 0.7em; }
.gt-wl button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gt-wl button:hover { background: var(--main); color: #fff; }
.gt-wl .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="gt-wl" data-n="12" data-moves="1,2,3" data-note="Uzorak: n je L točno kada je n djeljiv s 4   ✓">
  <div class="chips">Dozvoljeni potezi:</div>
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
  document.querySelectorAll('.gt-wl').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function le(a, b) { return Math.min(a, b) === a; }
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

    var N = parseInt(root.dataset.n, 10);
    var moves = root.dataset.moves.split(',').map(Number);
    var chipsBox = root.querySelector('.chips');
    var chips = moves.map(function (m) { var s = mk('span', 'chip', m); chipsBox.appendChild(s); return s; });
    var R = makeRow(root.querySelector('.row'), N + 1, 0);

    // Unaprijed izračunamo sve korake (jedan korak = jedno stanje n)
    var win = [false];
    var snaps = [{ upto: 0, cur: 0, src: [], tgt: -1, tm: -1, fin: false,
      l1: 'n = 0: nema žetona, igrač na potezu ne može povući potez',
      l2: 'Stanje 0 je L (gubitničko)' }];
    for (var x = 1; x !== N + 1; x++) {
      var src = [], parts = [], tgt = -1, tm = -1;
      moves.forEach(function (m, mi) {
        if (le(m, x)) {
          src.push(x - m);
          parts.push((x - m) + ' (' + (win[x - m] ? 'W' : 'L') + ')');
          if (tgt === -1) {
            if (!win[x - m]) { tgt = x - m; tm = mi; }
          }
        }
      });
      win.push(tgt !== -1);
      snaps.push({ upto: x, cur: x, src: src, tgt: tgt, tm: tm, fin: false,
        l1: 'n = ' + x + ': potezi vode u ' + parts.join(', '),
        l2: tgt !== -1
          ? x + ' je W: uzmemo ' + moves[tm] + ' i protivnika ostavimo u L stanju ' + tgt + '   ✓'
          : x + ' je L: svi potezi vode u W stanja' });
    }
    var lose = [];
    for (var k = 0; k !== N + 1; k++) { if (!win[k]) lose.push(k); }
    snaps.push({ upto: N, cur: -1, src: [], tgt: -1, tm: -1, fin: true,
      l1: 'L stanja: ' + lose.join(', '), l2: root.dataset.note });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        var cls = 'cell';
        if (le(k, s.upto)) cls += win[k] ? ' w' : ' l';
        else cls += ' todo';
        if (s.src.indexOf(k) !== -1) cls += ' src';
        if (k === s.tgt) cls += ' tgt';
        if (s.fin) { if (!win[k]) cls += ' tgt'; }
        if (k === s.cur) cls += ' cur';
        c.className = cls;
        R.vals[k].textContent = le(k, s.upto) ? (win[k] ? 'W' : 'L') : '';
      });
      chips.forEach(function (ch, mi) {
        var cls = 'chip';
        if (s.cur !== -1) { if (!le(moves[mi], s.cur)) cls += ' skip'; }
        if (mi === s.tm) cls += ' on';
        ch.className = cls;
      });
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

# Igra kao graf stanja

Igru prikazujemo kao **usmjereni graf**: čvorovi su **stanja**, a bridovi **potezi**. Graf je **aciklički (DAG)** jer igra uvijek završava. Završna stanja su **L**, a ostala računamo DFS-om s memoizacijom (ili DP-om u topološkom poretku):

```cpp
int memo[MAXN]; // -1 = još nije izračunato, 0 = L, 1 = W

int solve(int x) {
    if (memo[x] != -1) return memo[x];
    int res = 0;                        // Pretpostavimo L
    for (int y : next_states(x))        // Stanja dostižna jednim potezom
        if (solve(y) == 0) res = 1;     // Postoji potez u L: x je W
    return memo[x] = res;
}
```

*(Ako graf ima cikluse, igra može trajati beskonačno. Vidi "Games on arbitrary graphs" na CP-Algorithms.)*

---

# Primjer: igra s djeliteljima

Stanje je prirodni broj $n$. Igrač na potezu bira djelitelj $x$ broja $n$ uz $x < n$, a novo stanje je $n - x$. Tko ne može povući potez (stanje $n = 1$), gubi.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| potez vodi u | – | 1 | 2 | 3, 2 | 4 | 5, 4, 3 | 6 | 7, 6, 4 | 8, 6 |
| stanje | **L** | **W** | **L** | **W** | **L** | **W** | **L** | **W** | **L** |

**Uzorak:** parni $n$ su W, neparni L.

- Neparan $n$ ima samo neparne djelitelje, pa potez uvijek vodi u **paran** broj.
- Iz parnog $n$ uzmemo $x = 1$ i protivniku ostavimo **neparan** broj.

---

<!-- _class: lead -->
# Igra Nim

## Temelj teorije nepristranih igara

---

# Igra Nim: pravila

- Imamo $k$ hrpa žetona veličina $x_1, x_2, \dots, x_k$.
- Igrač na potezu bira **jednu** hrpu i s nje uzima **proizvoljan broj** žetona (barem jedan, može i cijelu hrpu).
- Tko uzme zadnji žeton, pobjeđuje.

**Zašto je Nim važan?**

- Ima elegantno rješenje u $O(k)$.
- Po Sprague-Grundy teoremu **svaka** nepristrana igra ekvivalentna je nekoj Nim hrpi.

**Mali slučajevi:**

- Jedna hrpa: W ako je $x_1 > 0$ (uzmemo sve).
- Dvije jednake hrpe: L. Protivnika "zrcalimo": isti potez ponovimo na drugoj hrpi.

---

# Nim suma

Stanje igre određuje **Nim suma**, XOR veličina svih hrpa:
$$ S = x_1 \oplus x_2 \oplus \dots \oplus x_k $$

**Teorem (Bouton, 1901):**

- $S = 0$ $\Rightarrow$ stanje je **L**.
- $S \neq 0$ $\Rightarrow$ stanje je **W**.

**Primjer:** hrpe 5, 7 i 9.
$$ 0101_2 \oplus 0111_2 \oplus 1001_2 = 1011_2 = 11 \neq 0 $$

Prvi igrač pobjeđuje. Pobjednički potez: hrpu 9 smanjimo na $9 \oplus 11 = 2$, jer je $5 \oplus 7 \oplus 2 = 0$.

---

# Zašto Nim suma radi?

1. **Završno stanje** (sve hrpe prazne) ima $S = 0$ i to je L stanje.
2. **Iz $S = 0$ svaki potez daje $S \neq 0$.**
   Potez mijenja samo jednu hrpu $x_i \to x_i'$, pa je nova suma $S \oplus x_i \oplus x_i' = x_i \oplus x_i' \neq 0$.
3. **Iz $S \neq 0$ postoji potez u $S = 0$.**
   Neka je $d$ najviši postavljeni bit od $S$ i neka hrpa $x_i$ ima taj bit. Tada je $x_i \oplus S < x_i$ (bit $d$ se gasi, viši bitovi ostaju isti), pa hrpu smanjimo na $x_i \oplus S$. Nova suma je $0$.

Igrač sa $S \neq 0$ protivniku uvijek ostavlja $S = 0$, a protivnik mu uvijek mora vratiti $S \neq 0$. Kako igra završava, zadnji potez (u stanje $S = 0$ sa svim praznim hrpama) povlači igrač sa $S \neq 0$.

---

# Nim: kod

```cpp
// Tko pobjeđuje?
int s = 0;
for (int x : heaps) s ^= x;
cout << (s != 0 ? "first" : "second") << "\n";

// Pobjednički potez (ako je s != 0)
for (int i = 0; i < k; i++) {
    int target = heaps[i] ^ s;   // Nova veličina hrpe i
    if (target < heaps[i]) {     // Hrpa ima najviši postavljeni bit od s
        cout << "Hrpa " << i + 1 << ": uzmi " << heaps[i] - target << "\n";
        break;
    }
}
```

**Složenost:** $O(k)$ za odluku i za pobjednički potez.

---

# Nim korak po korak

Hrpe 3, 4 i 5. Mi uvijek vraćamo Nim sumu na 0, a protivnik uzima pola najveće hrpe.

<style scoped>
.gt-nim { margin-top: 0.3em; }
.gt-nim .turn { font-size: 20px; font-weight: bold; color: var(--main); margin-bottom: 0.4em; }
.gt-nim .grid { display: grid; gap: 5px; align-items: center; }
.gt-nim .th { height: 32px; line-height: 32px; text-align: center; font-size: 18px; font-weight: bold; color: #6e6e6e; border-radius: 6px; }
.gt-nim .th.hl { background: var(--main); color: #fff; }
.gt-nim .rl { height: 42px; line-height: 42px; padding: 0 10px; font-size: 20px; font-weight: bold; border-radius: 6px; transition: background-color .25s, color .25s; }
.gt-nim .rl.on { background: var(--main); color: #fff; }
.gt-nim .rl.sum { color: #6e6e6e; }
.gt-nim .toks { height: 42px; display: flex; align-items: center; gap: 4px; }
.gt-nim .tok { display: inline-block; width: 22px; height: 22px; border-radius: 50%; background: #f5db7e; border: 2px solid #141414; }
.gt-nim .tok.rm { background: #ffc9c9; border-color: #e03131; opacity: 0.6; }
.gt-nim .tc { height: 42px; line-height: 38px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s; }
.gt-nim .tc.zero { color: #b5b5b5; }
.gt-nim .tc.one { background: #e3ecf6; }
.gt-nim .tc.col { background: #f5db7e; }
.gt-nim .tc.sz { background: #9fdc9f; }
.gt-nim .tc.snz { background: #ffd8a8; }
.gt-nim .tc.cur { background: var(--main); color: #fff; }
.gt-nim .tc.dec { border-style: dashed; }
.gt-nim .line1, .gt-nim .line2 { font-family: monospace; font-size: 21px; min-height: 1.35em; }
.gt-nim .line1 { margin-top: 0.6em; }
.gt-nim .line2 { font-weight: bold; }
.gt-nim .ctrl { margin-top: 0.5em; }
.gt-nim button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gt-nim button:hover { background: var(--main); color: #fff; }
.gt-nim .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="gt-nim" data-heaps="3,4,5" data-bits="3">
  <div class="turn"></div>
  <div class="grid"></div>
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
  document.querySelectorAll('.gt-nim').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }

    var heaps = root.dataset.heaps.split(',').map(Number);
    var B = parseInt(root.dataset.bits, 10);
    var SUP = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'];
    function pw(d) { return '2' + SUP[d]; }
    function bit(x, d) { return Math.floor(x / Math.pow(2, d)) % 2; }
    function xorAll(h) { var r = 0; h.forEach(function (x) { r = r ^ x; }); return r; }
    function xorStr(h) { return h.join(' ⊕ '); }
    function empty() { return heaps.every(function (x) { return x === 0; }); }

    // Tablica: oznaka | žetoni | bitovi | vrijednost
    var grid = root.querySelector('.grid');
    grid.style.gridTemplateColumns = '130px 220px repeat(' + B + ', 50px) 70px';
    function cellAt(cls, text) { var e = mk('div', cls, text); grid.appendChild(e); return e; }
    cellAt('th', '');
    cellAt('th', 'Žetoni');
    var colHead = [];
    for (var d0 = B - 1; d0 !== -1; d0--) colHead.push(cellAt('th', pw(d0)));
    cellAt('th', '=');
    var rows = heaps.map(function (h, i) {
      var r = { lab: cellAt('rl', 'Hrpa ' + (i + 1)), toks: cellAt('toks', ''), bits: [], dec: null };
      for (var d = B - 1; d !== -1; d--) r.bits.push(cellAt('tc', ''));
      r.dec = cellAt('tc dec', '');
      return r;
    });
    var srow = { lab: cellAt('rl sum', 'S = XOR'), toks: cellAt('toks', ''), bits: [], dec: null };
    for (var d1 = B - 1; d1 !== -1; d1--) srow.bits.push(cellAt('tc', ''));
    srow.dec = cellAt('tc dec', '');
    var turnBox = root.querySelector('.turn');

    // Unaprijed odigramo cijelu partiju i spremimo svaki korak
    var snaps = [];
    function snap(o) {
      var s = { heaps: heaps.slice(), row: -1, col: -1, rm: -1, rc: 0, turn: 'Na potezu: mi (prvi igrač)', l1: '', l2: '' };
      Object.keys(o).forEach(function (k) { s[k] = o[k]; });
      snaps.push(s);
    }
    snap({ l1: 'Početno stanje: hrpe ' + heaps.join(', '),
      l2: 'Nim suma S = ' + xorStr(heaps) + ' = ' + xorAll(heaps) });
    var guard = 0;
    while (!empty()) {
      guard++;
      if (guard === 50) break;
      // Naš potez: vraćamo Nim sumu na 0
      var S = xorAll(heaps), d = B - 1;
      while (bit(S, d) === 0) d--;
      var i = 0;
      while (bit(heaps[i], d) === 0) i++;
      var nx = heaps[i] ^ S, c = heaps[i] - nx;
      snap({ col: d, l1: 'S = ' + S + ' ≠ 0, dakle mi smo u W stanju',
        l2: 'Najviši postavljeni bit od S je ' + pw(d) });
      snap({ col: d, row: i,
        l1: 'Hrpa ' + (i + 1) + ' ima bit ' + pw(d) + ':  ' + heaps[i] + ' ⊕ ' + S + ' = ' + nx + ', a to je manje od ' + heaps[i],
        l2: 'Hrpu ' + (i + 1) + ' smanjujemo na ' + nx + ' (uzimamo ' + c + ')' });
      heaps[i] = nx;
      var done = empty();
      snap({ row: i, rm: i, rc: c, turn: done ? 'Na potezu: protivnik, ali nema poteza' : 'Na potezu: protivnik',
        l1: 'Mi uzimamo ' + c + ' s hrpe ' + (i + 1) + ':  S = ' + xorStr(heaps) + ' = 0',
        l2: done ? 'Sve hrpe su prazne: protivnik ne može povući potez, pobijedili smo   ✓' : 'Protivnik je u L stanju (S = 0)   ✓' });
      if (done) break;
      // Protivnikov potez: uzima pola najveće hrpe (zaokruženo nagore)
      var j = 0;
      heaps.forEach(function (x, q) { if (x !== heaps[j]) { if (Math.max(x, heaps[j]) === x) j = q; } });
      var t = Math.ceil(heaps[j] / 2);
      heaps[j] -= t;
      snap({ row: j, rm: j, rc: t,
        l1: 'Protivnik uzima ' + t + ' s hrpe ' + (j + 1) + ':  S = ' + xorStr(heaps) + ' = ' + xorAll(heaps),
        l2: 'Iz S = 0 svaki potez daje S ≠ 0, pa smo opet u W stanju' });
    }

    function draw(s) {
      var S = xorAll(s.heaps);
      rows.forEach(function (r, i) {
        var x = s.heaps[i];
        r.lab.className = i === s.row ? 'rl on' : 'rl';
        r.toks.textContent = '';
        for (var a = 0; a !== x; a++) r.toks.appendChild(mk('span', 'tok'));
        if (i === s.rm) { for (var b = 0; b !== s.rc; b++) r.toks.appendChild(mk('span', 'tok rm')); }
        r.bits.forEach(function (e, jj) {
          var dd = B - 1 - jj, v = bit(x, dd), cls = v ? 'tc one' : 'tc zero';
          if (dd === s.col) cls += i === s.row ? ' cur' : ' col';
          e.className = cls;
          e.textContent = v;
        });
        r.dec.className = i === s.row ? 'tc dec col' : 'tc dec';
        r.dec.textContent = x;
      });
      var sc = S === 0 ? ' sz' : ' snz';
      srow.bits.forEach(function (e, jj) {
        var dd = B - 1 - jj;
        e.className = 'tc' + sc + (dd === s.col ? ' cur' : '');
        e.textContent = bit(S, dd);
      });
      srow.dec.className = 'tc dec' + sc;
      srow.dec.textContent = S;
      colHead.forEach(function (e, jj) { e.className = B - 1 - jj === s.col ? 'th hl' : 'th'; });
      turnBox.textContent = s.turn;
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

# Varijanta: misère Nim

U **misère** varijanti igrač koji uzme zadnji žeton **gubi**.

**Strategija:** igramo kao u običnom Nimu, osim pred sam kraj.

- Dok postoje barem dvije hrpe s 2 ili više žetona, igramo kao u Nimu.
- Kad ostane točno jedna hrpa s 2 ili više žetona, smanjimo je na 0 ili 1 tako da ostane **neparan** broj hrpa veličine 1.

**Tko pobjeđuje?**

- Ako su sve hrpe veličine najviše 1: prvi igrač pobjeđuje ako je broj jedinica **paran**.
- Inače: prvi igrač pobjeđuje ako je $S \neq 0$, kao u običnom Nimu.

---

<!-- _class: lead -->
# Sprague-Grundy teorem

## Svaka nepristrana igra je Nim hrpa

---

# Motivacija: zbroj igara

Što ako igramo **više igara odjednom**?

- Npr. nekoliko hrpa, a sa svake hrpe smijemo uzeti samo 2 ili 3 žetona.
- Igrač na potezu bira **jednu** podigru i u njoj povlači potez.
- Tko ne može povući potez ni u jednoj podigri, gubi.

W/L oznake podigara **nisu dovoljne**: Nim hrpe 1 i 1 (obje W) zajedno daju L stanje, a hrpe 1 i 2 (obje W) daju W stanje. DP po svim kombinacijama stanja podigara brzo postaje neizvediv.

**Rješenje:** svakom stanju pridružimo **broj** (ne samo W/L) koji se ponaša kao veličina Nim hrpe.

---

# Funkcija mex i Grundyjev broj

$\text{mex}(A)$ (*minimum excludant*) je **najmanji nenegativni cijeli broj koji nije u skupu** $A$.

- $\text{mex}(\{0, 1, 3\}) = 2$, $\quad \text{mex}(\{1, 2, 3\}) = 0$
- $\text{mex}(\{0, 1, 2\}) = 3$, $\quad \text{mex}(\emptyset) = 0$

**Grundyjev broj (nim-vrijednost) stanja $x$:**
$$ g(x) = \text{mex}(\{ g(y) \mid y \text{ je dostižan jednim potezom iz } x \}) $$

- $g(x) = 0$ $\iff$ $x$ je **L** stanje (nijedan potez ne vodi u stanje s $g = 0$).
- $g(x) > 0$ $\iff$ $x$ je **W** stanje (postoji potez u stanje s $g = 0$).

Grundyjev broj je, dakle, poopćenje W/L oznake.

---

# Zašto se Grundyjev broj ponaša kao Nim hrpa?

Neka je $g(x) = k$. Po definiciji mex-a:

- Iz $x$ možemo doći u stanja s Grundyjevim brojevima $0, 1, \dots, k-1$. To je točno kao Nim hrpa od $k$ žetona koju smanjujemo na bilo koju manju veličinu.
- Iz $x$ **ne možemo** doći u stanje s Grundyjevim brojem $k$.
- Možda možemo doći u stanje s brojem **većim** od $k$. Takav potez ne pomaže: protivnik ga poništi potezom natrag na vrijednost $k$.

Zato je stanje $x$ ekvivalentno Nim hrpi veličine $g(x)$.

Za Nim hrpu od $x$ žetona vrijedi $g(x) = \text{mex}\{0, 1, \dots, x-1\} = x$.

---

# Sprague-Grundy teorem: zbroj igara

**Teorem:** ako se igra sastoji od neovisnih podigara $G_1, G_2, \dots, G_m$ (svaki potez mijenja točno jednu), njezin Grundyjev broj je
$$ g(G) = g(G_1) \oplus g(G_2) \oplus \dots \oplus g(G_m) $$

**Recept:**

1. Rastavimo igru na **neovisne** podigre.
2. Za svaku podigru izračunamo Grundyjev broj (DP ili memoizacija + mex).
3. Izračunamo XOR svih Grundyjevih brojeva.
4. Ako je rezultat različit od 0, prvi igrač pobjeđuje.

Zbroj igara tako postaje običan Nim s hrpama veličina $g(G_1), \dots, g(G_m)$.

---

# Primjer: Grundyjevi brojevi za poteze {2, 3}

S hrpe smijemo uzeti **2 ili 3** žetona, pa je $g(n) = \text{mex}\{g(n-2), g(n-3)\}$.

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| dostižni $g$ | $\emptyset$ | $\emptyset$ | {0} | {0} | {0, 1} | {1} | {1, 2} | {0, 2} | {0} | {0, 1} |
| $g(n)$ | 0 | 0 | 1 | 1 | 2 | 0 | 0 | 1 | 1 | 2 |

Vrijednosti se ponavljaju s periodom 5: $0, 0, 1, 1, 2$.

**Zbroj igara:** hrpe 4, 7 i 9 daju $g = 2 \oplus 1 \oplus 2 = 1 \neq 0$, pa prvi igrač pobjeđuje.

---

# Kod: Grundyjevi brojevi

```cpp
vector<int> moves = {2, 3};
vector<int> g(n + 1);

for (int x = 0; x <= n; x++) {
    // g je najviše k (broj poteza), pa je niz veličine k + 1 dovoljan
    vector<bool> seen(moves.size() + 1, false);
    for (int m : moves)
        if (m <= x) seen[g[x - m]] = true;
    int mex = 0;
    while (seen[mex]) mex++;
    g[x] = mex;
}

int total = 0;
for (int h : heaps) total ^= g[h];   // Sprague-Grundy: XOR podigara
cout << (total != 0 ? "first" : "second") << "\n";
```

**Složenost:** $O(n \cdot k)$ za tablicu i $O(1)$ po hrpi.

---

# Grundyjevi brojevi korak po korak

Vrijednost u polju je $g(n)$. Žuti obrub: stanja dostižna potezom. Ispod je skup dostižnih vrijednosti, a mex je istaknut.

<style scoped>
.gt-grundy { margin-top: 0.4em; }
.gt-grundy .chips, .gt-grundy .mex { font-size: 20px; margin-bottom: 0.6em; }
.gt-grundy .mex { margin-top: 0.7em; margin-bottom: 0; }
.gt-grundy .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; transition: background-color .25s, color .25s; }
.gt-grundy .chip.in { background: #f5db7e; }
.gt-grundy .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gt-grundy .row { display: flex; gap: 6px; }
.gt-grundy .cell { width: 64px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s, box-shadow .25s; }
.gt-grundy .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gt-grundy .val { font-size: 28px; height: 44px; line-height: 44px; font-weight: bold; }
.gt-grundy .cell.todo .val { color: #b5b5b5; }
.gt-grundy .cell.w { background: #b2f2bb; }
.gt-grundy .cell.l { background: #ffc9c9; }
.gt-grundy .cell.src { box-shadow: 0 0 0 4px #f5b400; }
.gt-grundy .cell.cur { background: var(--main); color: #fff; }
.gt-grundy .cell.cur .idx, .gt-grundy .cell.cur .val { color: #fff; }
.gt-grundy .line1, .gt-grundy .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gt-grundy .line1 { margin-top: 0.6em; }
.gt-grundy .line2 { font-weight: bold; }
.gt-grundy .ctrl { margin-top: 0.6em; }
.gt-grundy button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gt-grundy button:hover { background: var(--main); color: #fff; }
.gt-grundy .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="gt-grundy" data-n="14" data-moves="2,3" data-heaps="4,7,9|4,9,5" data-note="Uzorak 0, 0, 1, 1, 2 ponavlja se s periodom 5">
  <div class="chips">Dozvoljeni potezi:</div>
  <div class="row"></div>
  <div class="mex">Dostižne vrijednosti:</div>
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
  document.querySelectorAll('.gt-grundy').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function le(a, b) { return Math.min(a, b) === a; }
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
    function uniq(a) {
      var r = [];
      a.forEach(function (x) { if (r.indexOf(x) === -1) r.push(x); });
      return r.sort(function (u, v) { return u - v; });
    }

    var N = parseInt(root.dataset.n, 10);
    var moves = root.dataset.moves.split(',').map(Number);
    var chipsBox = root.querySelector('.chips');
    moves.forEach(function (m) { chipsBox.appendChild(mk('span', 'chip', m)); });
    var R = makeRow(root.querySelector('.row'), N + 1, 0);
    // mex je najviše broj poteza, pa su dovoljne vrijednosti 0..k
    var mexBox = root.querySelector('.mex');
    var mexChips = [];
    for (var q = 0; q !== moves.length + 1; q++) { var mc = mk('span', 'chip', q); mexBox.appendChild(mc); mexChips.push(mc); }

    // Unaprijed izračunamo sve korake (jedan korak = jedno stanje n)
    var g = [];
    var snaps = [];
    for (var x = 0; x !== N + 1; x++) {
      var src = [], parts = [], vals = [];
      moves.forEach(function (m) {
        if (le(m, x)) { src.push(x - m); parts.push('g(' + (x - m) + ')'); vals.push(g[x - m]); }
      });
      var mex = 0;
      while (vals.indexOf(mex) !== -1) mex++;
      g.push(mex);
      var set = uniq(vals);
      snaps.push({ upto: x, cur: x, src: src, set: set, mex: mex,
        l1: parts.length
          ? 'g(' + x + ') = mex{' + parts.join(', ') + '} = mex{' + set.join(', ') + '}'
          : 'g(' + x + ') = mex{} (nema poteza)',
        l2: 'Najmanji broj koji nedostaje: g(' + x + ') = ' + mex + (mex === 0 ? '   → L stanje' : '   → W stanje') });
    }
    snaps.push({ upto: N, cur: -1, src: [], set: null, mex: -1,
      l1: 'g = ' + g.join(', '), l2: root.dataset.note });
    root.dataset.heaps.split('|').forEach(function (qq) {
      var hs = qq.split(',').map(Number), G = 0;
      hs.forEach(function (h) { G = G ^ g[h]; });
      snaps.push({ upto: N, cur: -1, src: hs, set: null, mex: -1,
        l1: 'Zbroj igara, hrpe ' + hs.join(', ') + ':  G = ' + hs.map(function (h) { return g[h]; }).join(' ⊕ ') + ' = ' + G,
        l2: G !== 0 ? 'G ≠ 0 → prvi igrač pobjeđuje   ✓' : 'G = 0 → drugi igrač pobjeđuje   ✓' });
    });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        var cls = 'cell';
        if (le(k, s.upto)) cls += g[k] === 0 ? ' l' : ' w';
        else cls += ' todo';
        if (s.src.indexOf(k) !== -1) cls += ' src';
        if (k === s.cur) cls += ' cur';
        c.className = cls;
        R.vals[k].textContent = le(k, s.upto) ? g[k] : '';
      });
      mexChips.forEach(function (ch, v) {
        var cls = 'chip';
        if (s.set) {
          if (s.set.indexOf(v) !== -1) cls += ' in';
          if (v === s.mex) cls += ' on';
        }
        ch.className = cls;
      });
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

# Pobjednički potez u zbroju igara

Neka je $G = g_1 \oplus g_2 \oplus \dots \oplus g_m \neq 0$.

- Kao u Nimu, tražimo podigru $i$ za koju je $g_i \oplus G < g_i$.
- Po definiciji mex-a iz te podigre **postoji** potez u stanje s Grundyjevim brojem točno $g_i \oplus G$.
- Nakon tog poteza ukupni XOR je $0$, pa je protivnik u L stanju.

**Važno:** podigre moraju biti **neovisne**. Ako jedan potez mijenja više podigara odjednom, XOR pravilo ne vrijedi.

---

<!-- _class: lead -->
# Zadaci za vježbu

## CSES i Codeforces

---

# CSES Problem Set (Mathematics)

1. **[Stick Game](https://cses.fi/problemset/task/1729):** W/L stanja za sve $n$ (DP).
2. **[Nim Game I](https://cses.fi/problemset/task/1730):** klasični Nim, XOR svih hrpa.
3. **[Nim Game II](https://cses.fi/problemset/task/1098):** s hrpe uzimamo 1, 2 ili 3 štapića. *Hint:* modulo 4.
4. **[Stair Game](https://cses.fi/problemset/task/1099):** Nim na stepenicama. *Hint:* bitne su samo parne stepenice.
5. **[Grundy's Game](https://cses.fi/problemset/task/2207):** dijeljenje hrpe na dvije nejednake. Sprague-Grundy u praksi.
6. **[Another Game](https://cses.fi/problemset/task/2208):** sa svake odabrane hrpe uzimamo po jedan novčić. *Hint:* parnost.

---

# Codeforces preporuke

Tražite zadatke s tagom `games`. Lakši su često ad-hoc (Div2 A/B), a teži koriste Sprague-Grundy (Div2 D/E).

- **[1-2-K Game](https://codeforces.com/problemset/problem/1194/D)**
  - Igra oduzimanja s potezima 1, 2 i $k$ uz ogroman $n$: tražimo uzorak.
- **[Deleting Divisors](https://codeforces.com/problemset/problem/1537/D)**
  - Srodna igri s djeliteljima: W/L za male $n$, zatim uzorak.
- **[Stoned Game](https://codeforces.com/problemset/problem/1396/B)**
  - Ad-hoc argument s parnošću i najvećom hrpom.

---

<!-- _class: title -->
# Stick Game (CSES)

## W/L stanja dinamičkim programiranjem

---

# Analiza: Stick Game

**Problem:**
Hrpa štapića i skup dozvoljenih poteza $P = \{p_1, \dots, p_k\}$ (u potezu uzmemo točno $p_i$ štapića). Tko uzme zadnji štapić, pobjeđuje. Za **svaki** $n = 1, 2, \dots, N$ treba ispisati je li stanje W ili L.
**Ograničenja:** $N \le 10^6$, $k \le 100$.

**Intuicija:**
Ovo je točno W/L analiza s početka predavanja, samo s proizvoljnim skupom poteza.

- `win[0] = false` (nema štapića, igrač na potezu je izgubio).
- `win[x] = true` ako postoji $p \in P$, $p \le x$, takav da je `win[x - p] = false`.

**Složenost:** $O(N \cdot k)$, najviše $10^8$ jednostavnih operacija, što prolazi.

---

# Implementacija: Stick Game

```cpp
int n, k;
cin >> n >> k;
vector<int> p(k);
for (int &x : p) cin >> x;

// win[x] = je li stanje s x štapića pobjedničko (W)
vector<bool> win(n + 1, false);
for (int x = 1; x <= n; x++)
    for (int m : p)
        if (m <= x && !win[x - m]) { win[x] = true; break; }

string ans;
for (int x = 1; x <= n; x++) ans += win[x] ? 'W' : 'L';
cout << ans << "\n";
```

**Napomena:** `break` prekida provjeru čim nađemo potez u L stanje, pa W stanja obično obradimo brzo.

---

# Stick Game korak po korak

Primjer iz zadatka: $P = \{1, 3, 4\}$ i $N = 10$. Očekivani izlaz je `WLWWWWLWLW`.

<style scoped>
.gt-stick { margin-top: 0.4em; }
.gt-stick .chips { font-size: 20px; margin-bottom: 0.6em; }
.gt-stick .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; }
.gt-stick .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gt-stick .chip.skip { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gt-stick .row { display: flex; gap: 8px; }
.gt-stick .cell { width: 78px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s, box-shadow .25s; }
.gt-stick .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gt-stick .val { font-size: 30px; height: 46px; line-height: 46px; font-weight: bold; }
.gt-stick .cell.todo .val { color: #b5b5b5; }
.gt-stick .cell.w { background: #b2f2bb; }
.gt-stick .cell.l { background: #ffc9c9; }
.gt-stick .cell.src { box-shadow: 0 0 0 4px #f5b400; }
.gt-stick .cell.tgt { box-shadow: 0 0 0 4px #e03131; }
.gt-stick .cell.cur { background: var(--main); color: #fff; }
.gt-stick .cell.cur .idx, .gt-stick .cell.cur .val { color: #fff; }
.gt-stick .line1, .gt-stick .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gt-stick .line1 { margin-top: 0.8em; }
.gt-stick .line2 { font-weight: bold; }
.gt-stick .ctrl { margin-top: 0.7em; }
.gt-stick button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gt-stick button:hover { background: var(--main); color: #fff; }
.gt-stick .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="gt-stick" data-n="10" data-moves="1,3,4" data-note="Izlaz za n = 1..10: WLWWWWLWLW (kao u primjeru)   ✓">
  <div class="chips">Dozvoljeni potezi:</div>
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
  document.querySelectorAll('.gt-stick').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function le(a, b) { return Math.min(a, b) === a; }
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

    var N = parseInt(root.dataset.n, 10);
    var moves = root.dataset.moves.split(',').map(Number);
    var chipsBox = root.querySelector('.chips');
    var chips = moves.map(function (m) { var s = mk('span', 'chip', m); chipsBox.appendChild(s); return s; });
    var R = makeRow(root.querySelector('.row'), N + 1, 0);

    // Unaprijed izračunamo sve korake (jedan korak = jedno stanje n)
    var win = [false];
    var snaps = [{ upto: 0, cur: 0, src: [], tgt: -1, tm: -1, fin: false,
      l1: 'n = 0: nema štapića, igrač na potezu ne može povući potez',
      l2: 'Stanje 0 je L (gubitničko)' }];
    for (var x = 1; x !== N + 1; x++) {
      var src = [], parts = [], tgt = -1, tm = -1;
      moves.forEach(function (m, mi) {
        if (le(m, x)) {
          src.push(x - m);
          parts.push((x - m) + ' (' + (win[x - m] ? 'W' : 'L') + ')');
          if (tgt === -1) {
            if (!win[x - m]) { tgt = x - m; tm = mi; }
          }
        }
      });
      win.push(tgt !== -1);
      snaps.push({ upto: x, cur: x, src: src, tgt: tgt, tm: tm, fin: false,
        l1: 'n = ' + x + ': potezi vode u ' + parts.join(', '),
        l2: tgt !== -1
          ? x + ' je W: uzmemo ' + moves[tm] + ' i protivnika ostavimo u L stanju ' + tgt + '   ✓'
          : x + ' je L: svi potezi vode u W stanja' });
    }
    var lose = [];
    for (var k = 0; k !== N + 1; k++) { if (!win[k]) lose.push(k); }
    snaps.push({ upto: N, cur: -1, src: [], tgt: -1, tm: -1, fin: true,
      l1: 'L stanja: ' + lose.join(', '), l2: root.dataset.note });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        var cls = 'cell';
        if (le(k, s.upto)) cls += win[k] ? ' w' : ' l';
        else cls += ' todo';
        if (s.src.indexOf(k) !== -1) cls += ' src';
        if (k === s.tgt) cls += ' tgt';
        if (s.fin) { if (!win[k]) cls += ' tgt'; }
        if (k === s.cur) cls += ' cur';
        c.className = cls;
        R.vals[k].textContent = le(k, s.upto) ? (win[k] ? 'W' : 'L') : '';
      });
      chips.forEach(function (ch, mi) {
        var cls = 'chip';
        if (s.cur !== -1) { if (!le(moves[mi], s.cur)) cls += ' skip'; }
        if (mi === s.tm) cls += ' on';
        ch.className = cls;
      });
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
# Nim Game I (CSES)

## Klasični Nim

---

# Analiza: Nim Game I

**Problem:**
$t$ testova. U svakom je $n$ hrpa veličina $x_1, \dots, x_n$, a s jedne hrpe smijemo uzeti proizvoljno mnogo štapića. Tko uzme zadnji, pobjeđuje. Tko pobjeđuje?
**Ograničenja:** $\sum n \le 2 \cdot 10^5$, $x_i \le 10^9$.

**Intuicija:**
Izravna primjena Boutonova teorema. Računamo $S = x_1 \oplus x_2 \oplus \dots \oplus x_n$.

- $S \neq 0$ $\Rightarrow$ `first`
- $S = 0$ $\Rightarrow$ `second`

**Primjer iz zadatka:** $3 \oplus 5 \oplus 6 = 011_2 \oplus 101_2 \oplus 110_2 = 0$, pa pobjeđuje drugi igrač.

---

# Implementacija: Nim Game I

```cpp
#include <iostream>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        int s = 0;                    // Nim suma
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            s ^= x;
        }
        cout << (s != 0 ? "first" : "second") << "\n";
    }
}
```

---

<!-- _class: title -->
# Nim Game II (CSES)

## Sprague-Grundy na djelu

---

# Analiza: Nim Game II

**Problem:** kao Nim Game I, ali s hrpe smijemo uzeti samo **1, 2 ili 3** štapića.

**Intuicija (Sprague-Grundy):**
Hrpe su neovisne podigre. Svaka je igra oduzimanja s potezima $\{1, 2, 3\}$:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| $g(x)$ | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 | 0 |

Dakle, $g(x) = x \bmod 4$, a odgovor određuje
$$ G = (x_1 \bmod 4) \oplus (x_2 \bmod 4) \oplus \dots \oplus (x_n \bmod 4) $$

**Pazite:** XOR samih $x_i$ ovdje je **pogrešan** (to bi bio običan Nim)!

---

# Implementacija: Nim Game II

Jedina promjena u odnosu na Nim Game I je Grundyjev broj hrpe:

```cpp
while (t--) {
    int n;
    cin >> n;
    int s = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s ^= x % 4;                   // g(x) = x mod 4
    }
    cout << (s != 0 ? "first" : "second") << "\n";
}
```

**Primjer iz zadatka:** hrpe 5, 7, 2, 5 daju $1 \oplus 3 \oplus 2 \oplus 1 = 1 \neq 0$, pa pobjeđuje prvi igrač.

---

<!-- _class: title -->
# Stair Game (CSES)

## Nim na stepenicama

---

# Analiza: Stair Game (1/2)

**Problem:**
Stepenice su numerirane $1, 2, \dots, n$, a na stepenici $k$ je $p_k$ loptica. U potezu biramo stepenicu $k \ne 1$ i **proizvoljan broj** loptica s nje pomičemo na stepenicu $k - 1$. Tko povuče zadnji potez, pobjeđuje.

**Intuicija (staircase Nim):**
Stepenica 1 je "pod": loptice s nje se više ne pomiču.

- Loptice na **parnim** stepenicama ($2, 4, 6, \dots$) ponašaju se kao **Nim hrpe**: pomak s parne na neparnu stepenicu isto je što i uzimanje žetona s hrpe.
- Loptice na **neparnim** stepenicama ne utječu na ishod.

**Odgovor:** $p_2 \oplus p_4 \oplus p_6 \oplus \dots \neq 0$ $\Rightarrow$ `first`, inače `second`.

---

# Analiza: Stair Game (2/2)

**Zašto neparne stepenice ne smetaju?**

Neka je XOR parnih stepenica 0 i neka protivnik pomakne $c$ loptica s **neparne** stepenice $k \ge 3$ na parnu stepenicu $k - 1$.
Mi tada pomaknemo **istih $c$ loptica** s $k - 1$ na $k - 2$ (neparna). Parne stepenice su opet kao prije.

Protivnikov potez je "poništen". Loptice se samo spuštaju, pa takvih poteza ima konačno mnogo.

**Primjeri iz zadatka:**

- $p = (0, 2, 1)$: parne stepenice daju $p_2 = 2 \neq 0$, pa je odgovor `first`.
- $p = (1, 1, 1, 1)$: $p_2 \oplus p_4 = 1 \oplus 1 = 0$, pa je odgovor `second`.

---

# Implementacija: Stair Game

```cpp
while (t--) {
    int n;
    cin >> n;
    int s = 0;
    for (int i = 1; i <= n; i++) {
        int p;
        cin >> p;
        if (i % 2 == 0) s ^= p;       // Samo parne stepenice
    }
    cout << (s != 0 ? "first" : "second") << "\n";
}
```

**Pazite na indeksiranje:** stepenice u zadatku kreću od 1. Ako učitavate u niz od indeksa 0, parne stepenice su na **neparnim** indeksima.

---

<!-- _class: title -->
# Grundy's Game (CSES)

## Dijeljenje hrpe i potraga za uzorkom

---

# Analiza: Grundy's Game (1/2)

**Problem:**
Hrpa od $n$ novčića. U potezu biramo jednu hrpu i dijelimo je na **dvije neprazne hrpe različitih veličina**. Tko povuče zadnji potez, pobjeđuje.
**Ograničenja:** $n \le 10^6$, $t \le 10^5$ testova.

**Intuicija (Sprague-Grundy):**
Nakon podjele $n = a + b$ imamo **dvije neovisne podigre**, pa je Grundyjev broj novog stanja $g(a) \oplus g(b)$:
$$ g(n) = \text{mex}\{\, g(a) \oplus g(n - a) \;:\; 1 \le a < n - a \,\} $$

Hrpe od 1 i 2 novčića ne možemo podijeliti, pa je $g(1) = g(2) = 0$.
Izračun za sve $n$ do $10^6$ je $O(n^2)$, što je **presporo**!

---

# Grundy's Game korak po korak

Za svaki $n$ isprobamo sve podjele $a + b$ uz $a < b$. Podjela na dvije jednake hrpe nije dozvoljena.

<style scoped>
.gt-split { margin-top: 0.4em; }
.gt-split .chips, .gt-split .mex { font-size: 20px; }
.gt-split .chips { margin-top: 0.7em; min-height: 36px; }
.gt-split .mex { margin-top: 0.4em; }
.gt-split .chip { display: inline-block; min-width: 32px; text-align: center; padding: 2px 10px; margin-left: 6px; border: 2px solid #141414; border-radius: 16px; font-weight: bold; font-size: 18px; transition: background-color .25s, color .25s; }
.gt-split .chip.in { background: #f5db7e; }
.gt-split .chip.on { background: var(--main); border-color: var(--main); color: #fff; }
.gt-split .chip.skip { color: #b5b5b5; border-color: #ccc; text-decoration: line-through; }
.gt-split .list .chip { font-size: 17px; padding: 2px 8px; }
.gt-split .muted { color: #6e6e6e; font-style: italic; margin-left: 6px; }
.gt-split .row { display: flex; gap: 8px; }
.gt-split .cell { width: 72px; text-align: center; border: 2px solid #141414; border-radius: 6px; transition: background-color .25s, color .25s, box-shadow .25s; }
.gt-split .idx { font-size: 16px; color: #6e6e6e; border-bottom: 1px solid #ccc; }
.gt-split .val { font-size: 28px; height: 44px; line-height: 44px; font-weight: bold; }
.gt-split .cell.todo .val { color: #b5b5b5; }
.gt-split .cell.w { background: #b2f2bb; }
.gt-split .cell.l { background: #ffc9c9; }
.gt-split .cell.tgt { box-shadow: 0 0 0 4px #e03131; }
.gt-split .cell.cur { background: var(--main); color: #fff; }
.gt-split .cell.cur .idx, .gt-split .cell.cur .val { color: #fff; }
.gt-split .line1, .gt-split .line2 { font-family: monospace; font-size: 22px; min-height: 1.4em; }
.gt-split .line1 { margin-top: 0.6em; }
.gt-split .line2 { font-weight: bold; }
.gt-split .ctrl { margin-top: 0.6em; }
.gt-split button { font: inherit; font-size: 18px; padding: 4px 14px; margin-right: 8px; border: 2px solid var(--main); border-radius: 6px; background: #fff; color: var(--main); cursor: pointer; }
.gt-split button:hover { background: var(--main); color: #fff; }
.gt-split .hint { font-size: 16px; color: #6e6e6e; }
</style>

<div class="gt-split" data-n="13">
  <div class="row"></div>
  <div class="chips">Podjele:<span class="list"></span></div>
  <div class="mex">Dostižne vrijednosti:</div>
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
  document.querySelectorAll('.gt-split').forEach(function (root) {
    var slide = root.closest('svg');
    var line1 = root.querySelector('.line1');
    var line2 = root.querySelector('.line2');
    function mk(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text !== undefined) e.textContent = text;
      return e;
    }
    function le(a, b) { return Math.min(a, b) === a; }
    function lt(a, b) { return a !== b ? Math.min(a, b) === a : false; }
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
    function uniq(a) {
      var r = [];
      a.forEach(function (x) { if (r.indexOf(x) === -1) r.push(x); });
      return r.sort(function (u, v) { return u - v; });
    }

    var N = parseInt(root.dataset.n, 10);
    var R = makeRow(root.querySelector('.row'), N, 1);
    var list = root.querySelector('.list');
    // Broj podjela je najviše (N - 1) / 2, a mex je najviše broj podjela
    var K = Math.floor((N - 1) / 2);
    var mexBox = root.querySelector('.mex');
    var mexChips = [];
    for (var q = 0; q !== K + 1; q++) { var mc = mk('span', 'chip', q); mexBox.appendChild(mc); mexChips.push(mc); }

    // Unaprijed izračunamo sve korake (jedan korak = jedna veličina hrpe n)
    var g = [0];
    var snaps = [];
    for (var n = 1; n !== N + 1; n++) {
      var sp = [], vals = [];
      for (var a = 1; lt(a, n - a); a++) {
        var v = g[a] ^ g[n - a];
        sp.push({ t: a + '+' + (n - a) + ': ' + g[a] + '⊕' + g[n - a] + '=' + v, bad: false });
        vals.push(v);
      }
      if (n % 2 === 0) sp.push({ t: (n / 2) + '+' + (n / 2), bad: true });
      var mex = 0;
      while (vals.indexOf(mex) !== -1) mex++;
      g.push(mex);
      var set = uniq(vals), l1;
      if (n === 1) l1 = 'n = 1: hrpu od jednog novčića ne možemo podijeliti, g(1) = mex{} = 0';
      else if (vals.length === 0) l1 = 'n = ' + n + ': jedina podjela ' + (n / 2) + '+' + (n / 2) + ' nije dozvoljena, g(' + n + ') = mex{} = 0';
      else l1 = 'g(' + n + ') = mex{' + set.join(', ') + '} = ' + mex;
      snaps.push({ upto: n, cur: n, sp: sp, set: set, mex: mex, fin: false, l1: l1,
        l2: mex === 0 ? 'L stanje: igrač na potezu gubi (CSES: second)' : 'W stanje: igrač na potezu pobjeđuje (CSES: first)' });
    }
    var lose = [];
    for (var k = 1; k !== N + 1; k++) { if (g[k] === 0) lose.push(k); }
    snaps.push({ upto: N, cur: -1, sp: [], set: null, mex: -1, fin: true,
      l1: 'L stanja do ' + N + ': ' + lose.join(', '),
      l2: 'Niz se nastavlja: 20, 23, 26, 50, 53, …, a zadnje L stanje je n = 1222' });

    function draw(s) {
      R.cells.forEach(function (c, k) {
        var v = k + 1, cls = 'cell';
        if (le(v, s.upto)) cls += g[v] === 0 ? ' l' : ' w';
        else cls += ' todo';
        if (s.fin) { if (g[v] === 0) cls += ' tgt'; }
        if (v === s.cur) cls += ' cur';
        c.className = cls;
        R.vals[k].textContent = le(v, s.upto) ? g[v] : '';
      });
      list.textContent = '';
      s.sp.forEach(function (p) { list.appendChild(mk('span', p.bad ? 'chip skip' : 'chip', p.t)); });
      if (s.sp.length === 0) { if (s.cur !== -1) list.appendChild(mk('span', 'muted', 'nema podjela')); }
      mexChips.forEach(function (ch, v) {
        var cls = 'chip';
        if (s.set) {
          if (s.set.indexOf(v) !== -1) cls += ' in';
          if (v === s.mex) cls += ' on';
        }
        ch.className = cls;
      });
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

# Analiza: Grundy's Game (2/2)

**Opažanje (eksperimentom):**
Izračunamo $g(n)$ za male $n$ i ispišemo sve $n$ za koje je $g(n) = 0$:
$$ n \in \{1, 2, 4, 7, 10, 20, 23, 26, 50, 53, \dots, 1222\} $$

Nakon $n = 1222$ više nema L stanja (provjereno računalno daleko iznad $10^6$).

**Rješenje:**

- Za $n \le 2000$ (s rezervom iznad 1222) računamo $g(n)$ izravno, u $O(2000^2)$.
- Za $n > 2000$ odgovor je uvijek `first`.

**Pouka:** kad formula nije očita, napišite brute force za male $n$ i **tražite uzorak**.

---

# Implementacija: Grundy's Game (1/2)

Predračun Grundyjevih brojeva za $n \le 2000$:

```cpp
const int LIM = 2000;   // Zadnje L stanje je 1222, LIM je s rezervom
int g[LIM + 1];         // g[1] = g[2] = 0 (globalni niz je već nula)

void precompute() {
    for (int n = 3; n <= LIM; n++) {
        // Vrijednosti g su ovdje male (manje od 64), pa LIM mjesta sigurno dostaje
        vector<bool> seen(LIM, false);
        for (int a = 1; 2 * a < n; a++)     // a < n - a: hrpe moraju biti različite
            seen[g[a] ^ g[n - a]] = true;

        int mex = 0;
        while (seen[mex]) mex++;
        g[n] = mex;
    }
}
```

**Složenost predračuna:** oko $\frac{2000^2}{4} = 10^6$ operacija.

---

# Implementacija: Grundy's Game (2/2)

```cpp
#include <iostream>
#include <vector>
using namespace std;

// ... LIM, g[] i precompute() s prethodnog slajda ...

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    precompute();

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        bool win = (n > LIM) || g[n] != 0;   // Iznad LIM nema L stanja
        cout << (win ? "first" : "second") << "\n";
    }
}
```

---

<!-- _class: title -->
# Another Game (CSES)

## Kad Sprague-Grundy ne pomaže: parnost

---

# Analiza: Another Game

**Problem:** $n$ hrpa novčića. U potezu biramo **bilo koji neprazan skup** nepraznih hrpa i sa svake uzmemo **po jedan** novčić. Tko uzme zadnji novčić, pobjeđuje.

**Intuicija (parnost):**

- Ako su **sve hrpe parne**, svaki potez barem jednu hrpu čini **neparnom**. Protivnik tada uzme po jedan novčić sa svih neparnih hrpa i opet su sve parne.
- Završno stanje (sve hrpe 0) je "sve parno", pa je "sve parno" **L** stanje.
- Ako postoji neparna hrpa, uzmemo po jedan novčić sa svih neparnih hrpa i protivnika stavimo u L stanje.

**Odgovor:** `first` ako postoji barem jedna neparna hrpa, inače `second`.
Sprague-Grundy ovdje ne pomaže izravno: potez mijenja više hrpa, pa hrpe **nisu neovisne**.

---

# Implementacija: Another Game

```cpp
while (t--) {
    int n;
    cin >> n;
    bool odd = false;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x % 2 == 1) odd = true;   // Postoji neparna hrpa
    }
    cout << (odd ? "first" : "second") << "\n";
}
```

**Primjeri iz zadatka:**

- $(1, 2, 3)$: postoji neparna hrpa, pa je odgovor `first`.
- $(2, 2)$: sve hrpe su parne, pa je odgovor `second`.

---

<!-- _class: title -->
# Zaključak i najbitnije napomene

---

# Što smo danas naučili?

1. **W/L stanja:**
   - L: svi potezi vode u W. W: postoji potez u L.
   - Računamo ih DP-om od završnih stanja prema početnom.
2. **Nim:**
   - Stanje je L $\iff$ XOR veličina svih hrpa je 0.
   - Pobjednički potez: hrpu $x_i$ smanjimo na $x_i \oplus S$.
3. **Sprague-Grundy teorem:**
   - $g(x)$ je mex Grundyjevih brojeva stanja dostižnih jednim potezom.
   - Zbroj neovisnih igara ima Grundyjev broj jednak XOR-u Grundyjevih brojeva podigara.

---

# Savjeti za rješavanje zadataka

- **Brute force, pa uzorak:**
  - Napišite W/L (ili Grundy) DP za male ulaze i ispišite tablicu. Uzorak (modulo, parnost, periodičnost) često je cijelo rješenje.
- **Tražite neovisne podigre:**
  - Ako se igra raspada na dijelove koji se ne ometaju, računamo XOR Grundyjevih brojeva.
- **Simetrija i parnost:**
  - Strategija zrcaljenja (ponovimo protivnikov potez "na drugoj strani") rješava mnoge ad-hoc zadatke.
- **Pazite na pravilo kraja:**
  - Normalna igra (zadnji potez pobjeđuje) i misère (zadnji potez gubi) imaju različita rješenja.
