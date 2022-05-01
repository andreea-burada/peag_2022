# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
from FunctiiSelectii import elitism
import generare_init as gi
import matplotlib.pyplot as grafic
#pentru legenda
import matplotlib.patches as mpatches

#generarea aleatoare a doua populatii
dim=16
[p1,v1],n=gi.gen("costuri.txt",dim)
[p2,v2],n=gi.gen("costuri.txt",dim)
genu,valori=elitism(p1,v1,p2,v2,dim)
#constituirea populatiei rezultate
rez=[genu,valori]
print('populatia1 cu valori')
print(v1)
print('populatia2 cu valori')
print(v2)
print('selectat:')
print(valori)
x=[i for i in range(dim)]
grafic.plot(x,v1,"go",markersize=18)
grafic.plot(x,v2,"bo",markersize=14)
grafic.plot(x,valori,"ro",markersize=10)
red_patch = mpatches.Patch(color='red', label='Generatia urmatoare')
green_patch = mpatches.Patch(color='green', label='Populatia curenta')
blue_patch = mpatches.Patch(color='blue', label='Populatia de copii')
grafic.legend(handles=[red_patch,green_patch,blue_patch])
grafic.show()

