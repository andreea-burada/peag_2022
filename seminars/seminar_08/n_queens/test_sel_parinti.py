# script pentru testul selectiei parintilor - selectia de tip ruleta cu distributie fps cu sigma-scalare
import numpy as np
from FunctiiSelectii import ruleta
import generare_init as gi
import matplotlib.pyplot as grafic
# pentru legenda
import matplotlib.patches as mpatches

# generarea aleatoare a unei populatii
dim = 8
n = 10
p = gi.gen(n, dim)
# populatia p este impartita in matricea indivizilor si vectorul calitatilor
# calculul parintilor si calitatii acestora utilizand selectia ruleta cu FPS cu sigma scalare
parinti, valori = ruleta(p[:, :n], p[:, n], dim, n)
# constituirea populatiei rezultate
rez = np.zeros([dim, n + 1], dtype='int')
rez[:, :n] = parinti.copy()
rez[:, n] = valori.copy()
print("Populatia considerata curenta")
print(p)
print("Populatia de parinti")
print(rez)

x = [i for i in range(dim)]
grafic.plot(x, p[:, n], "go", markersize=16)
grafic.plot(x, rez[:, n], "ro", markersize=10)
red_patch = mpatches.Patch(color='red', label='Calitatile parintilor')
green_patch = mpatches.Patch(color='green', label='Calitatile populatiei curente')
grafic.legend(handles=[red_patch, green_patch])
grafic.show()
