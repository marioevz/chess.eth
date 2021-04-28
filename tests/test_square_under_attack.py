import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

TestCases = [
        ("0x0000000000000000000000000000000000000000000000000000000000005000", "0x03", False),
        # White square, enemy horse up-right 1
        ("0x000000000000000000b000000000500000000000000000000000000000000000", "0x23", True),
        # White square, enemy horse up-right 2
        ("0x00000000000b0000000000000000500000000000000000000000000000000000", "0x23", True),

        # White square, enemy horse up-left 1
        ("0x0000000000000b00000000000000500000000000000000000000000000000000", "0x23", True),
        # White square, enemy horse up-left 2
        ("0x0000000000000000000000b00000500000000000000000000000000000000000", "0x23", True),

        # White square, enemy horse down-left 1
        ("0x00000000000000000000000000005000000000b0000000000000000000000000", "0x23", True),
        # White square, enemy horse down-left 2
        ("0x000000000000000000000000000050000000000000000b000000000000000000", "0x23", True),

        # White square, enemy horse down-right 1
        ("0x0000000000000000000000000000500000000000000b00000000000000000000", "0x23", True),
        # White square, enemy horse down-right 2
        ("0x0000000000000000000000000000500000b00000000000000000000000000000", "0x23", True),

        # White square, enemy rook up
        ("0x0000c00000000000000000000000000000000000000000000000000000005000", "0x03", True),
        # White square, enemy rook up, border
        ("0xc000000000000000000000000000000000000000000000000000000050000000", "0x07", True),
        # White square, enemy rook up-left
        ("0x00000c0000000000000000000000000000000000000000000000000000005000", "0x03", False),
        # White square, friend rook up
        ("0x0000400000000000000000000000000000000000000000000000000000005000", "0x03", False),
        # White square, enemy rook up friend block
        ("0x0000c00000000000000000000000000000000000000000000000400000005000", "0x03", False),
        # White square, enemy rook up friend block 2
        ("0x0000c00000004000000000000000000000000000000000000000000000005000", "0x03", False),
        # White square, enemy rook up enemy block
        ("0x0000c00000000000000000000000000000000000000000000000a00000005000", "0x03", False),
        # White square, enemy rook up enemy block 2
        ("0x0000c00000000000000000000000000000000000000000000000900000005000", "0x03", False),
        # White square, check overflow
        ("0x00050000000000000000000000000000000000000000000000010000000d0000", "0x3c", False),
        
        # White square, enemy rook down
        ("0x000050000000000000000000000000000000000000000000000000000000c000", "0x3b", True),
        # White square, enemy rook down-left
        ("0x0000500000000000000000000000000000000000000000000000000000000c00", "0x3b", False),
        # White square, friend rook down
        ("0x0000500000000000000000000000000000000000000000000000000000004000", "0x3b", False),
        # White square, enemy rook down friend block
        ("0x000050000000000000000000000000000000000000000000000040000000c000", "0x3b", False),
        # White square, enemy rook down friend block 2
        ("0x000050000000400000000000000000000000000000000000000000000000c000", "0x3b", False),
        # White square, enemy rook down enemy block
        ("0x000050000000a00000000000000000000000000000000000000000000000c000", "0x3b", False),
        # White square, enemy rook down enemy block 2
        ("0x000050000000900000000000000000000000000000000000000000000000c000", "0x3b", False),
        # White square, check overflow
        ("0x0000e00000001000000000000000000000000000000000000000000000006000", "0x03", False),

        # White square, enemy queen right
        ("0x00000000000000000000000000000000d0000006000000000000000000000000", "0x18", True),
        # White square, enemy queen right-up
        ("0x000000000000000000000000d000000000000006000000000000000000000000", "0x18", False),
        # White square, friend queen right
        ("0x0000000000000000000000000000000050000006000000000000000000000000", "0x18", False),
        # White square, enemy queen right friend block
        ("0x00000000000000000000000000000000d0000016000000000000000000000000", "0x18", False),
        # White square, enemy queen right friend block 2
        ("0x00000000000000000000000000000000d1000006000000000000000000000000", "0x18", False),
        # White square, enemy queen right enemy block
        ("0x00000000000000000000000000000000d00000a6000000000000000000000000", "0x18", False),
        # White square, enemy queen right enemy block 2
        ("0x00000000000000000000000000000000d0000096000000000000000000000000", "0x18", False),
        # White square, check overflow
        ("0x0000000000000000000000000000000d60000000000000000000000000000000", "0x1f", False),

        # White square, enemy queen left
        ("0x000000000000000000000000000000006000000d000000000000000000000000", "0x1f", True),
        # White square, enemy queen left-up
        ("0x0000000000000000000000000000000d60000000000000000000000000000000", "0x1f", False),
        # White square, friend queen left
        ("0x0000000000000000000000000000000060000005000000000000000000000000", "0x1f", False),
        # White square, enemy queen left friend block
        ("0x000000000000000000000000000000006100000d000000000000000000000000", "0x1f", False),
        # White square, enemy queen left friend block 2
        ("0x000000000000000000000000000000006000001d000000000000000000000000", "0x1f", False),
        # White square, enemy queen left enemy block
        ("0x000000000000000000000000000000006900000d000000000000000000000000", "0x1f", False),
        # White square, enemy queen left enemy block 2
        ("0x000000000000000000000000000000006a00000d000000000000000000000000", "0x1f", False),
        # White square, check overflow
        ("0x0000000000000000000000000000000000000006d00000000000000000000000", "0x18", False),

        # White square, enemy bishop diagonal up-right far
        ("0xa000000000000000000000000000000000000000000000000000000000000005", "0x00", True),
        # White square, enemy queen diagonal up-right far
        ("0xd000000000000000000000000000000000000000000000000000000000000005", "0x00", True),
        # White square, enemy pawn diagonal up-right near
        ("0x0000000000000000000000000000000000000000000000000000009000000005", "0x00", True),
        # White square, enemy bishop diagonal up-right near
        ("0x000000000000000000000000000000000000000000000000000000a000000005", "0x00", True),
        # White square, enemy queen diagonal up-right near
        ("0x000000000000000000000000000000000000000000000000000000d000000005", "0x00", True),
        # White square, enemy pawn diagonal up-right far
        ("0x0000000000000000000000000000000000000000000009000000000000000005", "0x00", False),
        # White square, enemy bishop diagonal up-right off 1
        ("0x00000000000000000000000000000000000000000000000000000a0000000005", "0x00", False),
        # White square, enemy bishop diagonal up-right off 2
        ("0x0000000000000000000000000000000000000000000000a00000000000000005", "0x00", False),
        # White square, enemy bishop diagonal up-right friend block
        ("0xa000000000000000000000000000000000000000000001000000000000000005", "0x00", False),
        # White square, enemy bishop diagonal up-right enemy block
        ("0xa00000000000000000000000000000000000000000000000000000b000000005", "0x00", False),
         # Black square, enemy pawn diagonal up-right near
        ("0x000000000000000000000000000000000000000000000000000000100000000e", "0x00", False),
        # White square, enemy bishop diagonal up-right overflow
        ("0x00000000000000000000000000000000000000000000000a0000000060000000", "0x07", False),

        # White square, enemy bishop diagonal up-left far
        ("0x0000000a00000000000000000000000000000000000000000000000060000000", "0x07", True),
        # White square, enemy queen diagonal up-left far
        ("0x0000000d00000000000000000000000000000000000000000000000060000000", "0x07", True),
        # White square, enemy pawn diagonal up-left near
        ("0x0000000000000000000000000000000000000000000000000900000060000000", "0x07", True),
        # White square, enemy bishop diagonal up-left near
        ("0x0000000000000000000000000000000000000000000000000a00000060000000", "0x07", True),
        # White square, enemy queen diagonal up-left near
        ("0x0000000000000000000000000000000000000000000000000d00000060000000", "0x07", True),
        # White square, enemy pawn diagonal up-left far
        ("0x0000000000000000000000000000000000000000009000000000000060000000", "0x07", False),
        # White square, enemy bishop/queen diagonal up-left off 1
        ("0x00000000000000000000000000000000000000000d00000000a0000060000000", "0x07", False),
        # White square, enemy bishop diagonal up-left friend block
        ("0x0000000a00000000000000000000000000000000000000000100000060000000", "0x07", False),
        # White square, enemy bishop diagonal up-left enemy block
        ("0x0000000a00000000000000000000000000000000000000000b00000060000000", "0x07", False),
         # Black square, enemy pawn diagonal up-left near
        ("0x00000000000000000000000000000000000000000000000001000000e0000000", "0x07", False),
        # White square, enemy bishop diagonal up-left overflow
        ("0x000000000000000000000000000000000000000000000000a000000600000000", "0x08", False),














        # Black square, enemy bishop diagonal down-right far
        ("0x0000000e00000000000000000000000000000000000000000000000020000000", "0x38", True),
        # Black square, enemy queen diagonal down-right far
        ("0x0000000e00000000000000000000000000000000000000000000000050000000", "0x38", True),
        # Black square, enemy pawn diagonal down-right near
        ("0x0000000e00000010000000000000000000000000000000000000000000000000", "0x38", True),
        # Black square, enemy bishop diagonal down-right near
        ("0x0000000e00000020000000000000000000000000000000000000000000000000", "0x38", True),
        # Black square, enemy queen diagonal down-right near
        ("0x0000000e00000050000000000000000000000000000000000000000000000000", "0x38", True),
        # Black square, enemy pawn diagonal down-right far
        ("0x0000000e00000000000001000000000000000000000000000000000000000000", "0x38", False),
        # Black square, enemy bishop diagonal down-right off 1
        ("0x0000000e00000000000000200000000000000000000000000000000000000000", "0x38", False),
        # Black square, enemy bishop diagonal down-right off 2
        ("0x0000000e00000200000000000000000000000000000000000000000000000000", "0x38", False),
        # Black square, enemy bishop diagonal down-right friend block
        ("0x0000000e00000090000002000000000000000000000000000000000000000000", "0x38", False),
        # Black square, enemy bishop diagonal down-right enemy block
        ("0x0000000e00000030000002000000000000000000000000000000000000000000", "0x38", False),
        # White square, enemy pawn diagonal down-right near
        ("0x0000000600000090000000000000000000000000000000000000000000000000", "0x38", False),
        # Black square, enemy bishop diagonal down-right overflow
        ("0x00000000e0000000000000000000000200000000000000000000000000000000", "0x37", False),

        # Black square, enemy bishop diagonal down-left far
        ("0xe000000000000000000000000000000000000000000000000000000000000002", "0x3f", True),
        # Black square, enemy queen diagonal down-left far
        ("0xe000000000000000000000000000000000000000000000000000000000000005", "0x3f", True),
        # Black square, enemy pawn diagonal down-left near
        ("0xe000000001000000000000000000000000000000000000000000000000000000", "0x3f", True),
        # Black square, enemy bishop diagonal down-left near
        ("0xe000000002000000000000000000000000000000000000000000000000000000", "0x3f", True),
        # Black square, enemy queen diagonal down-left near
        ("0xe000000005000000000000000000000000000000000000000000000000000000", "0x3f", True),
        # Black square, enemy pawn diagonal down-left far
        ("0xe000000000000000001000000000000000000000000000000000000000000000", "0x3f", False),
        # Black square, enemy bishop/queen diagonal down-left off 1
        ("0xe000000000500000020000000000000000000000000000000000000000000000", "0x3f", False),
        # Black square, enemy bishop diagonal down-left friend block
        ("0xe000000009000000002000000000000000000000000000000000000000000000", "0x3f", False),
        # Black square, enemy bishop diagonal down-left enemy block
        ("0xe000000003000000002000000000000000000000000000000000000000000000", "0x3f", False),
        # White square, enemy pawn diagonal down-left near
        ("0x6000000009000000000000000000000000000000000000000000000000000000", "0x3f", False),
        # Black square, enemy bishop diagonal down-left overflow
        ("0x0000000e00000000200000000000000000000000000000000000000000000000", "0x38", False),
        
    ]

@pytest.mark.parametrize("gameState,piece_position,expected_outcome", TestCases)
def test_piece_at_pos(chess_contract, gameState, piece_position, expected_outcome):
    assert chess_contract.pieceUnderAttack(gameState, piece_position) == expected_outcome
