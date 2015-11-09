import random

from . import (
        cards,
        constants,
        constructed_constants,
        )

def generate_hands(deck=None, no_players=None):
    if not deck:
        deck = constructed_constants.DECK

    if not no_players:
        no_players = constants.NO_PLAYERS

    def pick_card(deck=deck):
        """Draws a card from the deck without replacement."""
        return deck.pop(random.randint(0, len(deck) - 1))

    hands = [[] for i in range(no_players)]
    while deck:
        for player in range(no_players):
            hands[player].append(pick_card())

    hands = [sorted(hand) for hand in hands]

    return hands


def print_hands(hands):
    for hand in hands:
        print([str(card) for card in hand])


def main():
    hands = generate_hands()
    print_hands(hands)


if __name__ == "__main__":
    main()
