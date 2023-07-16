---
layout: default
parent: Solidity
grand_parent: ISBiT
nav_order: 1
---

# Varijable stanja i funkcije

U Solidityu je potrebno specificirati tip svake varijable (globalne i lokalne). Solidity pruža nekoliko elementarnih tipova koji se mogu kombinirati u složene tipove. Ovi tipovi također se nazivaju vrijednosnim tipovima jer će se varijable ovih tipova uvijek prosljeđivati po vrijednosti, tj. uvijek se kopiraju kada se dodjeljuju ili koriste kao argumenti funkcije. Tipovi mogu međusobno komunicirati u izrazima koji sadrže operatore. Reference različitih operatora možete pronaći na [Order of Precedence of Operators](https://docs.soliditylang.org/en/latest/types.html#order)

## Elementarni tipovi podataka

- `bool` - Moguće vrijednosti su konstante `true` i `false`.
- `int` / `uint` - Cijeli brojevi s predznakom i bez predznaka različitih veličina. Veličina im varira ovisno o ključnoj riječi od `uint8` do `uint256`. `uint` i `int` su aliasi za `uint256` odnosno `int256`.
- `fixed` / `ufixed` - Broj s fiksnom točkom, s predznakom i bez predznaka različitih veličina. Ključne riječi `ufixedMxN` i `fixedMxN`, gdje `M` predstavlja broj bitova koje uzima tip, a `N` predstavlja koliko je decimalnih točaka dostupno. `M` mora biti djeljiv s 8 i ide od 8 do 256 bita. `N` mora biti između 0 i 80, uključivo. `ufixed` i `fixed` su aliasi za `ufixed128x18` odnosno `fixed128x18`.
- `address` - sadrži vrijednost od 20 bajtova (veličina Ethereum adrese).
- `address payable` - ista kao i `address`, ali s dodatnim članovima `transfer` i `send`. Razlika `address payable` pd `address` je da je `address payable` adresa na koju možete poslati Ether, dok ne biste trebali slati Ether na `address`, običnu adresu, na primjer zato što bi to mogao biti pametni ugovor koji nije izgrađen za prihvaćanje Ethera. [Svi članovi address payable](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#address-related)

## Nizovi

Za razliku od elementarnih tipova možemo imati i nizove čija veličina može biti zanada, odnosno fiksna ili dinamična.  

- Nizovi s fiksno zadanom veličinom su primjerice `bytes1`, `bytes2`, `bytes3`, …, `bytes32` koji sadrže niz bajtova od jedan do 32. S članom `.length` koji daje fiksnu duljinu niza bajtova (samo za čitanje).
- Nizovi koji su zadani samo kao `bytes` ili `string` su pak niz koji je dinamičke veličine i sadržava bajtove ili UTF-8 znakove.

## Tipovi funkcija

Tipovi funkcija označeni su na sljedeći način:

```solidity
function () {internal|external|public|private
} [pure|view|payable] [returns ()]
```

- `internal` - Ovim funkcijama može se pristupiti samo interno (tj. unutar trenutnog ugovora ili ugovora koji iz njega proizlaze), bez korištenja `this`.
- `external` - Vanjske funkcije dio su sučelja ugovora, što znači da se mogu pozvati iz drugih ugovora i putem transakcija. Za interni poziv funkcije `f()` koristimo `this.f()`.
- `public` - Javne funkcije dio su sučelja ugovora i mogu se pozivati interno ili putem poruka. Za javne varijable stanja generira se funkcija `get`
- `private` - Privatne funkcije i varijable stanja vidljive su samo za ugovor u kojem su definirane, dok u izvedenim ugovorima nisu.
- `view` - Ove funkcije koriste se samo za čitanje i ne mijenjaju stanje. Drugim riječima, ako želite čitati podatke iz blockchaina, možete koristiti `view`. Getter metode su zadane kao funkcije prikaza, odnosno `view`. Ove funkcije ne mogu: ažurirati blockchain, stvarati ugovore, poslati Ether
- `pure` - Ove funkcije su +su restriktivnije od `view` funkcija  i ne mijenjaju stanje niti čitaju stanje blockchaina. Ove funkcije ne mogu: Čitati iz varijabli stanja, stanja blockchaina. Ovakve funkcije su dobre kao poziv jer nam osiguravaju da se trenutno stanje neće promjeniti.
- `payable` - Ova funkcija nam omogućuje slanje i primanje Ethera. Stvaranjem ovakve funkcije u ugovoru omogućujemo izvršavanje transakcija.

Za razliku od `<parameter types>`, `<return types>` ne mogu biti prazni - ako tip funkcije ne bi trebao vratiti ništa, `returns (<return types>)` mora biti izostavljen.

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
