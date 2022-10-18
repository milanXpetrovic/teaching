---
layout: default
parent: ISBiT
---

# Solidity 

- [Solidity instalacija](https://docs.soliditylang.org/en/latest/installing-solidity.html)
- [Remix IDE](https://remix-project.org/)
- [Struktura pametnog ugovora](https://docs.soliditylang.org/en/latest/structure-of-a-contract.html)
- [Tipovi varijabli](https://docs.soliditylang.org/en/latest/types.html)
- [Vidljivost](https://docs.soliditylang.org/en/latest/contracts.html#visibility-and-getters)


## Jednostavni tipovi podataka
U Solidityu je potrebno specificirati tip svake varijable (globalne i lokalne). Solidity pruža nekoliko elementarnih tipova koji se mogu kombinirati u složene tipove. Ovi tipovi također se nazivaju vrijednosnim tipovima jer će se varijable ovih tipova uvijek prosljeđivati po vrijednosti, tj. uvijek se kopiraju kada se dodjeljuju ili koriste kao argumenti funkcije. Tipovi mogu međusobno komunicirati u izrazima koji sadrže operatore. Reference različitih operatora možete pronaći na [Order of Precedence of Operators](https://docs.soliditylang.org/en/latest/types.html#order)

Elementarni tipovi podataka: 
- `bool` - Moguće vrijednosti su konstante `true` i `false`.
- `int` / `uint` - Cijeli brojevi s predznakom i bez predznaka različitih veličina. Veličina im varira ovisno o ključnoj riječi od `uint8` do `uint256`. `uint` i `int` su aliasi za `uint256` odnosno `int256`.
- `fixed` / `ufixed` - Broj s fiksnom točkom, s predznakom i bez predznaka različitih veličina. Ključne riječi `ufixedMxN` i `fixedMxN`, gdje `M` predstavlja broj bitova koje uzima tip, a `N` predstavlja koliko je decimalnih točaka dostupno. `M` mora biti djeljiv s 8 i ide od 8 do 256 bita. `N` mora biti između 0 i 80, uključivo. `ufixed` i `fixed` su aliasi za `ufixed128x18` odnosno `fixed128x18`.
- `address` - sadrži vrijednost od 20 bajtova (veličina Ethereum adrese).
- `address payable` - ista kao i `address`, ali s dodatnim članovima `transfer` i `send`. Razlika `address payable` pd `address` je da je `address payable` adresa na koju možete poslati Ether, dok ne biste trebali slati Ether na `address`, običnu adresu, na primjer zato što bi to mogao biti pametni ugovor koji nije izgrađen za prihvaćanje Ethera. [Svi članovi address payable](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#address-related)

Za razliku od elementarnih tipova možemo imati i nizove čija veličina može biti zanada, odnosno fiksna ili dinamična.  
- Nizovi sa fiksno zadanom veličinom su primjerice `bytes1`, `bytes2`, `bytes3`, …, `bytes32` koji sadrže niz bajtova od jedan do 32. S članom `.length` koji daje fiksnu duljinu niza bajtova (samo za čitanje).
- Nizovi koji su zadani samo kao `bytes` ili `string` su pak niz koji je dinamičke veličine i sadržava bajtove ili UTF-8 znakove.


Tipovi funkcija označeni su na sljedeći način:
```solidity
function (<parameter types>) {internal|external} [pure|view|payable] [returns (<return types>)]
```

- `internal`
- `external`

- `pure`
- `view`
- `payable`

Za razliku od `<parameter types>`, `<return types>` ne mogu biti prazni - ako tip funkcije ne bi trebao vratiti ništa, `returns (<return types>)` mora biti izostavljen.




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






```solidity

```






## Zadatak 1: Omiljeni broj
Stvorite novi file `SimpleStorage.sol` u kojem ćete napisati vaš ugovor. Cilj vašeg ugovora je omogućiti unos i ispis omiljenog broja. Stvorite varijablu `favNum` u koju pohranjujete omiljeni broj, za pohranu kreirajte funkciju `store`, a za dohvaćanje vrijednosti kreirajte funkciju `retrieve`. 









## Zadatak 2:







## Zadatak 3: 



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
