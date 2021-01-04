import src.ui as UI


class Player:

    def __init__(self, name):
        self.name = name
        self.wins = 0

    def clear_hand(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def hand_value(self):
        value = 0
        has_ace = False
        for card in self.hand:
            value += card[0]
            if card[0] == 1:
                has_ace = True
        if value < 12 and has_ace:
            value += 10
        return value

    def show_hand(self):
        return UI.show_hand(self)

    def can_buy(self):
        return self.hand_value() < 21

    def lost(self):
        return self.hand_value() > 21
