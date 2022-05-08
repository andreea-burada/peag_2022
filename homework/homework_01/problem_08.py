# 8. Verify the property of a permutation that is an identical permutation
import numpy as np


def verify_permutation(p):
    for i in range(len(p)):
        if p[i] != (i + 1):
            return False
    return True


def test():
    # our_permutation = [1, 2, 3, 4, 5]
    our_permutation = np.random.permutation([1, 2, 3, 4, 5])
    print("The permutation: ")
    print(our_permutation)
    if verify_permutation(our_permutation):
        print("\nOur permutation is identical\n")
    else:
        print("\nOur permutation is NOT identical\n")

# import problem_08 as p08
# p08.test()
