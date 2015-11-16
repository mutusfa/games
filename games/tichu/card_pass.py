import random

from . import (
        cards,
        constants,
        constructed_constants,
        )

class Hand(list):
    def simple(self):
        return Hand([card for card in self if card.strength])

    def __str__(self):
        as_list = []
        try:
            for phase in self:  #pre/post grand tichu
                as_list.append(str([str(card) for card in phase]))
        except TypeError:
            as_list.append(str([str(card) for card in self]))
        return "\n".join(as_list)


def parse_hands(hands_):
    raise NotImplementedError()


def generate_hands(deck=None, no_players=None, grand_tichu=None):
    if deck is None:
        deck = constructed_constants.DECK.copy()

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
        for hand_id, hand in enumerate(hands):
            hands[hand_id] = hand[:grand_tichu], hand[grand_tichu:]

        hands = [(sorted(hand[0]), sorted(hand[1])) for hand in hands]
    else:
        hands = [sorted(hand) for hand in hands]

    for hand_id, hand in enumerate(hands):
        hands[hand_id] = Hand(hand)

    return hands


def print_hands(hands):
    for hand in hands:
        print(hand)


def print_combinations(combinations):
    for comb_type, combs in combinations.items():
        if len(combs) > 0:
            print(comb_type)
            for comb in combs:
                if len(comb) > 0:
                    print([str(card) for card in comb])


def find_combinations(hand):
    combs = {}
    print("\n" + str(hand) + "\n")
    combs['same_kind'] = find_same_kind(hand.simple())
    combs['singletons'] = combs['same_kind'][1]
    combs['pairs'] = combs['same_kind'][2]
    combs['triples'] = combs['same_kind'][3]
    combs['bombs'] = combs['same_kind'][4]
    combs['rows']=find_rows(hand)
    for type_id in combs['rows'].keys():
        combs['rows_%s' % type_id] = combs['rows'][type_id]
    del combs['rows']
    del combs['same_kind']
    return combs


def find_same_kind(hand):
    """Find combinations regarding same kind.

    Expects ordered hand without special cards.

    (readable representation)
    ["2L", "3B", "3L", "3R", "3G", "5R", "8L", "8R", "8G", "KB", "KL", ...]
        ==> {
            1: [("2L",), ("5R",), ...],
            2: [("KB", "KL"), ...],
            3: [("8L", "8R", "8G"), ...],
            4: [("3B", "3L", "3R", "3G")],
            }
    """
    same_kind_combs = {}
    for i in range(5):
        same_kind_combs[i] = []

    kind_count = 1
    for card_id, card in enumerate(hand[:-1]):
        if card.strength == hand[card_id + 1].strength:
            kind_count += 1  #next card is of the same kind
        else:
            same_kind_combs[kind_count].append(
                hand[card_id - kind_count + 1: card_id + 1]
                )
            kind_count = 1
    same_kind_combs[kind_count].append(hand[-kind_count:])  #append last group
    return same_kind_combs


def find_complex_combs(same_kind_combs):
    """Finds combinations gained by mixing combinations of same kind.

    Combinations of same kind must come in ascending order.

    (readable representation)
    {
        1: [('2R',), ('4G',),],
        2: [('3G', '3L'), ('5R', '5B'), ('6G', '6B'), ('7R','7B'),],
        3: [('KR', 'KG', 'KB'),],
        4: [],
    }
        ===>
        {
            'straight_pairs': {
                2: [(('5R', '5B'), ('6G', '6B')), (('6G', '6B'), ('7R', '7B')),],
                3: [(('5R', '5B'), ('6G', '6B'), ('7R', '7B')),],
            },
            'full_houses': [(('3G', '3L'), ('KR', 'KG', 'KB')),],
        }

    Finds:
        Full-house
        straight pairs
    """
    raise NotImplementedError()


def find_rows(hand, row_length=None):
    """Finds separate rows with and without pheonix.

    Does not add pheonix to the end of a row if doing so would not
    lengthen the row with simple cards.

    Expects ordered hand with special cards in the beggining.

    At the moment fails to recognise duplicate rows, ie, when the same row
    appears twice.
    """
    if row_length is None:
        row_length = constants.MIN_ROW_LENGTH

    pheonix = None
    for card in hand:
        if card.strength: break
        if card.kind == "P":
            pheonix = card
            break

    hand = hand.simple()

    rows = {'simple':[], 'pheonix':[], 'bomb':[]}

    row = Hand()
    hand_size = len(hand)
    for card_id, card in enumerate(hand):
        #strip out cards of the same strength
        if (
            (card_id + 1 < hand_size) and
            (card.strength == hand[card_id + 1].strength)
            ):
            continue
        row.append(card)

        if not (
            (card_id + 1 < hand_size) and
            (card.strength + 1 == hand[card_id + 1].strength)
            ):
                rows['simple'].append(row)
                row = Hand()

    if pheonix:
        for row_id, row in enumerate(rows['simple'][:-1]):
            if (
                #if two rows lack only 1 card to connect
                row[len(row) - 1].strength + 2 ==
                rows['simple'][row_id + 1][0].strength
            ):
                rows['pheonix'].append(tuple(row + [pheonix] + rows['simple'][row_id + 1]))

    if row_length:
        for type_id, single_type_rows in dict(rows).items():
            rows[type_id] = []
            for row_id, row in enumerate(single_type_rows):
                if len(row) >= row_length:
                    rows[type_id].append(row)
                    for card_id, card in enumerate(row[:-1]):
                        try:
                            if card.colour != row[card_id + 1].colour:
                                break
                        except AttributeError:
                            break
                    else:  #all cards in row are of the same colour
                        rows['bomb'].append(row)
    return rows


def main():
    hands = generate_hands(grand_tichu=0)
    print_hands(hands)
    print_combinations(find_combinations(hands[0]))

if __name__ == "__main__":
    main()
