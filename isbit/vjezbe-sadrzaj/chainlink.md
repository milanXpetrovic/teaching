---
layout: default
parent: ISBiT
nav_exclude: true
---

# Offchain

Pametni ugovor koji svakome omogućuje uplatu ETH u ugovor
Samo vlasnik ugovora može povući ETH

Želimo omogućiti transakcije na našem ugovoru.

funkcija fund()

zelimo imati evidenciju tko nam je koliko uplatio.

zelmo postaviti minimalnu vrijednost za uplatu

zelimo raditi u americkim dolarima a ne u ETH, odnosno potrebno je pretvoriti ETH -> USD.

```solidity

mapping(address => uint256) public whoFunded;

function fund() public payable {
    whoFunded[msg.sender] += msg.value;
}
```


https://www.npmjs.com/package/@chainlink/contracts

https://github.com/smartcontractkit/chainlink/tree/develop/contracts

```solicity
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
```
