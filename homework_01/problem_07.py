
# 7. Implement the insertion sorting algorithm for list/vectors
import numpy as np


# input: to_be_sorted - list
# output: - ; the sorted list stored in to_be_sorted
def insertion_sort(to_be_sorted):
        for i in range(1, len(to_be_sorted)):
            for j in range(0, i):
                if to_be_sorted[j] > to_be_sorted[i]:
                    to_be_moved = to_be_sorted[i]
                    for k in range(i, j, -1):
                        to_be_sorted[k] = to_be_sorted[k-1]
                    to_be_sorted[j] = to_be_moved


def test():
    array = np.random.randint(100, size=10)
    print("Unsorted array: ")
    print(array)
    insertion_sort(array)
    print("\nSorted array:")
    print(array)

# import problem_07 as p07
# p07.test()
