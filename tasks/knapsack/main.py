from sam_utilities import validated_input
from typing import List


class Item:
    def __init__(self, name: str, value: int, weight):
        self._name = name
        self._value = value
        self._weight = weight
    
    def __str__(self):
        return f"Item(name={self._name}, value={self._value}, weight={self._weight})"

    def get_name(self):
        return self._name
    
    def get_value(self):
        return self._value

    def get_weight(self):
        return self._weight


class Knapsack:
    def __init__(self, max_weight: int):
        self._max_weight = max_weight
        self._items: List[Item] = []
    
    def get_max_weight(self):
        return self._max_weight
    
    def get_current_weight(self):
        total = 0
        for item in self._items:
            total += item.get_weight()
        return total

    def get_items(self):
        return self._items

    def put(self, item: Item):
        if not self.get_current_weight() > self.get_max_weight():
            self._items.append(item)
        else:
            raise ValueError(f"The item {item.get_name()} is too big for this Knapsack! ({item.get_weight()} + {self.get_current_weight()} > {self.get_max_weight()})")

def log(msg: str):
    with open("log.txt", "a") as f:
        f.write(f"{msg}\n")


items: List[Item] = []

with open("items.csv") as f:
    lines = f.readlines()
    for line in lines:
        data = line.split(",")
        item = Item(data[0], int(data[1]), int(data[2]))
        items.append(item)

size = validated_input(int, "How big do you want you knapsack to be?")
print("Running calculations, please wait ...")

greedy_knapsack = Knapsack(size)
exhaustive_knapsack = Knapsack(size)

def greedy(knapsack: Knapsack):
    ratios = []
    for item in items:
        ratios.append(item.get_value()/item.get_weight())
    
    w = 0
    v = 0
    for _ in range(len(ratios)):
        best = max(ratios)
        index = ratios.index(best)
        # ratios.remove(best) # BAD: changes the indices of everything! Just clear it instead.
        ratios[index] = 0
        if w + items[index].get_weight() < knapsack.get_max_weight():
            v += items[index].get_value()
            w += items[index].get_weight()
            knapsack.put(items[index])

greedy(greedy_knapsack)

def exhaustive(kanpsack: Knapsack):
    all_combos: List[List[Item | None]] = [[]]
    max_v = 0
    for i in range(len(items)):
        for j in range(len(all_combos)):
            subset = list(all_combos[j])
            subset.append(items[i])
            all_combos.append(subset)
    for combo in all_combos:
        cur_v = 0
        cur_w = 0
        for item in combo:
            cur_v = item.get_value()
            cur_w = item.get_weight()
        if len(combo) > 0:
            pass
        if cur_w > kanpsack.get_max_weight():
            pass
        else:
            if max_v < cur_v:
                max_v = cur_v
    return all_combos

all_combos = exhaustive(exhaustive_knapsack)

log("The greedy knapsack now contains:")
for item in greedy_knapsack.get_items():
    log(f"- {item}")

log("The exhaustive knapsack could contain:")
for combo in all_combos:
    log("===")
    for item in combo:
        log(f"- {item}")