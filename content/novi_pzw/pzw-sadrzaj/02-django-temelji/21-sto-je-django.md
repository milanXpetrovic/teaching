---
parent: 'Django Temelji: Od Projekta do Prve Aplikacije'
nav_order: 1
title: '2.1 Što je Django? MVT/MTV Arhitektura'
---

# 2.1 Što je Django? MVT/MTV Arhitektura

Dobrodošli u svijet Djanga! Django je besplatan, open-source i visoko-razinski Python web framework koji potiče brzi razvoj i čist, pragmatičan dizajn. Njegov glavni moto je:

> **"Web framework za perfekcioniste s rokovima."**

To znači da je Django dizajniran da vam pomogne izraditi web aplikacije što je brže i efikasnije moguće, bez žrtvovanja kvalitete, sigurnosti i skalabilnosti.

## Filozofija "Baterije Uključene" (Batteries-Included)

Jedna od ključnih karakteristika Djanga je njegova "batteries-included" filozofija. Za razliku od nekih drugih, minimalističkih frameworka gdje morate sami birati i spajati različite biblioteke za osnovne zadatke, Django dolazi s ogromnim setom ugrađenih alata za rješavanje uobičajenih web-razvojnih problema.

To uključuje:
* **ORM (Object-Relational Mapper):** Moćan alat za interakciju s bazom podataka koristeći Python kod umjesto SQL-a.
* **Admin sučelje:** Automatski generirano administratorsko sučelje za upravljanje podacima vaše aplikacije.
* **Sustav autentikacije:** Ugrađena podrška za upravljanje korisnicima, grupama i dozvolama.
* **Forme:** Sustav za obradu i validaciju korisničkog unosa.
* **Routing:** Elegantan sustav za mapiranje URL-ova na vaš kod.
* **Sigurnost:** Ugrađena zaštita od čestih sigurnosnih prijetnji kao što su CSRF, XSS i SQL injection.

## MVT Arhitektura: Model, View, Template

Kako Django postiže organizaciju i brzinu razvoja? Kroz arhitektonski uzorak koji se zove **Model-View-Template (MVT)**.

MVT je Djangova interpretacija poznatijeg **Model-View-Controller (MVC)** uzorka. Cilj je isti: **odvojiti brige** (eng. *separation of concerns*). To znači da se kod koji se bavi podacima (logika) odvaja od koda koji se bavi prikazom (prezentacija).

Pogledajmo svaku komponentu:

###  Model (M) – Podaci

* **Što je?** Model je jedini, definitivni izvor istine o vašim podacima. On predstavlja strukturu podataka vaše aplikacije.
* **Uloga:** Definira od čega se podaci sastoje (polja) i kako se ponašaju (metode). Svaki model se mapira na jednu tablicu u bazi podataka.
* **Primjer:** U blog aplikaciji, imali biste `Post` model koji definira da svaki post ima naslov, sadržaj, autora i datum objave.

### View (V) – Logika

* **Što je?** View (pogled) je mjesto gdje se nalazi poslovna logika aplikacije. On posreduje između Modela i Templatea.
* **Uloga:** Prima HTTP zahtjev od korisnika, dohvaća ili mijenja podatke iz baze putem Modela, a zatim vraća HTTP odgovor, najčešće prosljeđujući podatke Templateu da ih prikaže.
* **Važna napomena:** Djangov "View" je zapravo bliži onome što se u klasičnom MVC uzorku naziva **Controller**.

### Template (T) – Prezentacija

* **Što je?** Template je datoteka (obično HTML) koja definira strukturu i izgled onoga što će korisnik vidjeti.
* **Uloga:** Sadrži statički dio prikaza, kao i posebne oznake (tagove) koje služe kao placeholderi za dinamičke podatke koje je pripremio View. Django Template Language (DTL) omogućuje jednostavnu logiku prikaza poput petlji i uvjeta.
* **Filozofija:** U templateima bi trebalo biti što je manje moguće programske logike. Njihova svrha je prikazati podatke, a ne obrađivati ih.

## Kako sve funkcionira zajedno: Tijek jednog zahtjeva

Zamislimo da korisnik posjeti URL `.../posts/5/` na našem blogu.

1. **Zahtjev:** Korisnikov preglednik šalje HTTP GET zahtjev serveru.
2. **URL Router:** Django prvo provjerava `urls.py` datoteke kako bi vidio koji **View** je zadužen za tu URL putanju.
3. **View:** Django poziva odgovarajući View. View shvaća da korisnik traži post s ID-om 5.
4. **Model:** View komunicira s **Modelom** (`Post` modelom) i traži: "Daj mi post čiji je ID jednak 5". Model to pretvara u SQL upit, dohvaća podatke iz baze i vraća ih Viewu kao Python objekt.
5. **Template:** View zatim uzima taj `Post` objekt i prosljeđuje ga **Templateu** (`post_detail.html`). Kaže mu: "Renderiraj se koristeći ove podatke".
6. **Odgovor:** Template popunjava svoje placeholdere s podacima iz `Post` objekta (naslov, sadržaj, itd.) i generira konačni HTML. Django taj HTML zapakira u HTTP odgovor i šalje ga natrag korisnikovom pregledniku.


Ova jasna podjela odgovornosti čini Django projekte organiziranima, lakšima za održavanje i bržima za razvoj. Sada kada razumijemo teoriju, spremni smo stvoriti naš prvi Django projekt.