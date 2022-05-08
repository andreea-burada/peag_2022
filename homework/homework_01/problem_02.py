
# 2. Compute the number of columns for which the max element is 5

ourMatrix = [[1, 2, 3, 4],
             [3, 1, 4, 2],
             [4, 3, 2, 1],
             [5, 4, 5, 6]]


# input: matrix - list of lists: our matrix
# output: noLines - no of columns for which 5 is the max element
def no_favorable_columns(matrix):
    no_columns = 0

    # we check column by column and calculate the max
    for j in range(len(matrix[0])):
        max = 0
        for i in range(len(matrix)):
            if matrix[i][j] > max:
                max = matrix[i][j]
        if max == 5:
            no_columns += 1

    return no_columns


def test():
    result = no_favorable_columns(ourMatrix)
    print("Number of columns with the max element  = 5: ", result)

# import problem_02 as p02
# p02.test()
