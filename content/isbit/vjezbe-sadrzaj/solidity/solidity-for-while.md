---
layout: default
parent: Solidity
grand_parent: ISBiT
nav_order: 4
---

# For i While petlje

Solidity podržava `for`, `while` i `do while` petlje.

Nemojte pisati petlje koje nemaju ograničenja jer može doseći `gas limit`, uzrokujući neuspjeh vaše transakcije. Iz ovog razloga, `while` i `do while` petlje se rijetko koriste.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Loop {
    function loop() public {
        // for loop
        for (uint i = 0; i < 10; i++) {
            if (i == 3) {
                // Skip to next iteration with continue
                continue;
            }
            if (i == 5) {
                // Exit loop with break
                break;
            }
        }

        // while loop
        uint j;
        while (j < 10) {
            j++;
        }
    }
}
```
