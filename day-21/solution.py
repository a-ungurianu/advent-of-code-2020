from collections import defaultdict
from functools import reduce

INPUT = "input.txt"


def parse_food(line):
    ingredients, rest = line.split(" (")
    ingredients = ingredients.split(" ")
    alergens = rest[9:-1]
    alergens = alergens.split(", ")

    return (set(ingredients), set(alergens))


with open(INPUT, "r") as f:
    FOODS = [parse_food(line.strip()) for line in f.readlines()]

alergens_to_food = defaultdict(list)

INGREDIENTS = reduce(lambda a, b: a.union(b), (food[0] for food in FOODS))

for food in FOODS:
    ingredients, alergens = food

    for alergen in alergens:
        alergens_to_food[alergen].append(ingredients)

alergen_matches = []


def resolve_pair(pair):
    alergen, ingredient = pair
    alergen_matches.append(pair)
    del alergens_to_food[alergen]
    for food in FOODS:
        ingredients, _ = food
        ingredients.discard(ingredient)


while len(alergens_to_food) > 0:
    for alergen, ingredient_sets in alergens_to_food.items():
        intersection = reduce(lambda a, b: a.intersection(b), ingredient_sets)
        if len(intersection) == 1:
            pair = (alergen, next(iter(intersection)))
            break
    resolve_pair(pair)

print(alergen_matches)
print(INGREDIENTS)

unused_ingredients = INGREDIENTS.difference(
    set(match[1] for match in alergen_matches))


unused_total = 0

for food in FOODS:
    ingredients, _ = food
    unused_total += len(unused_ingredients.intersection(ingredients))

print(unused_total)

print(",".join(match[1] for match in sorted(alergen_matches)))
