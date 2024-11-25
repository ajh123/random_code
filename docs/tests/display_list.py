from timeit import timeit

from sam_utilities import display_list

iterations = 100

list1 = list(range(0, 10))

total1 = timeit("display_list(list1)", number = iterations, globals=globals())
print(f"{total1} seconds for {len(list1)}")

list2 = list(range(0, 100))

total1 = timeit("display_list(list2)", number = iterations, globals=globals())
print(f"{total1} seconds for {len(list2)}")

list3 = list(range(0, 1000))

total1 = timeit("display_list(list3)", number = iterations, globals=globals())
print(f"{total1} seconds for {len(list3)}")

list4 = list(range(0, 100000))

total1 = timeit("display_list(list4)", number = iterations, globals=globals())
print(f"{total1} seconds for {len(list4)}")