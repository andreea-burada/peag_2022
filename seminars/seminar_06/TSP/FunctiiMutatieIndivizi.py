import numpy as np

# All Resulted Individuals' Evaluations - In Caller
#
#TOATE EVALUARILE INDIVIZILOR REZULTATI - IN APELATOR


# Binary Arrays
# bit flip mutation
# I: x - the value that is being modified
# O: y - the result of the mutation
#
# VECTORI BINARI
# mutatia bitflip
#I: x - valoarea care se modifica
#E: y - rezultatul mutatiei
def m_binar(x):
    y=not x
    return int(y)


# Integer Numbers Arrays
# randomly resetting
# I: a,b - the resetting is being made on the set a, a+1, ..., b-1
# O: y - the new value
#
#VECTORI NUMERE INTREGI
#resetare aleatoare
#I:a,b - resetarea se face pe multimea a, a+1,...,b-1
#E: y - noua valoare
def m_ra(a,b):
    y=np.random.randint(a,b)
    return y

# "fluaj" mutation
# I: x - value to change
#    a,b - the limits that have to output the result y, the variant of x modified by a unit
# O: y - as above
#
#mutatia fluaj
#I: x - valoarea de modificat
#   a,b - limitele in care trebuie sa rezulte iesirea y, varianta a lui x modificata cu o unitate
#E:y - ca mai sus
def m_fluaj(x,a,b):
    # generating +1 or -1
    #
    #generare +1 sau -1
    p=np.random.randint(0,2)
    if p==0:
        sign=-1
    else:
        sign=1
    y=x+sign
    if y>b:
        y=b
    if y<a:
        y=a
    return y

# Real Numbers Arrays
# Uniform Mutation
# I: a,b - the interval in which the resetting is being done
# O: y - the new value
#
#VECTORI NUMERE REALE
#mutatia uniforma
#I:a,b - intervalul in care se face resetarea
#E: y - noua valoare
def m_uniforma(a,b):
    y=np.random.uniform(a,b)
    return y

# non-uniform mutation
# I: x - value to change
#    sigma - "fluaj" step
#    a,b - the limits in which the output y must be
# O: y - as above
#
#mutatia neuniforma
#I: x - valoarea de modificat
#   sigma - pasul de fluaj
#   a,b - limitele in care trebuie sa rezulte iesirea y
#E:y - ca mai sus
def m_neuniforma(x,sigma,a,b):
    #generate noise
    #
    #generare zgomot
    p=np.random.normal(0,sigma)
    y=x+p
    if y>b:
        y=b
    if y<a:
        y=a
    return y


# Permutations
# the inversion mutation of the permutation x with n components
# I: x,n
# O: y - result permutation
#
#PERMUTARI
# mutatia prin inversiune a permutarii x cu n componete
# I:x,n
# E:y - permutarea rezultat
def m_perm_inversiune(x,n):
    # generates the positions for the inversion
    #
    # generarea pozitiilor pentru inversiune
    poz = np.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = np.random.randint(0, n, 2)
    p1 = np.min(poz)
    p2 = np.max(poz)
    y=x.copy()
    y[p1:p2+1]=[x[i] for i in range(p2,p1-1,-1)]
    return y


# interchange(swap) mutation of the permutation x with n components
# I: x,n
# O: y - result permutation
#
# mutatia prin interschimbare a permutarii x cu n componete
# I:x,n
# E:y - permutarea rezultat
def m_perm_interschimbare(x,n):
    # generates the positions for the inversion
    #
    # generarea pozitiilor pentru inversiune
    poz = np.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = np.random.randint(0, n, 2)
    p1 = np.min(poz)
    p2 = np.max(poz)
    y=x.copy()
    y[p1]=x[p2]
    y[p2]=x[p1]
    return y


# mutation through the insertion of the permutation x with n components
# I: x,n
# O: y - result permutation
#
# mutatia prin inserare a permutarii x cu n componete
# I:x,n
# E:y - permutarea rezultat
def m_perm_inserare(x,n):
    # generates the positions for the inversion
    #
    # generarea pozitiilor pentru inversiune
    poz = np.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = np.random.randint(0, n, 2)
    p1 = np.min(poz)
    p2 = np.max(poz)
    y=x.copy()
    y[p1+1]=x[p2]
    if p1<n-2:
        y[p1+2:n]=np.array([x[i] for i in range(p1+1,n) if i != p2])
    return y