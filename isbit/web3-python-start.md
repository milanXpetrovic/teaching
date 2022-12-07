---
layout: default
title: Web3
has_children: true
layout: default
parent: ISBiT
has_toc: false
---

# Postavljanje razvojnog okruženja za Web3.py 

Web3.py je Python biblioteka koja se koristi za rad s Ethereum mrežom. Omogućuje izvršavanje transakcije i interakcije s pametnim ugovorima jednostavnog API-ja. Web3.py također omogućuje pristup različitim podacima iz Ethereum mreže, poput stanja računa i transakcija, što je korisno za razvoj različitih aplikacija na Ethereum mreži, poput decentraliziranih aplikacija (dApps) i drugih alata za rad s Ethereum mrežom.

**Razvojno okruženje:**

- [VS Code](https://code.visualstudio.com/download)

**Dodaci za VSC:**

- Python (>= 3.8.0)
- Solidity

**Python moduli:**

- py-solc-x
- web3

Osim Python modula i Solidity-a, potrebno je instalirati testnu mrežu koja se koristi za postavljanje pametnih ugovora.

**Izvori:**

- [Web3.py dokumentacija](https://web3py.readthedocs.io/en/v5/)
- [Smart Contract Developer Bootcamp Setup Instructions: Brownie Track](https://chain.link/bootcamp/brownie-setup-instructions)
- [Install Node.js on WSL](https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl)
- [Ganache testna mreža](https://github.com/trufflesuite/ganache)

## Primjer: Pokretanje pametnog ugovora pomoću pythona na Ganache testnoj mreži

- Kreirajte direktorij koji sadrži pametan ugovor unutar `.sol` datoteke  i `deploy.py` datoteku koja se koristi za postavljanje pametnog ugovora na testnu mrežu.

### Pametni ugovor

Primjer pametnog ugovora:

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    
    // this will get initialized to 0!
    uint256 favoriteNumber;
    bool favoriteBool;
    
    // defines a structure for a person, with a favorite number and name
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    // an array of people, publicly accessible
    People[] public people;
    
    // a mapping from a name to a favorite number, publicly accessible
    mapping(string => uint256) public nameToFavoriteNumber;
    
    // function to store a new favorite number
    function store(uint256 _favoriteNumber) public {
        // set the favoriteNumber variable to the value passed in as an argument
        favoriteNumber = _favoriteNumber;
    }
    
    // function to retrieve the current favorite number
    function retrieve() public view returns(uint256) {
        // return the current value of the favoriteNumber variable
        return favoriteNumber;
    }
    
    // function to add a new person to the contract
    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        // add a new person to the people array
        people.push(People(_favoriteNumber, _name));
        // update the nameToFavoriteNumber mapping with the new name and favorite number
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }    
}

```

### Ganache testna mreža

Naredba za preuzimanje Docker slike:
```docker pull trufflesuite/ganache-cli```

Nakon uspješnog pokretanja Ganache mreže u terminalu se ispisuje sadržaj koji sadrži informacije o mreži i nekoliko adresa i njihovih privatnih ključeva.

```console

Available Accounts
==================
(0) 0xaC0837a0785ffe2CDd9762a1fba452D636e6400D (1000 ETH)

...

Private Keys
==================
(0) 0x9243a4a666d641d827843f1263385e08d539a5b40e70bfc4c02e7f91446a5c6f

...

RPC Listening on 127.0.0.1:8545
```

### deploy.py

{: .important-title}
> Napomena
>
> Prilikom pokretanja programa, poziv `from solcx import compile_standard` može javiti grešku koja javlja da paket `solcx` nije instaliran ili da nedostaju `cryptography` paketi.
> Ovaj problem može se riješiti instalacijom paketa `cryptography==3.2` i unutar programskog koda na samom početku dodaje se:
> ```python
> from solcx import compile_standard, install_solc
> install_solc("0.6.0")
> ```

```python
from solcx import compile_standard, install_solc

# install_solc("0.6.0")

import json
from web3 import Web3

# Read the contents of the SimpleStorage.sol contract file
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile the Solidity contract using the solcx package
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# Save the compiled contract's bytecode and ABI to a local file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract the bytecode and ABI from the compiled contract
# bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
```

Nakon pokreanja testne mreže, potrebno je povezati se na mrežu i postaviti ugovor:

```python
# Connect to ganache
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
chain_id = 1337
my_addres = "0x3a15E757b305981111673fF06A410B04Ae7216A4"
private_key = "0xc4a748b56159fc035f43951eedab4119988446f368084891892ec13cb3e0da36"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce
nonce = w3.eth.getTransactionCount(my_addres)

# Build a transaction
transaction = SimpleStorage.constructor().build_transaction(
    {"chainId": chain_id, "from": my_addres, "nonce": nonce}
)

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
```

Primjer interakcije s ugovorom:

```python
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

store_transaction = simple_storage.functions.store(33).buildTransaction(
    {"chainId": chain_id, "from": my_addres, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())
```
