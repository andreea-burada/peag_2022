import numpy as np
from FunctiiCrossoverIndivizi import crossover_OCX, crossover_PMX, crossover_CX

def test_PMX(n):
    x1=np.random.permutation(n)
    y1=np.random.permutation(n)
    print(x1)
    print(y1)
    c1,c2=crossover_PMX(x1,y1,n)
    print("Rezultat")
    print(c1)
    print(c2)
    return c1,c2

def test_OCX(n):
    x1=np.random.permutation(n)
    y1=np.random.permutation(n)
    print(x1)
    print(y1)
    c1,c2=crossover_OCX(x1,y1,n)
    print("Rezultat")
    print(c1)
    print(c2)
    return c1,c2

def test_CX(n):
    x1=np.random.permutation(n)
    y1=np.random.permutation(n)
    print(x1)
    print(y1)
    c1,c2=crossover_CX(x1,y1,n)
    print("Rezultat")
    print(c1)
    print(c2)
    return c1,c2