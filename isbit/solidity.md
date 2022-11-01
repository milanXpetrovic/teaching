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

## Varijable stanja i funkcije

U Solidityu je potrebno specificirati tip svake varijable (globalne i lokalne). Solidity pruža nekoliko elementarnih tipova koji se mogu kombinirati u složene tipove. Ovi tipovi također se nazivaju vrijednosnim tipovima jer će se varijable ovih tipova uvijek prosljeđivati po vrijednosti, tj. uvijek se kopiraju kada se dodjeljuju ili koriste kao argumenti funkcije. Tipovi mogu međusobno komunicirati u izrazima koji sadrže operatore. Reference različitih operatora možete pronaći na [Order of Precedence of Operators](https://docs.soliditylang.org/en/latest/types.html#order)

**Elementarni tipovi podataka:**

- `bool` - Moguće vrijednosti su konstante `true` i `false`.
- `int` / `uint` - Cijeli brojevi s predznakom i bez predznaka različitih veličina. Veličina im varira ovisno o ključnoj riječi od `uint8` do `uint256`. `uint` i `int` su aliasi za `uint256` odnosno `int256`.
- `fixed` / `ufixed` - Broj s fiksnom točkom, s predznakom i bez predznaka različitih veličina. Ključne riječi `ufixedMxN` i `fixedMxN`, gdje `M` predstavlja broj bitova koje uzima tip, a `N` predstavlja koliko je decimalnih točaka dostupno. `M` mora biti djeljiv s 8 i ide od 8 do 256 bita. `N` mora biti između 0 i 80, uključivo. `ufixed` i `fixed` su aliasi za `ufixed128x18` odnosno `fixed128x18`.
- `address` - sadrži vrijednost od 20 bajtova (veličina Ethereum adrese).
- `address payable` - ista kao i `address`, ali s dodatnim članovima `transfer` i `send`. Razlika `address payable` pd `address` je da je `address payable` adresa na koju možete poslati Ether, dok ne biste trebali slati Ether na `address`, običnu adresu, na primjer zato što bi to mogao biti pametni ugovor koji nije izgrađen za prihvaćanje Ethera. [Svi članovi address payable](https://docs.soliditylang.org/en/latest/units-and-global-variables.html#address-related)

**Nizovi**
Za razliku od elementarnih tipova možemo imati i nizove čija veličina može biti zanada, odnosno fiksna ili dinamična.  

- Nizovi s fiksno zadanom veličinom su primjerice `bytes1`, `bytes2`, `bytes3`, …, `bytes32` koji sadrže niz bajtova od jedan do 32. S članom `.length` koji daje fiksnu duljinu niza bajtova (samo za čitanje).
- Nizovi koji su zadani samo kao `bytes` ili `string` su pak niz koji je dinamičke veličine i sadržava bajtove ili UTF-8 znakove.

**Funkcije**
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

## Strukture podataka

### Polja

Polja mogu biti zadani da imaju fiksnu ili dinamičku veličinu. Tip polja fiksne veličine `k` i tipa elementa `T` piše se kao `T[k]`, a polje dinamičke veličine kao `T[]`. Sintaksa pisanja polja razlikuje se od nekih drugih jezika, tako ćemo primjerice polje `x` koji sadrži 4 polja dinamičke veličine pisati kao `uint[][5]`, razlog tome je što u Solidity-u `X[3]` znači polje koji sadržava 3 elementa tipa `X`, a samim time i `X` može biti polje. Primjerice u varijabli `uint[][5] memory x` ako želimo pristupiti sedmom `uint` elemetu u drugom dinamičkom polju koristit ćemo `x[2][6]`

```solidity
// primjer polja zadane veličine
uint balance[10];

// primjer polja dinamičke veličine
type[] arrayName;
```

### Struktura

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

### Mapping

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

**Enum**
 //TODO

## If/Else

```solidity
// SPDX-License-Identifier: MIT
pragma solidity <0.8.13;

contract IfElse {
    function foo(uint x) public pure returns (uint) {
        if (x < 10) {
            return 0;
        } else if (x < 20) {
            return 1;
        } else {
            return 2;
        }
    }

    function ternary(uint _x) public pure returns (uint) {
        // if (_x < 10) {
        //     return 1;
        // }
        // return 2;

        // shorthand way to write if / else statement
        // the "?" operator is called the ternary operator
        return _x < 10 ? 1 : 2;
    }
}
```

## For i While petlje

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

## Events

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

## Konstruktor

 Konstruktor je funkcija koja se izvršava prilikom stvaranja ugovora, ova funkcija nije obavezna u ugovoru, da bi funkcija bila konstruktor dodajemo ključnu riječ `constructor`.

```solidity
contract MyContract {
    string public username;

    constructor(string memory _username) {
        name = _name;
    }
}
```

Postoje dva načina za inicijalizaciju nadređenog ugovora s parametrima.

Prosljeđivanje parametara u listi nasljeđivanja.

```solidity
contract B is X("Input to X"), Y("Input to Y") { }
```

Prosljeđivanje parametara u konstruktoru, slično modifikatorima funkcija

```solidity
contract C is X, Y {
    constructor(string memory _name, string memory _text) X(_name) Y(_text) {}
}
```

## Nasljeđivanje

Solidity podržava višestruko nasljeđivanje. Ugovori mogu naslijediti druge ugovore korištenjem ključne riječi `is`. Funkcija koja će biti nadjačana podređenim ugovorom mora biti deklarirana kao virtualna. Funkcija koja će nadjačati nadređenu funkciju mora koristiti ključnu riječ `override`. Red nasljeđivanja je važan. Nasljeđivanje se navodi redoslijedom od "najsličniji osnovi" do "najviše izvedeni".

```solidity
Redosljed nasljedivanja
    A
   / \
  B   C
 / \ /
F  D,E

```

```solidity

contract A {
    function foo() public pure virtual returns (string memory) {
        return "A";
    }
}

// Ugovor B nasljeđuje od A
contract B is A {
    // korištenje override nad funkcijom A.foo()
    function foo() public pure virtual override returns (string memory) {
        return "B";
    }
}

contract C is A {
    // korištenje override nad funkcijom A.foo()
    function foo() public pure virtual override returns (string memory) {
        return "C";
    }
}

contract D is B, C {
    // D.foo() -> "C"
    function foo() public pure override(B, C) returns (string memory) {
        return super.foo();
    }
}

contract E is C, B {
    // E.foo() -> "B"
    function foo() public pure override(C, B) returns (string memory) {
        return super.foo();
    }
}

// Red nasljeđivanja je važan.
// Nasljeđivanje se navodi redoslijedom od "najsličniji osnovi" do "najviše izvedeni".
// Zamjena redoslijeda A i B će dati grešku.
contract F is A, B {
    function foo() public pure override(A, B) returns (string memory) {
        return super.foo();
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
