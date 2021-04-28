import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)


@pytest.mark.parametrize("game_state,movement,playerExtra,blackMove,expected_new_state,expected_new_player_extra", 
    [
        # White move 1 up
        ("0x0000000000000000000000000000000000006000000000000000000000000000", "0x6e3", "0x00070000", False,
         "0x0000000000000000000000000000600000000000000000000000000000000000","0x80872300"),
        # White move 1 down
        ("0x0000000000000000000000000000000000006000000000000000000000000000", "0x6d3", "0x00070000", False,
         "0x0000000000000000000000000000000000000000000060000000000000000000","0x80871300"),
        # White move 1 right
        ("0x0000000000000000000000000000000000006000000000000000000000000000", "0x6dc", "0x00070000", False,
         "0x0000000000000000000000000000000000060000000000000000000000000000","0x80871c00"),
        # White move 1 left
        ("0x0000000000000000000000000000000000006000000000000000000000000000", "0x6da", "0x00070000", False,
         "0x0000000000000000000000000000000000000600000000000000000000000000","0x80871a00"),
        # White castling queen-side 
        ("0x0000000000000000000000000000000000000000000000000000000000060004", "0x102", "0x00070000", False,
         "0x0000000000000000000000000000000000000000000000000000000000004600","0x80870200"),
        # White castling king-side 
        ("0x0000000000000000000000000000000000000000000000000000000040060000", "0x106", "0x00070000", False,
         "0x0000000000000000000000000000000000000000000000000000000006400000","0x80870600"),

        # White castling queen-side, king-side rook already moved
        ("0x0000000000000000000000000000000000000000000000000000000000060004", "0x102", "0x00870000", False,
         "0x0000000000000000000000000000000000000000000000000000000000004600","0x80870200"),
        # White castling king-side, queen-side rook already moved
        ("0x0000000000000000000000000000000000000000000000000000000040060000", "0x106", "0x80070000", False,
         "0x0000000000000000000000000000000000000000000000000000000006400000","0x80870600"),

        # White castling queen-side rook under attack
        ("0x0000000d00000000000000000000000000000000000000000000000000060004", "0x102", "0x00070000", False,
         "0x0000000d00000000000000000000000000000000000000000000000000004600","0x80870200"),
        # White castling king-side rook under attack
        ("0xd000000000000000000000000000000000000000000000000000000040060000", "0x106", "0x00070000", False,
         "0xd000000000000000000000000000000000000000000000000000000006400000","0x80870600"),
        # White castling queen-side empty under attack
        ("0x000000d000000000000000000000000000000000000000000000000000060004", "0x102", "0x00070000", False,
         "0x000000d000000000000000000000000000000000000000000000000000004600","0x80870200"),

        # Black move 1 up
        ("0x00000000000000000000000000000000000e0000000000000000000000000000", "0x724", "0x383f3c00", True,
         "0x000000000000000000000000000e000000000000000000000000000000000000","0xb8bf2400"),
        # Black move 1 down
        ("0x00000000000000000000000000000000000e0000000000000000000000000000", "0x714", "0x383f3c00", True,
         "0x0000000000000000000000000000000000000000000e00000000000000000000","0xb8bf1400"),
        # Black move 1 right
        ("0x00000000000000000000000000000000000e0000000000000000000000000000", "0x71d", "0x383f3c00", True,
         "0x0000000000000000000000000000000000e00000000000000000000000000000","0xb8bf1d00"),
        # Black move 1 left
        ("0x00000000000000000000000000000000000e0000000000000000000000000000", "0x71b", "0x383f3c00", True,
         "0x000000000000000000000000000000000000e000000000000000000000000000","0xb8bf1b00"),
        # Black castling queen-side 
        ("0x000e000c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x383f3c00", True,
         "0x0000ce0000000000000000000000000000000000000000000000000000000000","0xb8bf3a00"),
        # Black castling king-side 
        ("0xc00e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x383f3c00", True,
         "0x0ec0000000000000000000000000000000000000000000000000000000000000","0xb8bf3e00"),
        # Black castling queen-side rook under attack
        ("0x000e000c00000000000000000000000000000000000000000000000000000005", "0xf3a", "0x383f3c00", True,
         "0x0000ce0000000000000000000000000000000000000000000000000000000005","0xb8bf3a00"),
        # Black castling king-side rook under attack
        ("0xc00e000000000000000000000000000000000000000000000000000050000000", "0xf3e", "0x383f3c00", True,
         "0x0ec0000000000000000000000000000000000000000000000000000050000000","0xb8bf3e00"),
        # Black castling queen-side empty under attack
        ("0x000e000c00000000000000000000000000000000000000000000000000000050", "0xf3a", "0x383f3c00", True,
         "0x0000ce0000000000000000000000000000000000000000000000000000000050","0xb8bf3a00"),
        # Black castling queen-side, king-side rook already moved
        ("0x000e000c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x38bf3c00", True,
         "0x0000ce0000000000000000000000000000000000000000000000000000000000","0xb8bf3a00"),
        # Black castling king-side, queen-side rook already moved
        ("0xc00e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0xb83f3c00", True,
         "0x0ec0000000000000000000000000000000000000000000000000000000000000","0xb8bf3e00"),
        
    ])
def test_valid_movements(chess_contract, game_state, movement, playerExtra, blackMove, expected_new_state, expected_new_player_extra):
    result = chess_contract.verifyExecuteMove(game_state, movement, playerExtra, "0x00", blackMove)
    assert result[0] == expected_new_state
    assert result[1] == expected_new_player_extra


@pytest.mark.parametrize("game_state,movement,playerExtra,blackMove,err", 
    [
        # No move
        ("0x0000000000000000000000000000000000006000000000000000000000000000", "0x6db", "0x00000000", False, "inv move stale"),
        # White castling queen-side rook already moved
        ("0x0000000000000000000000000000000000000000000000000000000000060004", "0x102", "0x80000000", False, "inv move"),
        # White castling king-side rook already moved
        ("0x0000000000000000000000000000000000000000000000000000000040060000", "0x106", "0x00870000", False, "inv move"),
        # White castling queen-side king already moved
        ("0x0000000000000000000000000000000000000000000000000000000000060004", "0x102", "0x80870000", False, "inv move"),
        # White castling king-side king already moved
        ("0x0000000000000000000000000000000000000000000000000000000040060000", "0x106", "0x80870000", False, "inv move"),
        # White castling queen-side square occupied same color 1
        ("0x0000000000000000000000000000000000000000000000000000000000060034", "0x102", "0x00070000", False, "inv move"),
        # White castling queen-side square occupied same color 2
        ("0x0000000000000000000000000000000000000000000000000000000000063004", "0x102", "0x00070000", False, "inv move"),
        # White castling queen-side square occupied diff color 1
        ("0x00000000000000000000000000000000000000000000000000000000000600a4", "0x102", "0x00070000", False, "inv move"),
        # White castling queen-side square occupied diff color 2
        ("0x0000000000000000000000000000000000000000000000000000000000060a04", "0x102", "0x00070000", False, "inv move"),
        # White castling king-side square occupied same color 1
        ("0x0000000000000000000000000000000000000000000000000000000043060000", "0x106", "0x00070000", False, "inv move"),
        # White castling king-side square occupied same color 2
        ("0x0000000000000000000000000000000000000000000000000000000040260000", "0x106", "0x00070000", False, "inv move"),
        # White castling king-side square occupied diff color 1
        ("0x000000000000000000000000000000000000000000000000000000004b060000", "0x106", "0x00070000", False, "inv move"),
        # White castling king-side square occupied diff color 2
        ("0x0000000000000000000000000000000000000000000000000000000040b60000", "0x106", "0x00070000", False, "inv move"),
        # White castling queen-side under attack
        ("0x0000d00000000000000000000000000000000000000000000000000000060004", "0x102", "0x00070000", False, "inv move"),
        # White castling king-side under attack
        ("0x00d0000000000000000000000000000000000000000000000000000040060000", "0x106", "0x00070000", False, "inv move"),
        # White castling king currently in check
        ("0x000c000000000000000000000000000000000000000000000000000040060000", "0x106", "0x00070000", False, "inv move"),

        # No move
        ("0x000000000000000000000000000000000000e000000000000000000000000000", "0x6db", "0x383f3c00", True, "inv move stale"),
        # Black castling queen-side rook already moved
        ("0x000e000c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0xb83f3c00", True, "inv move"),
        # Black castling king-side rook already moved
        ("0xc00e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x38bf3c00", True, "inv move"),
        # Black castling queen-side king already moved
        ("0x000e000c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0xb8bf3c00", True, "inv move"),
        # Black castling king-side king already moved
        ("0xc00e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0xb8bf3c00", True, "inv move"),
        # Black castling queen-side square occupied same color 1
        ("0x000eb00c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x383f3c00", True, "inv move"),
        # Black castling queen-side square occupied same color 2
        ("0x000e00bc00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x383f3c00", True, "inv move"),
        # Black castling queen-side square occupied diff color 1
        ("0x000e300c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x383f3c00", True, "inv move"),
        # Black castling queen-side square occupied diff color 2
        ("0x000e030c00000000000000000000000000000000000000000000000000000000", "0xf3a", "0x383f3c00", True, "inv move"),
        # Black castling king-side square occupied same color 1
        ("0xc0be000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x383f3c00", True, "inv move"),
        # Black castling king-side square occupied same color 2
        ("0xcb0e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x383f3c00", True, "inv move"),
        # Black castling king-side square occupied diff color 1
        ("0xc30e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x383f3c00", True, "inv move"),
        # Black castling king-side square occupied diff color 2
        ("0xc03e000000000000000000000000000000000000000000000000000000000000", "0xf3e", "0x383f3c00", True, "inv move"),
        # Black castling queen-side under attack
        ("0x000e000c00000000000000000000000000000000000000000000000000005000", "0xf3a", "0x383f3c00", True, "inv move"),
        # Black castling king-side under attack
        ("0xc00e000000000000000000000000000000000000000000000000000000500000", "0xf3e", "0x383f3c00", True, "inv move"),
        # Black castling king currently in check
        ("0xc00e000000000000000000000000000000000000000000000000000000040000", "0xf3e", "0x383f3c00", True, "inv move"),


    ])
def test_invalid_movements(chess_contract, game_state, movement, playerExtra, blackMove, err):
    with reverts(err):
        chess_contract.verifyExecuteMove(game_state, movement, playerExtra, "0x00", blackMove)



@pytest.mark.parametrize("start_game_state,start_player_state,start_opponent_state,movements,expected_new_state", 
    [
        # Queen-side castling after king-side rook moved (Both colors)
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x1cf", "0xff7", "0x102", "0xf3a"],
         "0x0000ce00c9999990000000000000000000000000000000004111111000004600"),
        # King-side castling after queen-side rook moved (Both colors)
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x008", "0xe30", "0x106", "0xf3e"],
         "0x0ec000000999999c000000000000000000000000000000000111111406400000"),
        # White Queen-side castling after opponent queen-side rook moved (Opposite for black)
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x1cf", "0xe30", "0x102", "0xf3e"],
         "0x0ec000000999999c000000000000000000000000000000004111111000004600"),
        # White King-side castling after opponent king-side rook moved (Opposite for black)
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x008", "0xff7", "0x106", "0xf3a"],
         "0x0000ce00c9999990000000000000000000000000000000000111111406400000"),



        ("0xc00e000c00000000000000000000000000000000000000000000000040060004", "0x000704ff", "0x383f3cff", ["0x1cf", "0xff7", "0x3c7", "0xdff"],
         "0xc00e000c00000000000000000000000000000000000000000000000040060004"),
        
    ])
def test_valid_movement_combinations(chess_contract, start_game_state, start_player_state, start_opponent_state, movements, expected_new_state):
    result = chess_contract.checkGame(start_game_state, start_player_state, start_opponent_state, False, movements)
    assert result[0] == 0
    assert result[1] == expected_new_state

@pytest.mark.parametrize("start_game_state,start_player_state,start_opponent_state,movements,err", 
    [
        # White Queen-side castling after rook moved and returned
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x008", "0xe30", "0x200", "0xc38", "0x102"],
        "inv move"),
        # Black Queen-side castling after rook moved and returned
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x008", "0xe30", "0x200", "0xc38", "0x103", "0xf3a"],
        "inv move"),
        # White King-side castling after rook moved and returned
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x1cf", "0xff7", "0x3c7", "0xdff", "0x106"],
        "inv move"),
        # Black King-side castling after rook moved and returned
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x1cf", "0xff7", "0x3c7", "0xdff", "0x105", "0xf3e"],
        "inv move"),
        # White Queen-side ends up in check
        ("0x00000c0000000000000000000000000000000000000000000000000000060004", "0x000704ff", "0x383f3cff", ["0x102"],
        "inv check"),
        # White King-side ends up in check
        ("0x0c00000000000000000000000000000000000000000000000000000040060000", "0x000704ff", "0x383f3cff", ["0x106"],
        "inv check"),
        # Black Queen-side ends up in check
        ("0x000e000c00000000000000000000000000000000000000000000000000060004", "0x000704ff", "0x383f3cff", ["0x002", "0xf3a"],
        "inv check"),
        # Black King-side ends up in check
        ("0xc00e000000000000000000000000000000000000000000000000000040060000", "0x000704ff", "0x383f3cff", ["0x1c6", "0xf3e"],
        "inv check"),
    ])
def test_invalid_movement_combinations(chess_contract, start_game_state, start_player_state, start_opponent_state, movements, err):
    with reverts(err):
        chess_contract.checkGame(start_game_state, start_player_state, start_opponent_state, False, movements)