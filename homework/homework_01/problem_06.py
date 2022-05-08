
# 6. Consider A and B two square matrices and n,positive integer different than zero. Calculate
# A^T(A transposed), A+B, A*B, A^𝑛
import numpy as np


A = np.zeros((5, 5))
B = np.zeros((5, 5))


# generating square matrix
def generate_matrix(gen_mat):
    for i in range(5):
        gen_mat[i] = np.random.randint(10, size=5)


# A^T
def transpose(non_transposed):
    return np.transpose(non_transposed)


# A+B
def matrix_sum(first_mat, second_mat):
    result = np.zeros((5, 5))
    for i in range(len(first_mat)):
        result[i] = first_mat[i] + second_mat[i]
    return result


# A*B
def matrix_mul(first_mat, second_mat):
    return np.matmul(first_mat, second_mat)


# A^n
def matrix_pow(mat, pow):
    return np.linalg.matrix_power(mat, pow)


def test():
    n = int(input("n= "))

    generate_matrix(A)
    print("Matrix A:")
    for i in range(len(A)):
        print(A[i])

    generate_matrix(B)
    print("\nMatrix B:")
    for i in range(len(B)):
        print(B[i])

    A_transposed = transpose(A)
    print("\n\nA transposed:")
    for i in range(len(A_transposed)):
        print(A_transposed[i])

    matr_sum = matrix_sum(A, B)
    print("\nA + B:")
    for i in range(len(matr_sum)):
        print(matr_sum[i])

    matr_prod = matrix_mul(A, B)
    print("\nA * B:")
    for i in range(len(matr_prod)):
        print(matr_prod[i])

    matr_n = matrix_pow(A, n)
    print("\nA ^", n, ":")
    for i in range(len(matr_n)):
        print(matr_n[i])

# A = [[1, 2, 3], [2, 3, 4]]
# B = [[0, 1, 2], [0, 1, 2]]
