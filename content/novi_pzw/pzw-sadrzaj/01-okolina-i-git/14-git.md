---
parent: Razvojna Okolina i Git
nav_order: 4
title: 1.4 Kontrola Verzija s Gitom
---

# 1.4 Kontrola Verzija s Gitom

Sada kada znamo kako postaviti izolirano okruženje za naš projekt, vrijeme je da naučimo kako pratiti povijest promjena u našem kodu. Za to koristimo sustav za kontrolu verzija (eng. *Version Control System*), a apsolutni industrijski standard je **Git**.

## Što je kontrola verzija i zašto je Git važan?

Zamislite da pišete važan dokument. Spremite ga kao `projekt_v1.docx`. Zatim napravite izmjene i spremite ga kao `projekt_v2.docx`, pa `projekt_final.docx`, i na kraju `projekt_stvarno_final_ovajput.docx`. To je neorganizirano, zbunjujuće i dugoročno neodrživo.

Kontrola verzija rješava taj problem na strukturiran i profesionalan način. Omogućuje vam da:

* **Spremate "snimke" (eng. *snapshots*) stanja vašeg koda** u određenom trenutku. Te snimke se zovu **commitovi**.
* **Pratite povijest promjena:** Tko je, što i kada promijenio.
* **Vratite se na stariju verziju koda** ako nešto pođe po zlu.
* **Radite na različitim funkcionalnostima paralelno** koristeći grane (eng. *branches*), bez da ometate glavni, stabilni kod.
* **Jednostavno surađujete s drugim developerima** na istom projektu.

**Git** je alat koji sve to radi na vašem računalu. **GitHub** (ili GitLab, Bitbucket) je web servis koji služi kao centralno mjesto za pohranu vaših Git repozitorija ("skladišta" koda) na internetu, omogućavajući sigurnosne kopije i suradnju.

## Osnovni Git tijek rada (Workflow)

Za početak, fokusirat ćemo se na najosnovniji tijek rada koji ćete koristiti 90% vremena. On se sastoji od tri logička koraka.

### Korak 1: Inicijalizacija repozitorija (`git init`)

Prvo, moramo reći Gitu da počne pratiti promjene u našem projektnom direktoriju.

1. Otvorite terminal i navigirajte do korijena vašeg projekta (npr. `cd moj-django-projekt`).
2. Pokrenite naredbu:
    ```bash
    git init
    ```
    Ova naredba stvara skriveni poddirektorij `.git` unutar vašeg projekta. U tom direktoriju Git pohranjuje svu povijest i konfiguraciju vašeg repozitorija. Time je vaš projekt postao lokalni **Git repozitorij**.

### Korak 2: Dodavanje promjena u "staging area" (`git add`)

Git ne sprema automatski svaku promjenu. Vi mu morate eksplicitno reći koje promjene želite uključiti u sljedeću "snimku" (commit). To radite dodavanjem datoteka u privremeno područje koje se zove **staging area**.

* Nakon što ste napravili neke promjene (npr. stvorili novu datoteku `README.md`), možete provjeriti status repozitorija:
    ```bash
    git status
    ```
    Git će vam pokazati koje datoteke su izmijenjene, a koje su nove i još se ne prate (nalaze se u *radnom direktoriju*, ali ne u *staging area*).

* Da biste dodali specifičnu datoteku u *staging area*:
    ```bash
    git add README.md
    ```

* Da biste dodali **sve** promijenjene i nove datoteke iz trenutnog direktorija i poddirektorija:
    ```bash
    git add .
    ```

### Korak 3: Spremanje promjena (`git commit`)

Kada ste zadovoljni s promjenama koje ste pripremili u *staging area*, vrijeme je da ih trajno spremite kao **commit**. Svaki commit mora imati opisnu poruku koja objašnjava što je napravljeno.

```bash
git commit -m "Dodao početnu README.md datoteku"
```

* `git commit` je naredba za spremanje.
* `-m` je zastavica (eng. *flag*) koja označava da slijedi poruka (eng. *message*).
* Tekst unutar navodnika je vaša **commit poruka**.

> **Two Scoops Savjet:** Pišite jasne i sažete commit poruke! Dobra poruka opisuje *što* je promijenjeno i *zašto*. Primjer: "Feat: Dodana autorizacija za uređivanje profila" je mnogo bolja poruka od "neke izmjene".

---

## Rad s udaljenim repozitorijima (npr. GitHub)

Sada kada imate povijest spremljenu lokalno, želite je pohraniti na sigurno mjesto online i eventualno podijeliti s drugima.

1. **Kreiranje repozitorija na GitHubu:**
    * Prijavite se na svoj GitHub račun.
    * Kliknite na "New" za stvaranje novog repozitorija.
    * Dajte mu ime (npr. `moj-django-projekt`), odaberite je li javan (*public*) ili privatan (*private*) i **nemojte** ga inicijalizirati s `README` ili `.gitignore` datotekom, jer to već imamo lokalno.

2. **Povezivanje lokalnog i udaljenog repozitorija (`git remote`):**
    * GitHub će vam dati URL vašeg novog repozitorija (npr. `https://github.com/vase-ime/moj-django-projekt.git`).
    * U vašem lokalnom terminalu, pokrenite naredbu da povežete ta dva repozitorija:

      ```bash
      git remote add origin https://github.com/vase-ime/moj-django-projekt.git
      ```
      `origin` je standardno, konvencionalno ime za vaš glavni udaljeni repozitorij.

3. **Slanje (Push) promjena na GitHub (`git push`):**
    * Sada kada su povezani, možete poslati svoje lokalne commitove na GitHub:
      
      ```bash
      git push -u origin main
      ```
      * `git push` je naredba za slanje.
      * `origin` je ime udaljenog repozitorija.
      * `main` je ime glavne grane (eng. *branch*) na koju šaljete.
      * `-u` (ili `--set-upstream`) postavlja `origin main` kao zadanu lokaciju za buduće `push` i `pull` naredbe, tako da sljedeći put možete pisati samo `git push`.

## Neizostavna `.gitignore` datoteka

U vašem projektu će postojati datoteke koje **nikada ne želite** pratiti s Gitom i slati na GitHub. To su:
* Virtualno okruženje (`venv/`)
* Lokalna baza podataka (`db.sqlite3`)
* Python cache datoteke (`__pycache__/`)
* Osjetljivi podaci i tajni ključevi (`.env`)

Stvorite datoteku naziva `.gitignore` u korijenu projekta i u nju upišite imena datoteka i direktorija koje Git treba ignorirati.

**Primjer `.gitignore` za Django projekt:**

```bash
# Virtualno okruženje
venv/

# Baza podataka
db.sqlite3

# Python cache
__pycache__/
*.pyc

# Osjetljivi podaci
.env
```

Git je moćan alat s mnogo mogućnosti, ali ovaj osnovni tijek rada (`git add`, `git commit`, `git push`) je temelj koji ćete koristiti svakodnevno. Savladavanje ovih naredbi je prvi korak prema organiziranom i profesionalnom razvoju softvera.

