import random

HEARTS = "H"
DIAMONDS = "D"
SPADES = "S"
CLUBS = "C"

SUITS = (SPADES, HEARTS, DIAMONDS, CLUBS)

RANKS = tuple("A23456789TJQK")

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Player():
    def __init__(self, starting_cards=None):
        self.hand = []
        if starting_cards is not None:
            self.hand.extend(starting_cards)

    def print_hand(self):
        if len(self.hand) == 0:
            msg = f"Player's hand is empty"
        else:
            msg = f"Player's hand: {', '.join(str(card) for card in self.hand)}"
        print(msg)

def set_up_game():
    # Returns a list of four Player instances with 13 randomly distributed cards each.
    cards = [
        Card(suit, rank) for suit in SUITS for rank in RANKS
    ]
    random.shuffle(cards)
    return [
        Player(starting_cards = cards[13 * i:13 * i + 13])
        for i in range(4)
    ]
