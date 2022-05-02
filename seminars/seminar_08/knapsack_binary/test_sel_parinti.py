# script pentru testul selectiei parintilor - selectia de tip turneu
import numpy as np
from FunctiiSelectii import turneu
import generare_init as gi
import matplotlib.pyplot as grafic
# pentru legenda - afisare ajustata
import matplotlib.patches as mpatches

# generarea aleatoare a unei populatii
dim = 30
cmax = 30
k = 15
p, n = gi.gen("cost.txt", "valoare.txt", 30, 30)
# impartirea populatiei in lista indivizilor si lista calitatilor
# lista indivizilor (pop. list)
lp = []
# lista calitatilor (value list)
lval = []
for i in range(dim):
    individ = p[i][:n]
    lp = lp + [individ]
    lval = lval + [p[i][n]]
# populatia p este impartita in lista indivizilor si lista calitatilor
# calculul parintilor si calitatii acestora utilizand selectia turneu cu k indivizi
parinti, valori = turneu(lp, lval, dim, n, k)
# constituirea populatiei cu dim liste fiecare cu n+1 valori
rez = []
for i in range(dim):
    x = [None] * (n + 1)
    x[:n] = parinti[i].copy()
    x[n] = valori[i]
    rez = rez + [x]
print(p)
print(rez)

x = [i for i in range(dim)]
grafic.plot(x, lval, "go", markersize=16)
grafic.plot(x, valori, "ro", markersize=10)
red_patch = mpatches.Patch(color='red', label='Fitness values - mating pool')
green_patch = mpatches.Patch(color='green', label='Fitness values - current population')
grafic.legend(handles=[red_patch, green_patch])
grafic.show()
