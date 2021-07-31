# chess.eth
Chess implemented in a Solidity Smart Contract

The goal of this smart contract is to, given a set of movements of two players,
be able to calculate the outcome of the game on-chain, by calling checkGameFromStart.

Another smart contract should be responsible for the verification of the signatures of each move,
ideally using a SNARK, where each movement is signed by hashing the list of movements/signatures before it.
