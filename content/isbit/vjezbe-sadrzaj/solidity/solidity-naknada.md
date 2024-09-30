---
layout: default
parent: Solidity
grand_parent: ISBiT
nav_exclude: true
nav_order: 6
---

# Plaćanje naknade

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

