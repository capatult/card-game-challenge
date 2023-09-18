# pylint: skip-file

import pytest
from lib.main import *
from unittest.mock import Mock

# Phase One
# General concepts of cards, players and hands:
#   * Cards (Card class and 52 instances thereof?) can be shuffled and dealt to 4 Player objects
#   * Concept of a "hand" is created for a Player, with some way to print that in an appropriate fashion to the terminal

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

def test_display_cards_of_player():
    fake_io_handler = Mock()
    output_log = []
    fake_io_handler.send_output.side_effect = lambda x: output_log.append(x)
    game = Game(fake_io_handler)
    game.create_players()
    game.display_cards_of_player(0)
    assert output_log == [""]

# Phase Two
# Ability to play cards, 13 "tricks" making a full round:
#   * Some user interaction such that the user can choose what card to play from their own hand
#   * "Bot" hands to play a card, chosen randomly for now (restrictions on who can play what, and who leads, to come later)
#   * Forming of "tricks" - 4 cards, 1 from each player - kept and preserved such that they can belong to a player who won that trick, later on

# Phase Three
# Basic rules introduced:
#   * 2 Clubs owner goes first and plays that card first
#   * Players must follow suit, if possible
#   * Tricks are won by the player with the highest card of the leading suit (for now)
#   * Player who won the trick plays first card of next trick

# Phase Four
# Full rules implemented:
#   * Hearts can only be played if no card matching the leading suit is playable - counts as "Hearts are broken"
#   * Hearts can only lead once broken, or if hand only has Hearts in it
#   * Scoring and calculation of tricks, including 1 point per Heart and 13 points for Q Spades
#   * Points are displayed in the terminal at round end
#   * (optionally, since its absence won't take much away from the game) 3 cards are passed between players at the start of each round

# Bonus
# Begin adding some intelligent play to the "Bot" players e.g. (not necessarily in order):
#   * Try to avoid winning any tricks
#   * Throw away Q Spades if ever possible
#   * Don't lead something like Q Spades or high Hearts if possible
#   * ...

