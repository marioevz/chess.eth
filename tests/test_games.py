import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

draw_outcome = 1
white_win_outcome = 2
black_win_outcome = 3

@pytest.mark.parametrize("moves,expected_outcome", 
    [
        ##### Inconclusive Outcomes: Valid moves still available #####

        # Fool's mate (Black wins)
        (["0x355", "0xd2c", "0x39e", "0xedf"], black_win_outcome),
        # Fool's mate (White wins)
        (["0x314", "0xda6", "0x2db", "0xd6d", "0x0e7"], white_win_outcome),
    ])
def test_valid_endgame(chess_contract, moves, expected_outcome):
    result = chess_contract.checkGameFromStart(moves)
    assert result[0] == expected_outcome