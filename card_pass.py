import random

from . import (
        cards,
        constants,
        constructed_constants,
        )

def generate_hands(deck=None, no_players=None, grand_tichu=None):
    if deck is None:
        deck = constructed_constants.DECK

    if no_players is None:
        no_players = constants.NO_PLAYERS

    if grand_tichu is None:
        grand_tichu = constants.GRAND_TICHU

    def pick_card(deck=deck):
        """Draws a card from the deck without replacement."""
        return deck.pop(random.randint(0, len(deck) - 1))

    hands = [[] for i in range(no_players)]
    while deck:
        for player in range(no_players):
            hands[player].append(pick_card())

    if grand_tichu:
        temp = hands
        hands = []
        for hand in temp:
            hands.append((hand[:grand_tichu], hand[grand_tichu:]))
        del temp

        hands = [(sorted(hand[0]), sorted(hand[1])) for hand in hands]
    else:
        hands = [sorted(hand) for hand in hands]

    return hands


def print_hands(hands):
    for hand in hands:
        try:
            for phase in hand:  #pre/post grand tichu
                print([str(card) for card in phase])
        except TypeError:
            print([str(card) for card in hand])
        else:
            print()


def main():
    hands = generate_hands(grand_tichu=0)
    print_hands(hands)


if __name__ == "__main__":
    main()
