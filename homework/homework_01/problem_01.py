
# 1. Compute the number of lines in a matrix with the property that the elements are in
# ascending order

ourMatrix = [[1, 2, 3, 4],
             [3, 1, 4, 2],
             [4, 3, 2, 1],
             [3, 4, 5, 6]]


# input: matrix - list of lists: our matrix
# output: noLines - no of lines that have the elements in ascending order
def no_asc_lines(matrix):
    no_lines = 0

    # we check line by line if the line is ascending
    for i in range(len(matrix)):
        ok = 1
        j = int(0)
        while j < (len(matrix[i]) - 1) and ok == 1:
            if matrix[i][j] >= matrix[i][j + 1]:
                ok = 0
            j += 1
        if ok == 1:
            no_lines += 1

    return no_lines


def test():
    result = no_asc_lines(ourMatrix)
    print("Number of lines with ascending elements: ", result)

# import problem_01 as p01
# p01.test()
