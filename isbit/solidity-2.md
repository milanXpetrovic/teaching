---
layout: default
parent: ISBiT
nav_exclude: true
---

# Solitdity 2

## Ether i Wei

Transakcije se plaćaju `eterom`.

Slično kao što je jedan euro jednak 100 centi, jedan `ether` je jednak $10^18$ `wei`, (1 eht = $10^18$ wei).

```solidity
// SPDX-License-Identifier: MIT
pragma solidity <0.8.13;

contract EtherUnits {
    uint public oneWei = 1 wei;
    // 1 wei is equal to 1
    bool public isOneWei = 1 wei == 1;

    uint public oneEther = 1 ether;
    // 1 ether is equal to 10^18 wei
    bool public isOneEther = 1 ether == 1e18;
}
```

## Naknada

Prilikom transakcije potrebno je odraditi određenu količinu računanja. Količina računanja izražena je u jedinicama koje se nazivaju `Gas`. Sukladno tome trošak transakcije biti će određen količinom potrošenih `Gas` jedinica i njihovoj cijeni.

`Cijena transakcije = potrošena količina Gas * cijena Gas`

Cijena transakcije izražena je i plaća se u Etherima. Transakcije s višom cijenom Gas-a imaju veći prioritet za uključivanje u blok. Sav Gas koji nije potrošen biti će vraćen.

### Gas limit

Postoje dvije gornje granice količine Gas-a koje možete potrošiti.

- `gas limit` - maksimalna količina koju ste voljni koristiti za svoju transakciju, koju ste vi postavili.
- `block gas limit` - maksimalna količina dopuštena u bloku, postavljena od strane mreže.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity <0.8.13;

contract Gas {
    uint public i = 0;

    // Using up all of the gas that you send causes your transaction to fail.
    // State changes are undone.
    // Gas spent are not refunded.
    function forever() public {
        // Here we run a loop until all of the gas are spent
        // and the transaction fails
        while (true) {
            i += 1;
        }
    }
}
```

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

## Ethereum Improvement Proposals (EIPs)

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards. Network upgrades are discussed separately in the Ethereum Project Management repository.
