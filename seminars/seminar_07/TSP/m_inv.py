import numpy

def m_perm_inversiune(x,n):
    # generarea pozitiilor pentru inversiune
    poz = numpy.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = numpy.random.randint(0, n, 2)
    p1 = numpy.min(poz)
    p1=0
    p2 = numpy.max(poz)
    y=x.copy()
    #y[p1:p2+1]=x[p2:p1-1:-1]
    # daca p1=0, p1-1=-1 --> chiar daca valoarea este exslusa din sirul [p2:p1-1:-1]={p2,p2-1,...,p1>=0},
    # nu este permis -1 ca indice
    y[p1:p2]=x[p2:p1:-1]
    y[p2]=x[p1]
    return y
