
# Offchain

Pametni ugovor koji svakome omogućuje uplatu ETH u ugovor
Samo vlasnik ugovora može povući ETH

Želimo omogućiti transakcije na našem ugovoru.

funkcija fund()

zelimo imati evidenciju tko nam je koliko uplatio.

```solidity

mapping(address => uint256) public whoFunded;

function fund() public payable {
    whoFunded[msg.sender] += msg.value;
}
```
