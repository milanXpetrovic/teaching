---
layout: default
parent: Solidity
---

# Events

Eventi nam evidentiranje aktivnosti unutar Ehereum blockchaina.
Oni su nasljedni članovi ugovora. Kada ih pozovete, uzrokuju pohranjivanje argumenata u dnevnik transakcije - posebnu podatkovnu strukturu u blockchainu. Ti su zapisnici povezani s adresom ugovora, ugrađeni su u blockchain i ostaju tamo sve dok je blok dostupan. Dnevnik i njegovi podaci o događajima nisu dostupni unutar ugovora (čak ni iz ugovora koji ih je stvorio).

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.21 <0.9.0;

contract ClientReceipt {
    event Deposit(
        address indexed from,
        bytes32 indexed id,
        uint value
    );

    function deposit(bytes32 id) public payable {
        // Events are emitted using `emit`, followed by
        // the name of the event and the arguments
        // (if any) in parentheses. Any such invocation
        // (even deeply nested) can be detected from
        // the JavaScript API by filtering for `Deposit`.
        emit Deposit(msg.sender, id, msg.value);
    }
}
```

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Event {
    // Event declaration
    // Up to 3 parameters can be indexed.
    // Indexed parameters helps you filter the logs by the indexed parameter
    event Log(address indexed sender, string message);
    event AnotherLog();

    function test() public {
        emit Log(msg.sender, "Hello World!");
        emit Log(msg.sender, "Hello EVM!");
        emit AnotherLog();
    }
}

```
