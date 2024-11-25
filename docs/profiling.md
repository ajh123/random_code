# `sam_utilities.main.display_list`:

```python
def display_list(list: List[str]) -> str:
    out = "" # 1 instruction, create new string.
    for ele in list: # 3 instructions, create new variable, retreive element from list, increment internal pointer.
        out += f"{ele}, " # 3 instructions, create new string, retreive element from memory, append to another string.
    return out # 1 instruction
```

This algorithimn's time complexity is `O(n)`. This is becuase user input is a list and there is a for loop which iterates it, which results in linear time.

This algorithimn's space complexity can't be `O(1)` even though the number of variables that exist are consistant and don't depend on input, the input list still exists in memory so the space complexity is `O(n)` again.

For every element in the input list there are 6 instructions performed.

Furthermore results from using `timeit` proofs that the more elements that are in the list will mean the program will take longer.

```
7.050001295283437e-05 seconds for 10 elements
0.0007270000060088933 seconds for 100 elements
0.010179400007473305 seconds for 1000 elements
0.9704911000153515 seconds for 100000 elements
```

```
7.879998884163797e-05 seconds for 10 elements
0.0007431000121869147 seconds for 100 elements
0.011871900002006441 seconds for 1000 elements
1.0710788000142202 seconds for 100000 elements
```

# Greedy kanpsack:

```python
def greedy(knapsack: Knapsack):
    ratios = [] # 1 instruction
    for item in items: # 3 instructions, create new variable, retreive element from list, increment internal pointer.
        ratios.append(item.get_value()/item.get_weight()) # 4 instructions.
    
    w = 0 # 1 instruction
    v = 0 # 1 instruction
    for _ in range(len(ratios)): # Once 6 instructions (create a variable, iterate a list, increment a variable, create a new list, more iteration, append a number to the new list ) + 3 instructions, create new variable, retreive element from list, increment internal pointer.
        best = max(ratios) # 8 create a result variable, retreive 1 element, create a pointer variable, increment the pointer, retreive tha variable, use that pointer to index a list, compare the two elements, update the result. + 1 once done assign result to a new variable.
        index = ratios.index(best) # 8 create a result variable, retreive 1 element, create a pointer variable, increment the pointer, retreive tha variable, use that pointer to index a list, compare the two elements, update the result. + 1 once done assign result to a new variable.
        ratios[index] = 0 # 3 retreive index variable, retreive pointer to element in ratios, assign 0 to that pointer.
        if w + items[index].get_weight() < knapsack.get_max_weight():
            v += items[index].get_value() # 6 = create new variable, retreive index, retreive items, index the items list, retreive value variable, assign to variable.
            w += items[index].get_weight() # 6 = create new variable, retreive index, retreive items, index the items list, retreive weight variable, assign to variable.
            knapsack.put(items[index]) # get pointer to knapsack, retreive index, retrieve items, 
```
