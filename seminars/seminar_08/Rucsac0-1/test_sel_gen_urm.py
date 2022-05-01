# script pentru testul selectiei generatiei urmatoare - selectia de tip elitist
import numpy as np
from FunctiiSelectii import elitism
import generare_init as gi
import matplotlib.pyplot as grafic
#pentru legenda
import matplotlib.patches as mpatches

#generarea aleatoare a doua populatii
dim=8
cmax=30
p1,n=gi.gen("cost.txt","valoare.txt",30,8)
p2,n=gi.gen("cost.txt","valoare.txt",30,8)
#impartirea populatiilor in lista indivizilor si lista calitatilor
#lista indivizilor
lp1,lp2=[],[]
#lista calitatilor
lval1,lval2=[],[]
for i in range(dim):
    individ1,individ2=p1[i][:n],p2[i][:n]
    lp1,lp2=lp1+[individ1], lp2+[individ2]
    lval1,lval2=lval1+[p1[i][n]],lval2+[p2[i][n]]
# calculul populatiei urmatoare si calitatii acesteia utilizand selectia elitista
genu,valori=elitism(lp1,lval1,lp2,lval2,dim)
#constituirea populatiei cu dim liste fiecare cu n+1 valori
rez=[]
for i in range (dim):
    x=[None]*(n+1)
    x[:n]=genu[i].copy()
    x[n]=valori[i]
    rez=rez+[x]
print(p1)
print(p2)
print(rez)

x=[i for i in range(dim)]
grafic.plot(x,lval1,"go",markersize=18)
grafic.plot(x,lval2,"bo",markersize=14)
grafic.plot(x,valori,"ro",markersize=11)
red_patch = mpatches.Patch(color='red', label='Generatia urmatoare')
green_patch = mpatches.Patch(color='green', label='Populatia curenta')
blue_patch = mpatches.Patch(color='blue', label='Populatia de copii')
grafic.legend(handles=[red_patch,green_patch,blue_patch])
grafic.show()

