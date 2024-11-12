from typing import List

def dual_sort(list1: List, list2: List):
    """
    Sorts `list1` in ascending order while applying the same reordering to `list2`.

    This function performs a parallel bubble sort, rearranging elements in `list1` 
    such that they are sorted in ascending order. The elements in `list2` are 
    reordered in the same way as `list1` to maintain their original pairing.

    Parameters:
        list1 (List): The primary list of elements to sort in ascending order.
        list2 (List): The secondary list to reorder in correspondence with `list1`.

    Raises:
        ValueError: If `list1` and `list2` are not of the same length.

    Example:
        >>> list1 = [7, 2, 5, 10]
        >>> list2 = ['a', 'b', 'c', 'd']
        >>> dual_sort(list1, list2)
        >>> print(list1)  # Output: [2, 5, 7, 10]
        >>> print(list2)  # Output: ['b', 'c', 'a', 'd']
    """
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
            if list1[j] > list1[j+1]:  
                swap(list1, j, j+1)
                swap(list2, j, j+1)


def swap(in_list, start_index: int, end_index: int):
    ele1 = in_list[start_index]
    ele2 = in_list[end_index]
    in_list[start_index] = ele2
    in_list[end_index] = ele1


if __name__ == "__main__":
    thing = [7, 2, 5, 10, 100, -30]
    thing2 = ["A", "B", "C", "D", "E", "F"]
    dual_sort(thing, thing2)
    print(thing)
    print(thing2)