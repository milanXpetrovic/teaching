---
nav_exclude: true
---

# Završni pregled i strategija razvoja

## Sadržaj

1. [Od algoritama do inženjerstva](#od-algoritama-do-inženjerstva)
2. [Kvaliteta koda: Natjecanje vs. Industrija](#kvaliteta-koda-natjecanje-vs-industrija)
3. [Strategija rješavanja nepoznatih problema](#strategija-rješavanja-nepoznatih-problema)
4. [Tehnički intervjui i karijera](#tehnički-intervjui-i-karijera)
5. [Kako ostati u formi?](#kako-ostati-u-formi)

---

## Od algoritama do inženjerstva

Čestitamo! Došli ste do kraja kolegija koji pokriva neke od najkompleksnijih i najljepših koncepata u računalnoj znanosti. No, postavlja se pitanje: **"Hoću li ja ovo ikada koristiti u stvarnom poslu?"**

Odgovor je: **Rijetko ćete implementirati Dijkstra algoritam od nule, ali ćete svakodnevno koristiti način razmišljanja koji ste ovdje razvili.**

Ovaj kolegij vas nije učio samo "kako sortirati niz", već vas je naučio:

1. **Apstraktnom razmišljanju:** Kako stvarni problem (npr. mreža dostave, preporuka prijatelja, parsiranje konfiguracije) modelirati kao graf, stablo ili problem toka.
2. **Analizi performansi:** Razumijevanje zašto aplikacija radi sporo kada broj korisnika naraste s 1,000 na 1,000,000 (razlika između $O(N^2)$ i $O(N \log N)$).
3. **Rubnim slučajevima:** Naviku da se pitate "Što ako je ulaz prazan?", "Što ako su svi brojevi negativni?". To je temelj QA (Quality Assurance) i robusnog softvera.

---

## Kvaliteta koda: Natjecanje vs. Industrija

Tijekom vježbi često smo pisali "brzi" kod karakterističan za natjecateljsko programiranje (kratka imena varijabli, globalne varijable, makroi). U profesionalnom razvoju softvera, prioriteti su drugačiji.

### 1. Imenovanje varijabli

* **Natjecanje:** `adj`, `q`, `vis`, `dfs(u)`. Cilj je brzina tipkanja.
* **Industrija:** `adjacencyList`, `userQueue`, `visitedNodes`, `findConnectedComponents(userId)`.
  * **Pravilo:** Kod se čita puno češće nego što se piše. Imena moraju otkrivati *namjeru*.

### 2. Struktura i Modularnost

* **Natjecanje:** Sve u jednoj `main` funkciji ili par globalnih funkcija.
* **Industrija:** Klase, enkapsulacija, *Single Responsibility Principle*.
  * Algoritam za *Shortest Path* trebao bi biti u zasebnoj klasi ili servisu, odvojen od logike učitavanja podataka ili ispisa.

### 3. Testiranje

* **Natjecanje:** Testiranje na primjeru iz zadatka i "nadaj se najboljem".
* **Industrija:**
  * **Unit testovi:** Testiranje svake komponente izolirano.
  * **Rubni slučajevi:** Eksplicitni testovi za prazne grafove, stabla s jednim čvorom, itd.
  * **Regression testing:** Osiguravanje da popravak buga nije stvorio novi bug.

### 4. Korištenje biblioteka

Na kolegiju smo implementirali strukture od nule da bismo ih razumjeli. U poslu **uvijek koristite provjerene standardne biblioteke** (`std::sort`, `std::priority_queue`, vanjske biblioteke za grafove). One su optimizirane, testirane i održavane.

---

## Strategija rješavanja nepoznatih problema

Kada se u karijeri susretnete s teškim problemom koji ne znate riješiti odmah, primijenite inženjerski pristup koji smo vježbali:

1. **Razumijevanje zahtjeva:**
    * Nemojte odmah početi kodirati. Pročitajte specifikaciju, pitajte za nejasnoće, definirajte ulaze i izlaze.
    * *Primjer:* "Trebamo li podržati negativne težine?" (Odgovor mijenja izbor algoritma iz Dijkstre u Bellman-Ford).

2. **Apstrakcija i Modeliranje:**
    * Pokušajte svesti problem na nešto poznato.
    * Je li ovo problem pretrage? Optimizacije? Može li se modelirati kao graf?

3. **Gruba sila (Brute Force) kao početak:**
    * Često je bolje prvo napisati jednostavno, točno, ali sporo rješenje.
    * Ono služi kao referenca za točnost (baseline) pri optimizaciji i pomaže u razumijevanju problema.

4. **Optimizacija (Korak po korak):**
    * Gdje je usko grlo (bottleneck)?
    * Mogu li koristiti bolju strukturu podataka (npr. `Hash Map` umjesto `List` za pretragu)?
    * Mogu li izbjeći ponovljene izračune (Dinamičko programiranje)?

5. **Debugiranje:**
    * Nemojte nasumično mijenjati kod.
    * Koristite **Rubber Duck Debugging**: Objasnite svoj kod red po red (naglas) gumenoj patkici (ili kolegi). Često ćete sami uočiti grešku.

---

## Tehnički intervjui i karijera

Znanje s ovog kolegija je **zlatni standard** za tehničke intervjue u vodećim svjetskim tehnološkim tvrtkama (Google, Meta, Amazon, ali i vrhunske domaće tvrtke).

**Što se traži na intervjuu?**
Nije cilj samo doći do točnog rješenja u tišini. Intervjueri traže:

1. **Komunikaciju:** Razmišljajte naglas. Objasnite zašto birate `set` umjesto `vector`.
2. **Analizu složenosti:** Morate znati reći vremensku i prostornu složenost svog rješenja ($O$-notacija).
3. **Testiranje:** Sami predložite testne primjere (uključujući rubne slučajeve) prije nego vam ih intervjuer da.
4. **Čitljiv kod:** Pišite kod koji bi vaš kolega mogao razumjeti.

**Resursi za pripremu:**

* *LeetCode* / *HackerRank* (fokus na "Interview Preparation" setove).
* Knjiga: *Cracking the Coding Interview* (Gayle Laakmann McDowell).

---

## Kako ostati u formi?

Algoritamske vještine su kao mišići – atrofiraju ako se ne koriste.

1. **Rješavajte zadataka:** Održavajte mentalnu kondiciju na platformama poput LeetCode, Codeforces ili CSES.
2. **Sudjelujte u natjecanjima (opcionalno):** Google Code Jam, Advent of Code (svakog prosinca – izvrsno za zabavu i učenje).
3. **Primjenjujte znanje:** Kada radite na projektu i trebate pretražiti veliku količinu podataka, sjetite se stabala ili hashiranja. Kada imate složene ovisnosti taskova, sjetite se topološkog sortiranja.

### Zaključak

Cilj ovog kolegija bio je pretvoriti vas iz "osobe koja zna sintaksu jezika" u **inženjera koji zna rješavati probleme**. Alati i jezici se mijenjaju, ali logika, algoritamsko razmišljanje i sposobnost analize ostaju temelji vaše karijere.

Sretno u daljnjem školovanju i radu!
