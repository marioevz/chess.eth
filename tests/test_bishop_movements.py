import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

@pytest.mark.parametrize("game_state,movement,blackMove,expected_new_state", 
    [
        # White move 1 right 1 up
        ("0x0000000000000000000000000000000000000000000020000000000000000000", "0x4dc", False,
         "0x0000000000000000000000000000000000020000000000000000000000000000"),
        # White move 2 right 2 up
        ("0x0000000000000000000000000000000000000000000020000000000000000000", "0x4e5", False,
         "0x0000000000000000000000000020000000000000000000000000000000000000"),
        # White move 1 right 1 up, take piece
        ("0x0000000000000000000000000000000000090000000020000000000000000000", "0x4dc", False,
         "0x0000000000000000000000000000000000020000000000000000000000000000"),
        # White move 2 right 2 up, take piece
        ("0x0000000000000000000000000090000000000000000020000000000000000000", "0x4e5", False,
         "0x0000000000000000000000000020000000000000000000000000000000000000"),
        
    ])
def test_valid_movements(chess_contract, game_state, movement, blackMove, expected_new_state):
    assert chess_contract.verifyExecuteMove(game_state, movement, "0x00", "0x00", blackMove)[0] == expected_new_state


@pytest.mark.parametrize("game_state,movement,blackMove,err", 
    [
        # No move
        ("0x0000000000000000000000000000000000002000000000000000000000000000", "0x6db", False, "inv move stale"),
        # White same color in-between square
        ("0x0000000000000000000000000000000000020000000020000000000000000000", "0x4e5", False, "inv move"),
        # White diff color in-between square
        ("0x0000000000000000000000000000000000090000000020000000000000000000", "0x4e5", False, "inv move"),
        # White up
        ("0x0000000000000000000000000000000000020000000000000000000000000000", "0x724", False, "inv move"),
        # White down
        ("0x0000000000000000000000000000000000020000000000000000000000000000", "0x714", False, "inv move"),
        # White right
        ("0x0000000000000000000000000000000000020000000000000000000000000000", "0x71d", False, "inv move"),
        # White left
        ("0x0000000000000000000000000000000000020000000000000000000000000000", "0x71b", False, "inv move"),
        # White L move
        ("0x0000000000000000000000000000000000002000000000000000000000000000", "0x6e5", False, "inv move"),
    ])
def test_invalid_movements(chess_contract, game_state, movement, blackMove, err):
    with reverts(err):
        chess_contract.verifyExecuteMove(game_state, movement, "0x00", "0x00", blackMove)
