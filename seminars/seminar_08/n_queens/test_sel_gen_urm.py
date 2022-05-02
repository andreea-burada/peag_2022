# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
from FunctiiSelectii import elitism
import generare_init as gi
import matplotlib.pyplot as grafic
# pentru legenda
import matplotlib.patches as mpatches

# generarea aleatoare a doua populatii
dim = 6
n = 14
p1 = gi.gen(n, dim)
p2 = gi.gen(n, dim)
genu, valori = elitism(p1[:, :n], p1[:, n], p2[:, :n], p2[:, n], dim)
# constituirea populatiei rezultate
rez = np.zeros([dim, n + 1], dtype='int')
rez[:, :n] = genu.copy()
rez[:, n] = valori.copy()
print('populatia1')
print(p1)
print('populatia2')
print(p2)
print('selectat:')
print(rez)

x = [i for i in range(dim)]
grafic.plot(x, p1[:, n], "go", markersize=18)
grafic.plot(x, p2[:, n], "bo", markersize=14)
grafic.plot(x, rez[:, n], "ro", markersize=10)
red_patch = mpatches.Patch(color='red', label='Generatia urmatoare')
green_patch = mpatches.Patch(color='green', label='Populatia curenta')
blue_patch = mpatches.Patch(color='blue', label='Copiii eventual mutati')
grafic.legend(handles=[red_patch, green_patch, blue_patch])
grafic.show()
