from itertools import combinations
from collections import Counter

# Valores de las cartas, asumí A como 1.
values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

# Palos o colores en inglés. Corazónes, Diamantes, Picas y Tréboles.
suits = ['H','D','S','C']

# Itera las manos.
deck = [(v,s) for v in values for s in suits]

# Agrega los Jocker.
deck.append(("JOKER","J1"))
deck.append(("JOKER","J2"))

red_suits = ['H','D']

def has_two_red_pairs(hand):
    
    # ignorar manos con joker
    for card in hand:
        if card[0] == "JOKER":
            return False

    # contar valores
    values_in_hand = [v for v,s in hand]
    count = Counter(values_in_hand)

    # buscar pares
    pairs = [v for v,c in count.items() if c == 2]

    if len(pairs) != 2:
        return False

    # verificar que los pares sean rojos
    for p in pairs:
        pair_cards = [card for card in hand if card[0] == p]

        if not all(card[1] in red_suits for card in pair_cards):
            return False

    return True


valid_hands = []

for hand in combinations(deck,5):
    if has_two_red_pairs(hand):
        valid_hands.append(hand)

# Hice un Bloc de notas para guardar los resultados porque noc aben en impresión.
print("Total de manos:", len(valid_hands))
with open("manos.txt","w") as f:
    for h in valid_hands:
        f.write(str(h)+"\n")

# Aquí solo muestra algunas porque son un chingo. Consulten el bloc de notas.
for h in valid_hands[:20]:
    print(h)

input()