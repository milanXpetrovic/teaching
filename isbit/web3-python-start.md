---
layout: default
title: Web3
has_children: true
layout: default
parent: ISBiT
has_toc: false
---

# Postavljanje razvojnog okruženja za Web3.py 

- [VS Code](https://code.visualstudio.com/download)

Dodaci za VSC:

- Python (>= 3.8.0)
- Solidity

Python moduli:

- py-solc-x
- web3

{: .important-title}
> Napomena
> Prilikom pokretanja programa, poziv `from solcx import compile_standard` može javiti grešku koja javlja da paket `solcx` nije instaliran ili da nedostaju `cryptography` paketi.
> Ovaj problem može se riješiti instalacijom paketa `cryptography==3.2` i unutar programskog koda na samom po;etku dodaje se 
> ```python
> from solcx import compile_standard, install_solc
> install_solc("0.6.0")
> ```

- [Web3.py dokumentacija](https://web3py.readthedocs.io/en/v5/)
- [Smart Contract Developer Bootcamp Setup Instructions: Brownie Track](https://chain.link/bootcamp/brownie-setup-instructions)

- [Install Node.js on WSL](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
- [Ganache testna mreža](https://github.com/trufflesuite/ganache)

## Primjer

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    
    // this will get initialized to 0!
    uint256 favoriteNumber;
    bool favoriteBool;
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;
    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }    
    
}
```




