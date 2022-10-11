---
layout: default
parent: ISBiT
---

# Vježbe 1: Blockchain

## Web3
Web2 se odnosi na verziju interneta koju većina nas danas poznaje. Internet kojim dominiraju tvrtke koje pružaju usluge u zamjenu za vaše osobne podatke. Web3, u kontekstu Ethereuma, odnosi se na decentralizirane aplikacije koje rade na blockchainu. To su aplikacije koje svakome omogućuju sudjelovanje bez unovčavanja osobnih podataka

Prednosti:
- Bilo koji sudionik mreže ne treba dopuštenje za korištenje usluge
- Nitko vas ne može blokirati ili uskratiti pristup usluzi. 
- Primjerice Ethereum je turing-complete, što znači da možete programirati gotovo sve.

Nedostaci:
- Skalabilnost – transakcije su sporije na web3 jer su decentralizirane. Promjene stanja, poput plaćanja, treba obraditi čvor i propagirati kroz mrežu.
- UX – interakcija s web3 aplikacijama može zahtijevati dodatne korake, softver i edukaciju o korištenju. 
- Pristupačnost – nedostatak integracije u moderne web preglednike čini web3 manje dostupnim većini korisnika.

## Blockchain
Blockchain je distribuirana baza podataka ili registrator (*eng. ledger*) koja se dijeli među čvorovima u mreži. Podaci su pohranjeni u blokove koji se zatim međusobno povezuju. Kako dolaze novi podaci, oni se unose u novi blok. Nakon što se blok ispuni podacima, on se lančano povezuje s prethodnim blokom, što čini podatke lančano povezanim kronološkim redoslijedom. Različite vrste informacija mogu se pohraniti na blockchain. Unos podataka je nepovratan, jednom pohranjeni podaci ne mogu se više izmijeniti. Inovacija s blockchainom je u tome što jamči vjernost i sigurnost zapisa podataka i stvara povjerenje bez potrebe za trećom stranom. Najpoznatiji primjena blockchaina je u sustavima kriptovaluta za održavanje sigurne i decentralizirane evidencije transakcija. Primjerice u Bitcoin mreži to znači da se transakcije trajno bilježe i da ih svatko može vidjeti.

[Blockchain Demo](https://andersbrownworth.com/blockchain/blockchain)

### Blok
Blok je osnovna jedinica unutar blockchaina gdje su pohranjene kriptirane informacije s mreže. Jedinica podataka pohranjena unutar bloka može biti predstavljena bilo kojom vrijednošću ovisno o vrsti blockchaina. Blok može pohraniti iznos novca, udio u tvrtki, digitalnu potvrdu o vlasništvu, glas tijekom izbora ili bilo koju drugu vrijednost. Blok pohranjuje šifrirane detalje o stranama čija je interakcija rezultirala podacima pohranjenima u bloku. U slučaju kriptovaluta blok također sadrži kriptirane identifikatore pošiljatelja i primatelja. 

<img src="https://rubygarage.s3.amazonaws.com/uploads/article_image/file/1078/hash-example.png" width="400">

Svaki blok također ima hash koji ima ulogu identificirati blok i sadržaj bloka. Ova hash vrijednost je generirana pomoću matematičke funkcije iz sadržaja upisanog na blok. Hash se može usporediti s otiskom prsta jer je svaki hash jedinstven, svaka promjena podataka upisanih na blok uzrokovala bi i promjenu hash vrijednosti.

<img src="https://rubygarage.s3.amazonaws.com/uploads/article_image/file/1080/changes-in-block.png" width="400">

### Konsenzus u mreži
Konsenzus je metoda za postizanje dogovora oko zajedničkog stanja. Kako bi blockchain nastavio graditi, svi čvorovi u mreži moraju se složiti i doći do konsenzusa. To je način na koji čvorovi u decentraliziranoj mreži mogu ostati međusobno sinkronizirani. Bez konsenzusa za decentraliziranu mrežu čvorova u blockchainu, ne postoji način da se osigura da će stanje za koje jedan čvor vjeruje da je istinito dijeliti drugi čvorovi. Konsenzus ima za cilj pružiti objektivan pogled na stanje između sudionika od kojih svaki ima svoje subjektivne poglede na mrežu. To je proces kojim čvorovi komuniciraju i postižu dogovaraju te mogu graditi nove blokove.

<figure>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Byzantine_Generals.png/435px-Byzantine_Generals.png" width="400">
<figcaption>Prikaz konsenzusa u mreži iz Problema bizantskih generala.</figcaption>
</figure>

### Transakcije
Da bi razumjeli kako funkcioniraju transakcije prvo je potrebno navesti tko su sudionici u blockchain mreži: 
- Korisnici - to je bilo koji korisnik mehanike blockchaina za obavljanje transakcija.

- Rudari - Omogućuju korisnicima da njihova transakcija bude ispravno poštovana bez središnjeg tijela koje to nadzire. Rudari omogućuju ispravnost transakcija provjerom dolaznih transakcijskih blokova da budu potvrđeni. Ako rudari ispravno rade, ostvaruju nagradu, što je poticaj koji održava sustav u radu.

- Čvorovi - Svaki korisnik u mreži može biti čvor. Čvorovi održavaju cijeli sustav sigurnim i osiguranim potvrđivanjem transakcijskih blokova koje šalju rudari prije nego što se dodaju u blockchain. To čine provjerom dolaznih informacija s poviješću transakcija blockchaina, i osiguravaju da se sve podudara. Čvorovi mreže mogu se nalaziti bilo gdje, bitno je da su povezani s ostatkom mreže. Oni zatim kolektivno postižu konsenzus da su nove transakcije valjane, prije nego što ih dodaju u blockchain.

Proces transakcije može se podijeliti u šest koraka:

1. Netko zahtijeva transakciju. Transakcija može uključivati ​​kriptovalute, ugovore, zapise ili druge informacije.
2. Transakcija se emitira svim čvorovima koja sudjeluju u blockchain mreži. Sve transakcije objavljuju se u Mem-poolu ili memorijskom skupu, gdje se smatraju "na čekanju". Naknade plaćaju korisnici kao dio transakcije kako bi se nadoknadila računalna energija potrebna za obradu i provjeru valjanosti transakcija na blockchainu.
3. Rudari provjeravaju transakciju. Svako računalo u mreži provjerava transakciju prema nekim pravilima provjere valjanosti koja su postavili tvorci određene blockchain mreže.
4. Validirane transakcije pohranjuju se u blok i zapečaćene su bravom koja se naziva Hash.
5. Novi blok se dodaje postojećem lancu blokova. Ovaj blok postaje dio blockchaina kada druga računala u mreži potvrde je li zaključavanje bloka ispravno.
6. Transakcija je završena. Sada je transakcija dio blockchaina i ne može se ni na koji način mijenjati.

### Whitepaper
Whitepaper promovira određeni proizvod, uslugu ili metodologiju kako bi se utjecalo na trenutne i potencijalne odluke kupaca ili ulagača. On pruža činjenične dokaze da je određen proizvod/metoda bolja u rješavanju određenog problema. Whitepaper je obično dizajniran za marketinške svrhe, odnosno cilj mu je "prodati" određeno rješenje za neki problem.
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)

## Ethereum
Ethereum je blockchain s računalom ugrađenim u njega. To je temelj za izgradnju aplikacija i organizacija na decentraliziran način, bez dopuštenja i otporan na cenzuru.

U Ethereum svemiru postoji jedno, kanonsko računalo (zvano Ethereum Virtual Machine ili EVM) s čijim se stanjem svi na Ethereum mreži slažu. Svatko tko sudjeluje u Ethereum mreži (svaki Ethereum čvor) čuva kopiju stanja ovog računala. Dodatno, bilo koji sudionik može emitirati zahtjev za ovo računalo da izvrši proizvoljno izračunavanje. Kad god se takav zahtjev emitira, drugi sudionici na mreži provjeravaju, potvrđuju i provode ("izvršavaju") izračun. Ovo izvršenje uzrokuje promjenu stanja u EVM-u, koja se predaje i širi kroz cijelu mrežu.

Zahtjevi za izračun nazivaju se zahtjevi za transakcije. Evidencija svih transakcija i trenutno stanje EVM-a pohranjuju se na blockchain.

Kriptografski mehanizmi osiguravaju da nakon što se transakcije potvrde kao valjane, dodaju u blockchain. Isti mehanizmi također osiguravaju da su sve transakcije potpisane i izvršene s odgovarajućim "dopuštenjima" (nitko ne bi trebao moći slati digitalna sredstva s Aliceina računa, osim same Alice).

### Ether
Ether (ETH) je izvorna kriptovaluta Ethereuma. Svrha ETH-a je omogućiti tržište za računanje. Takvo tržište pruža ekonomski poticaj za sudionike da verificiraju i izvršavaju zahtjeve za transakcije i daju računalne resurse mreži. Svaki sudionik koji emitira zahtjev za transakciju također mora ponuditi određenu količinu ETH mreži kao nagradu. Mreža će ovu nagradu dodijeliti onome tko na kraju izvrši posao provjere transakcije, izvrši je, obvezuje je na blockchain i emitira je mreži. Plaćeni iznos ETH odgovara vremenu potrebnom za izračun. Ove nagrade također sprječavaju zlonamjerne sudionike da namjerno uspore mrežu tražeći izvršavanje beskonačnog računanja ili drugih skripti koje zahtijevaju velike resurse, budući da ti sudionici moraju platiti vrijeme računanja. 

### Pametni ugovori
Programe koji su postavljeni na mrežu i koje ona izvršava nazivamo pametnim ugovorima. U praksi, korisnici ne pišu novi programski kod svaki put kada žele zatražiti izračun na EVM-u. Umjesto toga, programeri postavljaju programe u EVM, a korisnici podnose zahtjeve za izvršavanje tih isječaka koda s različitim parametrima. 

Na vrlo osnovnoj razini, pametni ugovor možete zamisliti kao neku vrstu automata za prodaju. Skripta koja, kada se pozove s određenim parametrima, izvodi neke radnje ili računanje ako su zadovoljeni određeni uvjeti.

Svaki programer može stvoriti pametni ugovor i učiniti ga javnim na mreži, koristeći blockchain kao svoj podatkovni sloj, uz naknadu plaćenu mreži. Svaki korisnik tada može pozvati pametni ugovor da izvrši svoj kod, opet uz naknadu plaćenu mreži. S pametnim ugovorima, programeri mogu izgraditi i implementirati proizvoljno složene aplikacije i usluge okrenute korisniku. 

## Izvori
- https://www.investopedia.com/terms/b/blockchain.asp
- https://ethereum.org/en/developers/docs/web2-vs-web3/
- https://rubygarage.org/blog/how-blockchain-works
- https://www.investopedia.com/terms/b/block-bitcoin-block.asp
- https://en.wikipedia.org/wiki/Blockchain
- https://en.wikipedia.org/wiki/Proof_of_work
- https://ethereum.org/en/developers/docs/consensus-mechanisms/pow/
- https://en.wikipedia.org/wiki/Proof_of_stake
- https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/
- https://blockgeeks.com/guides/blockchain-consensus/
- https://wiki.polkadot.network/docs/learn-consensus
- https://en.wikipedia.org/wiki/Byzantine_fault
- https://ethereum.org/en/developers/docs/
- https://www.ledger.com/academy/how-does-a-blockchain-transaction-work
- https://www.investopedia.com/terms/s/smart-contracts.asp
- https://101blockchains.com/smart-contracts/
