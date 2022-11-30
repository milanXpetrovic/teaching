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

{: .important  }
> Napomena
> ```
> pip3 install cryptography==3.2
> from solcx import compile_standard, install_solc
> install_solc("0.6.0")
> ```



- [Web3.py dokumentacija](https://web3py.readthedocs.io/en/v5/)
- [Smart Contract Developer Bootcamp Setup Instructions: Brownie Track](https://chain.link/bootcamp/brownie-setup-instructions)





https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl

https://github.com/trufflesuite/ganache

``` pip install web3 ```


## Primjer 1

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




