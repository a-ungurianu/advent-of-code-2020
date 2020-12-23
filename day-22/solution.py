from queue import Queue
from itertools import count

from typing import List


def regular_combat(deck1, deck2):
    while deck1 and deck2:
        p1, p2 = deck1.pop(0), deck2.pop(0)

        if p1 > p2:
            deck1.append(p1)
            deck1.append(p2)
        else:
            deck2.append(p2)
            deck2.append(p1)

    return deck1, deck2


def recursive_combat(deck1, deck2):
    ROUNDS = set()

    while deck1 and deck2 and (tuple(deck1), tuple(deck2)) not in ROUNDS:
        ROUNDS.add((tuple(deck1), tuple(deck2)))
        p1, p2 = deck1.pop(0), deck2.pop(0)

        if len(deck1) >= p1 and len(deck2) >= p2:
            rec1, rec2 = recursive_combat(deck1[:p1], deck2[:p2])

            if rec1:
                deck1.append(p1)
                deck1.append(p2)
            elif rec2:
                deck2.append(p2)
                deck2.append(p1)
            else:
                assert False, "Bad error"

        elif p1 > p2:
            deck1.append(p1)
            deck1.append(p2)
        else:
            deck2.append(p2)
            deck2.append(p1)

    if (tuple(deck1), tuple(deck2)) in ROUNDS:
        print("Player 1 wins")

    return deck1, deck2


INPUT = "input.txt"

with open(INPUT, "r") as f:
    f.readline()

    PLAYER1_DECK = []

    while (line := f.readline().strip()) != "":
        PLAYER1_DECK.append(int(line))

    f.readline()

    PLAYER2_DECK = []

    while (line := f.readline().strip()) != "":
        PLAYER2_DECK.append(int(line))


# final_deck1, final_deck2 = regular_combat(
#     list(PLAYER1_DECK), list(PLAYER2_DECK))
# winning_deck = final_deck1 if final_deck1 else final_deck2


# print(sum(idx * card for idx, card in zip(count(1), reversed(winning_deck))))


final_deck1, final_deck2 = recursive_combat(PLAYER1_DECK, PLAYER2_DECK)
winning_deck = final_deck1 if final_deck1 else final_deck2


print(sum(idx * card for idx, card in zip(count(1), reversed(final_deck1))))
print(sum(idx * card for idx, card in zip(count(1), reversed(final_deck2))))
