# script pentru testul selectiei parintilor - selectia de tip SUS cu distributie fps cu sigma-scalare
import numpy as np

import generare_init as gi
import matplotlib.pyplot as grafic
# pentru legenda - ajustare
import matplotlib.patches as mpatches


# calculul distributiei de probabilitate FPS pentru un vector de calitati
# I: qual,dim - vectorul calitatilor, de dimensiune dim
# E: distributia cumulata qfps
def fps(qual, dim):
    fps = np.zeros(dim)
    # suma valorilor vectorului qual
    suma = np.sum(qual)
    for i in range(dim):
        fps[i] = qual[i] / suma
    print(fps)
    qfps = fps.copy()
    for i in range(1, dim):
        qfps[i] = qfps[i - 1] + fps[i]
    return qfps


# fps cu sigma scalare
# I: qual,dim - vectorul calitatilor, de dimensiune dim
# E: distributia cumulata qfps
# daca toate elementele din qual sunt egale, returneaza fps standard
def sigmafps(qual, dim):
    # media vectorului qual
    med = np.mean(qual)
    # deviatia standard - qual
    var = np.std(qual)
    # calculul variantei sigma-scalate: newq[i]=max(qual[i]-(med-2var)), i=1...dim
    newq = [max(0, qual[i] - (med - 2 * var)) for i in range(dim)]
    # calculul distributieipe noul vector
    if np.sum(newq) == 0:
        qfps = fps(qual, dim)
    else:
        qfps = fps(newq, dim)
    return qfps


# selectia SUS cu distributia fps cu sigma scalare
# I: pop,qual,dim,n - matricea populatiei, vectorul calitatilor, pop-dim x n, qual - dim
# E: spop,squal - populatia selectata, impreuna cu calitatile membrilor sai
def SUS(pop, qual, dim, n):
    spop = pop.copy()
    squal = np.zeros(dim)
    print(qual)
    # utilizeaza fps cu sigma-scalare
    qfps = sigmafps(qual, dim)
    r = np.random.uniform(0, 1 / dim)
    print(qfps)
    print(r)
    print(1 / dim)
    k, i = 0, 0
    while (k < dim):
        while (r <= qfps[i]):
            spop[k][:] = pop[i][:]
            squal[k] = qual[i]
            r = r + 1 / dim
            k = k + 1
            print(i)
        i = i + 1
    return spop, squal


# generarea aleatoare a unei populatii
dim = 10
[p, v], n = gi.gen("costuri.txt", dim)
# rezulta matricea indivizilor si vectorul calitatilor
# calculul parintilor si calitatii acestora utilizand selectia SUS cu FPS cu sigma-scalare
parinti, valori = SUS(p, v, dim, n)
# constituirea populatiei rezultate
rez = [parinti, valori]
# print(p)
# print(v)
# print('rezulta')
# print(parinti)
# print(valori)

x = range(dim)
grafic.plot(x, v, "go", markersize=16)
grafic.plot(x, valori, "ro", markersize=10)
red_patch = mpatches.Patch(color='red', label='Calitatile parintilor')
green_patch = mpatches.Patch(color='green', label='Calitatile populatiei curente')
grafic.legend(handles=[red_patch, green_patch])
grafic.show()
