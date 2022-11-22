# Konstruktori i nasljeđivanje

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
