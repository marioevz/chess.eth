import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

@pytest.mark.parametrize("game_state,movement, player_state, black_move,expected_new_state,expected_new_player_state", 
    [
        # White up
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6e3", "0x00070000", False,
         "0x0000000000000000000000000000400000000000000000000000000000000000", "0x00070000"),
        # White down
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6d3", "0x00070000", False,
         "0x0000000000000000000000000000000000000000000040000000000000000000", "0x00070000"),
        # White right
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6dc", "0x00070000", False,
         "0x0000000000000000000000000000000000040000000000000000000000000000", "0x00070000"),
        # White left
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6da", "0x00070000", False,
         "0x0000000000000000000000000000000000000400000000000000000000000000", "0x00070000"),
        # White rook queen-side start move
        ("0x0000000000000000000000000000000000000000000000000000000000000004", "0x038", "0x00070000", False,
         "0x0000000400000000000000000000000000000000000000000000000000000000", "0x80070000"),
        # White rook king-side start move
        ("0x0000000000000000000000000000000000000000000000000000000040000000", "0x1ff", "0x00070000", False,
         "0x4000000000000000000000000000000000000000000000000000000000000000", "0x00870000"),
        # Black rook queen-side start move
        ("0x0000000c00000000000000000000000000000000000000000000000000000000", "0xe00", "0x383f0000", True,
         "0x000000000000000000000000000000000000000000000000000000000000000c", "0xb83f0000"),
        # Black rook king-side start move
        ("0xc000000000000000000000000000000000000000000000000000000000000000", "0xfc7", "0x383f0000", True,
         "0x00000000000000000000000000000000000000000000000000000000c0000000", "0x38bf0000"),
        
    ])
def test_valid_movements(chess_contract, game_state, movement, player_state, black_move, expected_new_state, expected_new_player_state):
    result = chess_contract.verifyExecuteMove(game_state, movement, player_state, "0x00", black_move)
    assert result[0] == expected_new_state
    assert result[1] == expected_new_player_state


@pytest.mark.parametrize("game_state,movement,black_move,err", 
    [
        # No move
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6db", False, "inv move stale"),
        # White same color in-between square
        ("0x0000400000000000000000000000400000000000000000000000000000000000", "0xec3", False, "inv move"),
        # White diff color in-between square
        ("0x0000000000000000000000000000c00000000000000000000000000000004000", "0x0fb", False, "inv move"),
        # White up-right
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6e4", False, "inv move"),
        # White down-right
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6d4", False, "inv move"),
        # White up-left
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6e2", False, "inv move"),
        # White down-left
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6d2", False, "inv move"),
        # White L move
        ("0x0000000000000000000000000000000000004000000000000000000000000000", "0x6e5", False, "inv move"),
    ])
def test_invalid_movements(chess_contract, game_state, movement, black_move, err):
    with reverts(err):
        chess_contract.verifyExecuteMove(game_state, movement, "0x00", "0x00", black_move)