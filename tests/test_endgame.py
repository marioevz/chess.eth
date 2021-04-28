import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

@pytest.mark.parametrize("game_state,player_state,opponent_state,expected_outcome", 
    [
        ##### Inconclusive Outcomes: Valid moves still available #####
        # King check evaded by 1-up
        ("0x000cec0a0000000000000000000060000000000c000000000000000000000000", "0x000723ff", "0x383f3bff", 0),
        # King check evaded by 1-down
        ("0x000cec0a000000000000000c0000600000000000000000000000000000000000", "0x000723ff", "0x383f3bff", 0),
        # King check evaded by 1-right
        ("0x0000ec0a000000000000000c000060000000000c000000000000000000000000", "0x000723ff", "0x383f3bff", 0),
        # King check evaded by 1-left
        ("0x000ce00a000000000000000c000060000000000c000000000000000000000000", "0x000723ff", "0x383f3bff", 0),

        # King check evaded by 1-up 1-left
        ("0xe00cc00000000000000000000000600c0000000c000000000000000000000000", "0x000723ff", "0x383f3fff", 0),
        # King check evaded by 1-up 1-right
        ("0xe000cc0000000000000000000000600c0000000c000000000000000000000000", "0x000723ff", "0x383f3fff", 0),
        # King check evaded by 1-down 1-left
        ("0xe00cc000000000000000000c0000600c00000000000000000000000000000000", "0x000723ff", "0x383f3fff", 0),
        # King check evaded by 1-down 1-right
        ("0xe000cc00000000000000000c0000600c00000000000000000000000000000000", "0x000723ff", "0x383f3fff", 0),

        # King's (White) check blocked by pawn (1-up)
        ("0x00cec00000000000000000000000000c0006000d0000100c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's (White) check blocked by pawn (2-up)
        ("0x00cec0000000000000000000c0000000d0060000c00000000100000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's (White) check removed by pawn take (1-up 1-left)
        ("0x00cec00000000000000000000000000c0006000d0000001c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's (White) check removed by pawn take (1-up 1-right)
        ("0x00cec0000000000000000000c0000000d0060000c10000000000000000000000", "0x00071cff", "0x383f3cff", 0),

        # King's (Black) check blocked by pawn (1-down)
        ("0x0000000000000000400009000000e00540000000000000000000000000046400", "0x383f23ff", "0x000703ff", 0),
        # King's (Black) check blocked by pawn (2-down)
        ("0x0000000000000900400000000000e00540000000000000000000000000046400", "0x383f23ff", "0x000703ff", 0),
        # King's (Black) check removed by pawn take (1-down 1-left)
        ("0x0000000000000000900000040500e00000000004000000000000000000046400", "0x383f23ff", "0x000703ff", 0),
        # King's (Black) check removed by pawn take (1-down 1-right)
        ("0x0000000000000000400000090000e05040000000000000000000000000046400", "0x383f23ff", "0x000703ff", 0),

        # King's check removed by knight (2-right,1-up)
        ("0x00cec0000000000300000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by knight (1-right,2-up)
        ("0x00cec0300000000000000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),

        # King's check removed by knight (1-left,2-up)
        ("0x000cec00000000000000000c000060000000000c00a000000000000003000000", "0x000723ff", "0x383f3bff", 0),
        # King's check removed by knight (2-left,1-up)
        ("0x000cec00000000000000000c000060000000000c00a000003000000000000000", "0x000723ff", "0x383f3bff", 0),

        # King's check removed by knight (2-left,1-down)
        ("0x00cec000000000000000000c000600000000000c00000a000000000300000000", "0x000724ff", "0x383f3bff", 0),
        # King's check removed by knight (1-left,2-down)
        ("0x00cec000000000000000000c000600000000000c00000a000000000000000030", "0x000724ff", "0x383f3bff", 0),

        # King's check removed by knight (1-right,2-down)
        ("0x030cec000000000000a000000000000c000060000000000c0000000000000000", "0x00071bff", "0x383f3bff", 0),
        # King's check removed by knight (2-right,1-down)
        ("0x000cec003000000000a000000000000c000060000000000c0000000000000000", "0x00071bff", "0x383f3bff", 0),

        # King's check removed by rook (up movement)
        ("0x00cec0000000000000000a000000000c000600000000000c0000000000000400", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by rook (down movement)
        ("0x00cec4000000000000000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by rook (right movement)
        ("0x00cec0000000000000000a040000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by rook (left movement)
        ("0x00cec0000000000040000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),

        # King's check removed by bishop (up-right movement)
        ("0x00cec000000000000000000c000600000000000c00000a000000000000000002", "0x000724ff", "0x383f3cff", 0),
        # King's check removed by bishop (up-left movement)
        ("0x000cec00000000000000000c000060000000000c00a000000000000020000000", "0x000723ff", "0x383f3bff", 0),
        # King's check removed by bishop (down-right movement)
        ("0x00cec0020000000000000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by bishop (down-left movement)
        ("0x200cec000000000000a000000000000c000060000000000c0000000000000000", "0x00071bff", "0x383f3bff", 0),

        # King's check removed by Queen (up movement)
        ("0x00cec0000000000000000a000000000c000600000000000c0000000000000500", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by Queen (down movement)
        ("0x00cec5000000000000000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by Queen (right movement)
        ("0x00cec0000000000000000a050000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by Queen (left movement)
        ("0x00cec0000000000050000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by Queen (up-right movement)
        ("0x00cec000000000000000000c000600000000000c00000a000000000000000005", "0x000724ff", "0x383f3cff", 0),
        # King's check removed by Queen (up-left movement)
        ("0x000cec00000000000000000c000060000000000c00a000000000000050000000", "0x000723ff", "0x383f3bff", 0),
        # King's check removed by Queen (down-right movement)
        ("0x00cec0050000000000000a000000000c000600000000000c0000000000000000", "0x00071cff", "0x383f3cff", 0),
        # King's check removed by Queen (down-left movement)
        ("0x500cec000000000000a000000000000c000060000000000c0000000000000000", "0x00071bff", "0x383f3bff", 0),

        ##### Conclusive Outcomes: No valid moves still available #####
        # King's check can't be removed by pawn take (1-up 1-right overflow)
        ("0x00cec00000000000000000000000000c0006000d1000000c0000000000000000", "0x00071cff", "0x383f3cff", 2),
    ])
def test_valid_endgame(chess_contract, game_state, player_state, opponent_state, expected_outcome):
    result = chess_contract.checkEndgame(game_state, player_state, opponent_state)
    assert result == expected_outcome

@pytest.mark.parametrize("start_game_state,start_player_state,start_opponent_state,movements,expected_new_state", 
    [
        # King's check removed by en passant piece take
        ("0x0c0ce00009000000000000000000000c106000000000000c0000000000000000", "0x00071dff", "0x383f3bff", ["0x7e7", "0xda6"],
         "0x0c0ce00000000000000000001900000c006000000000000c0000000000000000"),
        
    ])
def test_valid_inconclusive_combinations(chess_contract, start_game_state, start_player_state, start_opponent_state, movements, expected_new_state):
    result = chess_contract.checkGame(start_game_state, start_player_state, start_opponent_state, False, movements)
    assert result[0] == 0
    assert result[1] == expected_new_state

@pytest.mark.parametrize("start_game_state,start_player_state,start_opponent_state,movements,err", 
    [
        # White Queen-side castling after rook moved and returned
        ("0xc00e000c09999990000000000000000000000000000000000111111040060004", "0x000704ff", "0x383f3cff", ["0x008", "0xe30", "0x200", "0xc38", "0x102"],
        "inv move"),
    ])
def test_invalid_movement_combinations(chess_contract, start_game_state, start_player_state, start_opponent_state, movements, err):
    with reverts(err):
        chess_contract.checkGame(start_game_state, start_player_state, start_opponent_state, False, movements)
