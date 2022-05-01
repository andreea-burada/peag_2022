import problem_09 as p09

# Consider A and V from the previous problem. Arrange the lines of matrix A so that the elements of V are
# ordered in ascending order


def order_according_to_v(to_be_ordered, reference):
    for i in range (len(reference)-1):
        for j in range (i+1,len(reference)):
            if(reference[i] > reference[j]):
                reference[i], reference[j] = reference[j], reference[i]
                for k in range(len(to_be_ordered[i])):
                    to_be_ordered[i][k], to_be_ordered[j][k] = to_be_ordered[j][k], to_be_ordered[i][k]

def test():
    A = p09.generate_matrix()
    V = p09.compute_v(A)
    print("The randomly generated matrix A before sorting: ")
    for i in range(len(A)):
        print(A[i])
    print("\nUnsorted array of qualities: ")
    print(V)
    order_according_to_v(A, V)
    print("\n\nThe randomly generated matrix A after sorting: ")
    for i in range(len(A)):
        print(A[i])
    print("\nSorted array of qualities: ")
    print(V)

# ---to test---
# import problem_10 as p10
# p10.test()
