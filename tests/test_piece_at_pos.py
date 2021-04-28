import pytest
from brownie import Chess, accounts, web3, reverts

@pytest.fixture
def chess_contract():
    return accounts[0].deploy(Chess)

@pytest.mark.parametrize("game_state,piece_position,expected", 
    [
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x00", 4),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x01", 3),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x02", 2),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x03", 5),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x04", 6),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x08", 1),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x10", 0),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x30", 9),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x38", 12),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x39", 11),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x3A", 10),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x3B", 13),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x3C", 14),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x3D", 10),
        ("0xcbaedabc99999999000000000000000000000000000000001111111143265234", "0x3F", 12),
    ])
def test_piece_at_pos(chess_contract, game_state, piece_position, expected):
    assert chess_contract.pieceAtPosition(game_state, piece_position) == expected