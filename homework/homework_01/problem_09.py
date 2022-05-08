
# 9. Consider S the set of all binary vectors of length 7. Calculate, through random generation, a matrix A of
# 20 lines, each line representing an element from set S and V, an array of 20 elements, where V[i] represents
# the quality of line i from matrix A (defines as the sum of bytes of line i)
import numpy as np


our_matrix = np.zeros((20, 7))


def generate_matrix():
    for i in range(20):
        our_matrix[i] = np.random.randint(2, size=7)
    return our_matrix


def compute_v(random_matrix):
    v = np.zeros(20)
    for i in range(len(v)):
        sum_v = 0
        for j in range(len(random_matrix[i])):
            sum_v += random_matrix[i][j]
        v[i] = sum_v
    return v


def test():
    A = generate_matrix()
    V = compute_v(A)
    print("The randomly generated matrix A: ")
    for i in range(len(A)):
        print(A[i])
    print("\nArray of qualities: ")
    print(V)