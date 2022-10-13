---
layout: default
parent: ISBiT
---

# Vježbe 2:  Solidity 

- [Solidity instalacija](https://docs.soliditylang.org/en/latest/installing-solidity.html)
- [Remix IDE](https://remix-project.org/)
- [Struktura pametnog ugovora](https://docs.soliditylang.org/en/latest/structure-of-a-contract.html)
- [Tipovi varijabli](https://docs.soliditylang.org/en/latest/types.html)
- [Vidljivost](https://docs.soliditylang.org/en/latest/contracts.html#visibility-and-getters)


## Primjer pametnog ugovora

Ugovor u smislu Solidityja je zbirka koda (njegove funkcije) i podataka (njegovo stanje) koji se nalaze na određenoj adresi na Ethereum blockchainu.

U ovom primjeru, ugovor definira funkcije `set` i `get` koje se mogu koristiti za izmjenu ili dohvaćanje vrijednosti varijable. Ovaj ugovor još ne čini mnogo osim dopuštanja bilo kome da pohrani jedan broj kojem može pristupiti bilo tko. Svatko može ponovno pozvati `set` s drugom vrijednošću i prebrisati vaš broj, ali broj je i dalje pohranjen u povijesti blockchaina. 

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

contract SimpleStorage {
    uint storedData;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}
```

- `// SPDX-License-Identifier: GPL-3.0` - Izvorni kod licenciran pod GPL verzijom 3.0. Strojno čitljivi specifikatori licence važni su u postavkama u kojima je objavljivanje izvornog koda zadano.
- `pragma solidity >=0.4.16 <0.9.0;` - Navodi da je izvorni kod napisan za Solidity verziju 0.4.16 ili noviju verziju jezika do, ali ne uključujući verziju 0.9.0. Ovo je kako bi se osiguralo da se ugovor ne može kompajlirati s novom (pokvarenom) verzijom prevoditelja, gdje bi se mogao ponašati drugačije.
- `uint storedData;` - Deklarira varijablu stanja pod nazivom `storedData` tipa `uint` (cijeli broj od 256 bita). 

## Zadatak 1: Omiljeni broj
Stvorite novi file `SimpleStorage.sol` u kojem ćete napisati vaš ugovor. Cilj vašeg ugovora je omogućiti unos i ispis omiljenog broja. Stvorite varijablu `favNum` u koju pohranjujete omiljeni broj, za pohranu kreirajte funkciju `store`, a za dohvaćanje vrijednosti kreirajte funkciju `retrieve`. 

## Izvori
- [Metamask](https://metamask.io/)
- [Etherscan](https://etherscan.io/)
- [Goerli Etherscan](https://goerli.etherscan.io/)
- [Rinkeby Etherscan](https://rinkeby.etherscan.io/)
- [Kovan Etherscan](https://kovan.etherscan.io/)
- [Goerli Faucet](https://faucets.chain.link/goerli)
  - NOTE: You can always find the most up to date faucets at [faucets.chain.link](https://faucets.chain.link/).
- OR, use the [Kovan ETH Faucet](https://faucets.chain.link/), just be sure to swap your metamask to kovan!
- [Gas and Gas Fees](https://ethereum.org/en/developers/docs/gas/)
- [Wei, Gwei, and Ether Converter](https://eth-converter.com/)
- [ETH Gas Station](https://ethgasstation.info/)
- [Run Your Own Ethereum Node](https://geth.ethereum.org/docs/getting-started)
