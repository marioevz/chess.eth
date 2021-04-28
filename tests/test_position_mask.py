import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

@pytest.mark.parametrize("expected_mask,piece_position", 
    [
        ("0x00000000000000000000000000000000000F0000000000000000000000000000", "0x1c"),
        ("0x000000000000000000000000000000000000000000000000000000000000000F", "0x00"),
        ("0xF000000000000000000000000000000000000000000000000000000000000000", "0x3f"),
        ("0xF000000000000000000000000000000000000000000000000000000000000000", "0xff"),
    ])
def test_piece_at_pos(chess_contract, expected_mask, piece_position):
    assert chess_contract.getPositionMask(piece_position) == expected_mask
