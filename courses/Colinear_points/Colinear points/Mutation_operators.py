import numpy as np

#THE OBTAINED INDIVIDUALS SHOULD BE EVALUATED BY THE CALLING FUNCTIONS

# BINARY VECTORS
# bit-flip mutation

#I: x
#E: y
def m_binar(x):
    y=not x
    return int(y)


# INTEGER VALUED VECTORS
# random resetting

#I: a,b - the interval endpoints
#E: y - the output value
def m_ra(a,b):
    y=np.random.randint(a,b)
    return y

#creep mutation

#I: x - the initial value
#   a,b - the interval endpoints
#E:y - the output value
def m_fluaj(x,a,b):
    # generate the sign
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

# REAL VALUED VECTORS
# uniform mutation

#I:a,b - the interval endpoints
#E: y - the output value
def m_uniforma(a,b):
    y=np.random.uniform(a,b)
    return y

# non uniform mutation

#I: x - the input value
#   sigma - mutation step size
#   a,b - the interval endpoints
#E:y - the output value
def m_neuniforma(x,sigma,a,b):
    # noise generation
    p=np.random.normal(0,sigma)
    y=x+p
    if y>b:
        y=b
    if y<a:
        y=a
    return y


# PERMUTATIONS
# inversion mutation

# I:x,n - the input permutation and its length
# E:y - the resulted permutation
def m_perm_inversiune(x,n):
    # randomly generate the mutation sequence - two genes
    poz = np.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = np.random.randint(0, n, 2)
    p1 = np.min(poz)
    p2 = np.max(poz)
    y=x.copy()
    y[p1:p2+1]=[x[i] for i in range(p2,p1-1,-1)]
    return y


# swap mutation

# I:x,n - the input permutation and its length
# E:y - the resulted permutation
def m_perm_interschimbare(x,n):
    # randomly generate the mutation sequence - two genes
    poz = np.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = np.random.randint(0, n, 2)
    p1 = np.min(poz)
    p2 = np.max(poz)
    y=x.copy()
    y[p1]=x[p2]
    y[p2]=x[p1]
    return y


# insert mutation
# I:x,n - the input permutation and its length
# E:y - the resulted permutation

def m_perm_inserare(x,n):
    # randomly generate the mutation sequence - two genes
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