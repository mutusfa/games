from . import (
    cards,
    constants,
    )

DECK = []
for colour in constants.COLOURS:
    DECK.append(cards.SimpleCard(colour=colour, strength=2))
    DECK.append(cards.SimpleCard(colour=colour, strength=3))
    DECK.append(cards.SimpleCard(colour=colour, strength=4))
    DECK.append(cards.SimpleCard(colour=colour, strength=5, value=5))
    DECK.append(cards.SimpleCard(colour=colour, strength=6))
    DECK.append(cards.SimpleCard(colour=colour, strength=7))
    DECK.append(cards.SimpleCard(colour=colour, strength=8))
    DECK.append(cards.SimpleCard(colour=colour, strength=9))
    DECK.append(cards.SimpleCard(colour=colour, strength=10,
        kind="0", value=10))
    DECK.append(cards.SimpleCard(colour=colour, strength=11,
        kind="J", verbose="Jack"))
    DECK.append(cards.SimpleCard(colour=colour, strength=12,
        kind="Q", verbose="Queen"))
    DECK.append(cards.SimpleCard(colour=colour, strength=13,
        kind="K", verbose="King", value=10))
    DECK.append(cards.SimpleCard(colour=colour, strength=14,
        kind="A", verbose="Ace"))

DECK.extend([
    cards.MahJongg(),
    cards.Dragon(),
    cards.Pheonix(),
    cards.Dog(),
])

DECK.sort()
