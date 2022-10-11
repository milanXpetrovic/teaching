---
layout: default
parent: ISBiT
---

# Vježbe 1: Blockchain
## Blockchain
Blockchain je distribuirana baza podataka ili registrator (*eng. ledger*) koja se dijeli među čvorovima u mreži. Podaci su pohranjeni u blokove koji se zatim međusobno povezuju. Kako dolaze novi podaci, oni se unose u novi blok. Nakon što se blok ispuni podacima, on se lančano povezuje s prethodnim blokom, što čini podatke lančano povezanim kronološkim redoslijedom. Različite vrste informacija mogu se pohraniti na blockchain. Unos podataka je nepovratan, jednom pohranjeni podaci ne mogu se više izmijeniti. Inovacija s blockchainom je u tome što jamči vjernost i sigurnost zapisa podataka i stvara povjerenje bez potrebe za trećom stranom. Najpoznatiji primjena blockchaina je u sustavima kriptovaluta za održavanje sigurne i decentralizirane evidencije transakcija. Primjerice u Bitcoin mreži to znači da se transakcije trajno bilježe i da ih svatko može vidjeti.

### Blok
Blok je osnovna jedinica unutar blockchaina gdje su pohranjene kriptirane informacije s mreže. Jedinica podataka pohranjena unutar bloka može biti predstavljena bilo kojom vrijednošću ovisno o vrsti blockchaina. Blok može pohraniti iznos novca, udio u tvrtki, digitalnu potvrdu o vlasništvu, glas tijekom izbora ili bilo koju drugu vrijednost. Blok pohranjuje šifrirane detalje o stranama čija je interakcija rezultirala podacima pohranjenima u bloku. U slučaju kriptovaluta blok također sadrži kriptirane identifikatore pošiljatelja i primatelja. 

<img src="https://rubygarage.s3.amazonaws.com/uploads/article_image/file/1078/hash-example.png" width="350">

Svaki blok također ima hash koji ima ulogu identificirati blok i sadržaj bloka. Ova hash vrijednost je generirana pomoću matematičke funkcije iz sadržaja upisanog na blok. Hash se može usporediti s otiskom prsta jer je svaki hash jedinstven, svaka promjena podataka upisanih na blok uzrokovala bi i promjenu hash vrijednosti.

<img src="https://rubygarage.s3.amazonaws.com/uploads/article_image/file/1080/changes-in-block.png" width="350">

### Konsenzus u mreži
Konsenzus je metoda za postizanje dogovora oko zajedničkog stanja. Kako bi blockchain nastavio graditi, svi čvorovi u mreži moraju se složiti i doći do konsenzusa. To je način na koji čvorovi u decentraliziranoj mreži mogu ostati međusobno sinkronizirani. Bez konsenzusa za decentraliziranu mrežu čvorova u blockchainu, ne postoji način da se osigura da će stanje za koje jedan čvor vjeruje da je istinito dijeliti drugi čvorovi. Konsenzus ima za cilj pružiti objektivan pogled na stanje između sudionika od kojih svaki ima svoje subjektivne poglede na mrežu. To je proces kojim čvorovi komuniciraju i postižu dogovaraju te mogu graditi nove blokove.

<figure>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Byzantine_Generals.png/435px-Byzantine_Generals.png" width="350">
<figcaption>Prikaz konsenzusa u mreži iz Problema bizantskih generala.</figcaption>
</figure>

### Kako funkcionira Blockchain?
[Blockchain Demo](https://andersbrownworth.com/blockchain/blockchain)

<img src="https://rubygarage.s3.amazonaws.com/uploads/article_image/file/1082/blockchain-dice-game.png" width="350">


### Whitepaper
Whitepaper promovira određeni proizvod, uslugu ili metodologiju kako bi se utjecalo na trenutne i potencijalne odluke kupaca ili ulagača. On pruža činjenične dokaze da je određen proizvod/metoda bolja u rješavanju određenog problema. Whitepaper je obično dizajniran za marketinške svrhe, odnosno cilj mu je "prodati" određeno rješenje za neki problem.
- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)







### Ethereum
- [What are Smart Contracts?](https://www.investopedia.com/terms/s/smart-contracts.asp)
- [Hybrid Smart Contracts](https://blog.chain.link/hybrid-smart-contracts-explained/)
- [Blockchain Oracles](https://betterprogramming.pub/what-is-a-blockchain-oracle-f5ccab8dbd72?source=friends_link&sk=d921a38466df8a9176ed8dd767d8c77d)
## Transakcije
- [Metamask](https://metamask.io/)
- [Etherscan](https://etherscan.io/)
- [Goerli Etherscan](https://goerli.etherscan.io/)
- [Rinkeby Etherscan](https://rinkeby.etherscan.io/)
- [Kovan Etherscan](https://kovan.etherscan.io/)
- [Goerli Faucet](https://faucets.chain.link/goerli)
- Rinkeby Faucet (Check the [link token contracts page](https://docs.chain.link/docs/link-token-contracts/#rinkeby))
  - NOTE: You can always find the most up to date faucets at [faucets.chain.link](https://faucets.chain.link/).
- OR, use the [Kovan ETH Faucet](https://faucets.chain.link/), just be sure to swap your metamask to kovan!
- [Gas and Gas Fees](https://ethereum.org/en/developers/docs/gas/)
- [Wei, Gwei, and Ether Converter](https://eth-converter.com/)
- [ETH Gas Station](https://ethgasstation.info/)
- [Run Your Own Ethereum Node](https://geth.ethereum.org/docs/getting-started)

### Consensus
- [Consensus](https://wiki.polkadot.network/docs/learn-consensus)
- [Proof of Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/)
- [Proof of Work](https://ethereum.org/en/developers/docs/consensus-mechanisms/pow/)
- [Nakamoto Consensus](https://blockonomi.com/nakamoto-consensus/)
## The Future
- [Ethereum 2](https://ethereum.org/en/eth2/)
## Miscellaneous 
- [DAOs](https://www.investopedia.com/tech/what-dao/)



## Izvori
- https://www.investopedia.com/terms/b/blockchain.asp
- https://rubygarage.org/blog/how-blockchain-works
- https://www.investopedia.com/terms/b/block-bitcoin-block.asp
- https://en.wikipedia.org/wiki/Blockchain
- https://en.wikipedia.org/wiki/Proof_of_work
- https://en.wikipedia.org/wiki/Proof_of_stake
- https://blockgeeks.com/guides/blockchain-consensus/
- https://wiki.polkadot.network/docs/learn-consensus
- https://en.wikipedia.org/wiki/Byzantine_fault
- https://ethereum.org/en/developers/docs/