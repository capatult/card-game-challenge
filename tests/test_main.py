# pylint: skip-file

from lib.main import *
from unittest.mock import Mock

# Phase One
# General concepts of cards, players and hands:
#     Cards (Card class and 52 instances thereof?) can be shuffled and dealt to 4 Player objects
#     Concept of a "hand" is created for a Player, with some way to print that in an appropriate fashion to the terminal

def test_create_players():
    game = Game()
    game.create_players()
    assert len(game.players) == 4
    assert all(isinstance(player, Player) for player in game.players)

def test_set_human_player():
    game_with_human = Game()
    game_with_human.create_players(human_playing = True)
    assert [
        player.is_human for player in game_with_human.players
    ] == [True, False, False, False]

def test_only_bots_created():
    bots_only_game = Game()
    bots_only_game.create_players(human_playing = False)
    assert all(not player.is_human for player in bots_only_game.players)

def test_full_deck_created():
    deck = Card.make_fresh_deck()
    assert len(deck) == 52
    assert all(isinstance(card, Card) for card in deck)

def test_deal_cards():
    game = Game()
    game.create_players()
    game.deal_cards()
    assert all(len(player.hand) == 13 for player in game.players)
    assert all(
        all(isinstance(card, Card) for card in player.hand)
        for player in game.players
    )

def test_report_cards():
    game = Game()
    game.create_players()
    game.deal_cards()
    report = game.players[0].report_cards_in_hand()
    assert len(report.split(", ")) == 13

def test_mock_input_and_output():
    fake_io_handler = Mock()
    fake_io_handler.fetch_input.return_value = "Q"
    output_log = []
    fake_io_handler.send_output.side_effect = lambda x: output_log.append(x)
    game = Game(fake_io_handler)
    game.play()
    assert output_log == [Game.GAME_CLOSE_MESSAGE]
