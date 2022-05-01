
# 3. bubble sort on matrix -> sorted lines

ourMatrix = [[1, 2, 3, 4],
             [3, 1, 4, 2],
             [4, 3, 2, 1],
             [5, 4, 2, 6]]


# input: to_be_sorted - list
# output: - ; the sorted list stored in to_be_sorted
def bubble_sort(to_be_sorted):
    swapped = 1
    while swapped == 1:
        swapped = 0
        for i in range(len(to_be_sorted) - 1):
            if to_be_sorted[i] > to_be_sorted[i + 1]:
                aux = to_be_sorted[i]
                to_be_sorted[i] = to_be_sorted[i + 1]
                to_be_sorted[i + 1] = aux
                swapped = 1


def sort_matrix(matrix):
    for i in range(len(matrix)):
        bubble_sort(matrix[i])


def test():
    sort_matrix(ourMatrix)
    print("\nOur sorted matrix:\n")
    for i in range(len(ourMatrix)):
        print(ourMatrix[i])
