from typing import List

def dual_sort(list1: List, list2: List):
    if len(list1) > len(list2):
        raise ValueError("Legnth of `list1` is greater then length of `list2`.")
    
    # fully_sorted = False

    # while not fully_sorted:
    #     last_index = 0
    #     for i in range(0, len(list1)):
    #         if list1[i] < list1[last_index]:
    #             swap(list1, last_index, i)
    #             swap(list2, last_index, i)
    #         last_index = i
        
    #     last_index = 0
    #     for i in range(0, len(list1)):
    #         if list1[i] < list1[last_index]:
    #             fully_sorted = False
    #         else:
    #             fully_sorted = True
    #         last_index = i
    l = len(list1)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if list1[i] > list1[j]:
                swap(list1, i, j)
                swap(list2, i, j)


def swap(in_list, start_index: int, end_index: int):
    ele1 = in_list[start_index]
    ele2 = in_list[end_index]
    in_list[start_index] = ele2
    in_list[end_index] = ele1


if __name__ == "__main__":
    thing = [7, 2, 5, 10, 100, -30]
    thing2 = [7, 2, 5, 10, 100, -30]
    dual_sort(thing, thing2)
    print(thing)
    print(thing2)