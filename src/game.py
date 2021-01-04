import random
from .player import Player
import src.ui as UI


full_deck = [(1, '🃁'), (1, '🂡'), (1, '🂱'), (1, '🃑'),
             (2, '🃂'), (2, '🂢'), (2, '🂲'), (2, '🃒'),
             (3, '🃃'), (3, '🂣'), (3, '🂳'), (3, '🃓'),
             (4, '🃄'), (4, '🂤'), (4, '🂴'), (4, '🃔'),
             (5, '🃅'), (5, '🂥'), (5, '🂵'), (5, '🃕'),
             (6, '🃆'), (6, '🂦'), (6, '🂶'), (6, '🃖'),
             (7, '🃇'), (7, '🂧'), (7, '🂷'), (7, '🃗'),
             (8, '🃈'), (8, '🂨'), (8, '🂸'), (8, '🃘'),
             (9, '🃉'), (9, '🂩'), (9, '🂹'), (9, '🃙'),
             (10, '🃊'), (10, '🂪'), (10, '🂺'), (10, '🃚'),
             (10, '🃋'), (10, '🂫'), (10, '🂻'), (10, '🃛'),
             (10, '🃍'), (10, '🂭'), (10, '🂽'), (10, '🃝'),
             (10, '🃎'), (10, '🂮'), (10, '🂾'), (10, '🃞')]


class Game:
    ''' Hosts a game of blackjack.'''

    def __init__(self, name):
        self.players = [Player(name), Player('Dealer')]

    def __repr__(self):
        return UI.scoreboard(self.players)

    def start_round(self):
        self.deck = full_deck[:]
        for index, player in enumerate(self.players):
            player.clear_hand()
            self.give_card(index)

    def give_card(self, player_id):
        player = self.players[player_id]
        player.add_card(
            self.deck.pop(random.randint(0, len(self.deck) - 1))
        )
        return player.can_buy()

    def dealer_needs_buy(self):
        return (self.players[0].hand_value() < 21 and
                not self.players[0].lost() and
                not self.players[1].lost() and
                self.players[0].hand_value() >= self.players[1].hand_value()
                )

    def dealer_won(self):
        if (
            self.players[0].lost() or (
                not self.players[1].lost() and
                self.players[0].hand_value() < self.players[1].hand_value()
            )
        ):
            self.players[1].wins += 1
            return True

        self.players[0].wins += 1
        return False
