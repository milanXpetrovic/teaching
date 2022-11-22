# Strukture podataka

## Polja

Polja mogu biti zadani da imaju fiksnu ili dinamičku veličinu. Tip polja fiksne veličine `k` i tipa elementa `T` piše se kao `T[k]`, a polje dinamičke veličine kao `T[]`. Sintaksa pisanja polja razlikuje se od nekih drugih jezika, tako ćemo primjerice polje `x` koji sadrži 4 polja dinamičke veličine pisati kao `uint[][5]`, razlog tome je što u Solidity-u `X[3]` znači polje koji sadržava 3 elementa tipa `X`, a samim time i `X` može biti polje. Primjerice u varijabli `uint[][5] memory x` ako želimo pristupiti sedmom `uint` elemetu u drugom dinamičkom polju koristit ćemo `x[2][6]`

```solidity
// primjer polja zadane veličine
uint balance[10];

// primjer polja dinamičke veličine
type[] arrayName;
```

## Struktura

Solidity pruža način za definiranje novih tipova u obliku struktura. U nastavku je prikazan primjer korištenja strukture.

```solidity
// Primjer strukture
struct Campaign {
        address payable beneficiary;
        uint fundingGoal;
        uint numFunders;
        uint amount;
        mapping (uint => Funder) funders;
    }
```

## Mapping

Mapiranja koriste sintaksu `mapping(KeyType => ValueType)`, a tipovi varijabli u mapiranju deklariraju se pomoću sintakse `mapping(KeyType => ValueType) VariableName`. `KeyType` može biti bilo koji ugrađeni tip vrijednosti, npr. bajtovi, string. Drugi korisnički definirani ili složeni tipovi, kao što su mapiranje, strukture ili polja, nisu dopušteni. `ValueType` može biti bilo koji tip, uključujući mapiranja, polja i strukture.

```solidity
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.0 <0.9.0;

// Primjer korištenja mappinga
contract MappingExample {
    mapping(address => uint) public balances;

    function update(uint newBalance) public {
        balances[msg.sender] = newBalance;
    }
}

contract MappingUser {
    function f() public returns (uint) {
        MappingExample m = new MappingExample();
        m.update(100);
        return m.balances(address(this));
    }
}
```

## Enum

Solidity podržava enumeraciju, koja je korisna za izbor i praćenje stanja.

`Enum` se može deklarirati i izvan ugovora.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Enum {
    // Enum representing queue status
    enum Status {
        Waiting,
        Accepted,
        Rejected,
        Processed
    }

    // Default value is the first element listed in
    // definition of the type, in this case "Waiting"
    Status public status;

    // Returns uint
    // Waiting  - 0
    // Accepted - 1
    // Rejected - 3
    // Processed - 4

    function get() public view returns (Status) {
        return status;
    }

    // Update status by passing uint into input
    function set(Status _status) public {
        status = _status;
    }

    // You can update to a specific enum like this
    function cancel() public {
        status = Status.Canceled;
    }

    // delete resets the enum to its first value, 0
    function reset() public {
        delete status;
    }
}
```
