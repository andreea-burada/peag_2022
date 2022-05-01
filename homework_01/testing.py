# 9. Fie S mulțimea vectorilor binari de lungime 7. Calculați, prin generare aleatoare, o matrice
# A cu 20 de linii, vectori din S și un vector V cu 20 de elemente, fiecare 𝑉[𝑖] reprezentând
# calitatea liniei i din A, definită prin suma biților vectorului linie i.
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

# rows, cols = (20, 7)
# matA = [[0 for i in range(cols)] for j in range(rows)]
#
# for i in range (len(matA)):
#     arr = np.random.randint(0, 2, 7)
#     matA[i]=arr
#
# print(matA)
#
# def sum(arr):
#     total=0
#     for el in range(0, len(arr)):
#         total = total + arr[el]
#     return total
#
# V=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#
# for i in range (0,len(matA)):
#     V[i]=sum(matA[i])
#
# print("Primul print")
# print(V)
#
#
# #10. Fie A și V construite la 9. Aranjați liniile matricei A astfel încât elementele lui V să fie în ordine
# crescătoare.
#
# def trying(matA):
#     for l in range(matA):
#         for j in range(matA[l]):
#             if V[l]>V[j]:
#                 matA[[l,j]]=matA[[j],l]
#     return matA
# print(matA)
#
# for i in range (0,len(matA)):
#     V[i]=sum(matA[i])
#
#
# print("Al doilea print")
# print(V)
#
#
# #Incercare de swap
# X = [[12,7,3],
#     [4 ,5,6],
#     [7 ,8,9]]
#
# def Swap(arr, start_index, last_index):
#     arr[:, [start_index, last_index]] = arr[:, [last_index, start_index]]
#
# Swap(X,0,2)
# print("XXXXXXXXXXX")
# print(X)
