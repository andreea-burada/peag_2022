
# 4. insertion sort for columns

ourMatrix = [[1, 2, 3, 4],
             [3, 1, 4, 2],
             [4, 3, 2, 1],
             [5, 4, 2, 6]]


# input: to_be_sorted - list of lists (matrix)
# output: - ; the sorted matrix stored in to_be_sorted
def insertion_sort(to_be_sorted):
    for column in range(len(to_be_sorted)):
        for i in range(1, len(to_be_sorted)):
            for j in range(0, i):
                if to_be_sorted[j][column] > to_be_sorted[i][column]:
                    to_be_moved = to_be_sorted[i][column]
                    for k in range(i, j, -1):
                        to_be_sorted[k][column] = to_be_sorted[k-1][column]
                    to_be_sorted[j][column] = to_be_moved


def test():
    insertion_sort(ourMatrix)
    print("\nSorted matrix:\n")
    for i in range(len(ourMatrix)):
        print(ourMatrix[i])
