from random import shuffle, randrange

class IOHandler():
    def __init__(self, input_function=None, output_function=None):
        self.input_function = (
            input if input_function is None
            else input_function
        )
        self.do_output = (
            print if output_function is None
            else output_function
        )

    def do_input(self, prompt):
        return self.input_function(self, prompt)

    def get_next_mocked_input(self, prompt):
        result = self.mocked_input[self.i_mocked_input]
        self.i_mocked_input += 1
        return result

    def write_to_list(self, message):
        self.output_log.append(message)

    @classmethod
    def using_mocked_input(cls, input_sequence):
        result = cls(
            input_function = cls.get_next_mocked_input,
            output_function = cls.write_to_list,
        )
        result.mocked_input = list(input_sequence)
        result.i_mocked_input = 0
        result.output_log = []
        return result


class Game():
    GAME_CLOSE_MESSAGE = "Goodbye!"

    def __init__(self, io_handler=None):
        # `input_source_function` should be a generator with the following behaviour:
        #   Arguments: 1 string, representing the prompt to be shown to the input source
        #   Return value: 1 string, representing the response from the input source
        # Input sources might be human users, mocked human users, API callers, frontends, etc.
        # `output_source_function` should be a function which processes output.
        #    Arguments: 1 string, representing the outputs to frontend GUI / CLI / etc.
        self._io_handler = (
            IOHandler() if io_handler is None else io_handler
        )
        # self._input = self._io_handler.do_input
        self._output = self._io_handler.do_output

    def _input(self, prompt):
        return self._io_handler.do_input(prompt)

    # @staticmethod
    # def make_static_input_source(iterable):
    #     for item in iterable:
    #         yield item
    #     return

    def create_players(self, human_playing=False):
        self.players = [Player() for __ in range(4)]
        if human_playing:
            self.players[0].is_human = True

    def deal_cards(self):
        deck = Card.make_fresh_deck(shuffled=True)
        for i in range(4):
            self.players[i].hand.extend(
                deck[13 * i : 13 * (i + 1)]
            )

    def play(self):
        self.players = [Player() for __ in range(4)]
        gamemode = self.query_user_for_option(
            """Would you like to:
* play in this game (P / Play);
* have bots play each other (B / Bots);
* or cancel and quit the game (Q / Quit)?
> """,
            "Response not recognised; please answer P / Play, B / Bots, or Q / Quit.\n> ",
            ("b", "p", "q"),
            lambda r: "" if len(r) == 0 else r[0].lower()
        )
        if gamemode == "q":
            self._output(self.GAME_CLOSE_MESSAGE)
            return
        self.create_players(gamemode == "p")
        self.deal_cards()

    def query_user_for_option(self,
            initial_prompt, subsequent_prompt, options, answer_filter=None, should_filter_response=True
        ):
        if answer_filter is None:
            answer_filter = lambda x: x
        prompt = initial_prompt
        while True:
            print(self._input)
            raw_response = self._input(prompt)
            filtered_response = answer_filter(raw_response)
            if filtered_response in options:
                return filtered_response if should_filter_response else raw_response
            prompt = subsequent_prompt

class Player():
    def __init__(self, is_human=False):
        self.is_human = is_human
        self.hand = []

# (Phase Two) Ability to play cards
#     def play_card_from_hand(self):
#         if self.is_human:
#             i_card_to_play = self.hand.index(query_user_for_option(
#                 f"""You have these cards in your hand: {self.report_cards_in_hand()}\n
# Which card would you like to play?\n> """,
#                 "You don't have that card, please select another.\n> ",
#                 [str(card) for card in self.hand],
#                 lambda r: r.upper()
#             ))
#         else:
#             # Bot functionality will go here
#             i_card_to_play = randrange(len(self.hand))
#         return self.hand.pop(i_card_to_play)

    def report_cards_in_hand(self, print_this=False):
        msg = ", ".join(str(card) for card in self.hand)
        if print_this:
            print(msg)
        else:
            return(msg)


class Card():
    RANKS = tuple("A23456789TJQK")
    SPADES, HEARTS, DIAMONDS, CLUBS = 'S', 'H', 'D', 'C'
    SUITS = (SPADES, HEARTS, DIAMONDS, CLUBS)

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    # def find_card_strength(self, leading_suit):
    #     # RULES (Phase 3): Tricks are won by the player with the highest card of the leading suit.
    #     pass

    @classmethod
    def make_fresh_deck(cls, shuffled=False):
        deck = [
            cls(rank, suit)
            for rank in cls.RANKS
            for suit in cls.SUITS
        ]
        if shuffled:
            shuffle(deck)
        return deck

if __name__ == "__main__":
    game = Game()
    game.play()

def make_generator_from(iterable):
    for item in iterable:
        yield item
    return

