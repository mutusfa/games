"""Module to create and parse tichu game logs."""

import json

from . import constructed_constants


class Parser():
    def __init__(self, deck=None, *args, **kwargs):
        self.deck = sorted(deck)
        self._str_deck = [str(card) for card in self.deck]
        super().__init__(*args, **kwargs)

    def parse(self, hands, *args, **kwargs):
        for hand_id, hand in enumerate(hands[:]):
            for card_id, card in enumerate(hand):
               hands[hand_id][card_id] = self.deck[self._str_deck.index(card)]
        return hands


class SteinacherParser(Parser):
    def __init__(
            self,
            steinacher_game=None,
            card_string_key='card_string',
            *args,
            **kwargs):
        self.game = steinacher_game
        self.translation_table = {
            "Hu" : "D", "Ma" : "1", "Ph" : "P", "Dr" : "R",
            "S" : "S", "R" : "T", "B" : "P", "G" : "E",
            "A" : "A", "K" : "K", "D" : "Q", "J" : "J",
            "SB" : "SJ", "RB" : "RJ", "BB" : "BJ", "GB" : "GJ",
            "S10" : "S0", "R10": "R0", "B10": "B0", "G10" : "E0",
            }
        self.card_string_key = card_string_key
        self.states_key = 'views'
        self.hands_key = 'hand'
        super().__init__(deck=constructed_constants.DECK, *args, **kwargs)

    def _card_string_card(self, card_id=None, value=None):
            """A DRY way to get or set value of a card card_string."""
            if card_id is None:
                return self.game[self.card_string_key]

            if value is not None:
                self.game[self.card_string_key][card_id] = value
                return

            value = self.game[self.card_string_key][card_id]
            return value

    def parse_hands(self, *args, **kwargs):
        for state_id, state in enumerate(self.game[self.states_key]):
            hands = super().parse(state[self.hands_key], *args, **kwargs)
            self.game[self.states_key][state_id][self.hands_key] = hands

    def pre_translate_card_string(self):
        temp = self.game[self.card_string_key]
        self.game[self.card_string_key] = {}
        for card_id, card_string in temp.items():
            self.game[self.card_string_key][int(card_id)] = card_string

    def replace_cards(self):
        """Replaces card ids from steinacher with their string."""
        for state_id, state in enumerate(self.game[self.states_key]):
            for hand_id, hand in enumerate(state[self.hands_key]):
                temp = hand
                self.game[
                    self.states_key][state_id][self.hands_key][hand_id] = []
                for card_id in temp:
                    self.game[
                        self.states_key][
                        state_id][
                        self.hands_key][
                        hand_id
                        ].append(self._card_string_card(card_id))

    def translate_card_string(self):
        def translate(card_string):
            return self.translation_table.get(card_string, card_string)

        #translate specials
        for card_id, card_string in self._card_string_card().items():
            self._card_string_card(card_id, translate(card_string))

        #translate simples
        for card_id, card_string in self._card_string_card().items():
            try:
                colour, strength = card_string
            except ValueError:
                pass
            else:
                self._card_string_card(card_id, translate(strength) + translate(colour))
