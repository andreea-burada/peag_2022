# script pentru testul selectiei parintilor - selectia de tip ruleta cu distributie rang liniar
import numpy as np
from FunctiiSelectii import ruleta_rang
import generare_init as gi
import matplotlib.pyplot as grafic
#pentru legenda - ajustarea legendei
import matplotlib.patches as mpatches

#generarea aleatoare a unei populatii
dim=8
cmax=30
p,n=gi.gen("cost.txt","valoare.txt",30,10)
s=1.7
#impartirea populatiei in lista indivizilor si lista calitatilor
#lista indivizilor
lp=[]
#lista calitatilor
lval=[]
for i in range(dim):
    individ=p[i][:n]
    lp=lp+[individ]
    lval=lval+[p[i][n]]
# populatia p este impartita in lista indivizilor si lista calitatilor
# calculul parintilor si calitatii acestora utilizand selectia ruleta bazata pe functia rang liniar
# ATENTIE!!! TREBUIE SORTATA POPULATIA
indici=np.argsort(lval)
lps=np.array(lp)[indici]
lvals=np.array(lval)[indici]
print(lval,'\n\n')
print(np.array(lp),'\n\n')
print(lvals,'\n\n')
print(lps)
parinti,valori=ruleta_rang(lps,lvals,dim,n,s)
#constituirea populatiei cu dim liste fiecare cu n+1 valori
rez=[]
for i in range (dim):
    x=[None]*(n+1)
    x[:n]=parinti[i].copy()
    x[n]=valori[i]
    rez=rez+[x]
#afisarea valorilor initiale si a celor selectate
print(lval)
print(valori)

x=[i for i in range(dim)]
grafic.plot(x,lval,"go",markersize=16)
grafic.plot(x,valori,"ro",markersize=10)
red_patch = mpatches.Patch(color='red', label='Calitatile parintilor')
green_patch = mpatches.Patch(color='green', label='Calitatile populatiei curente')
grafic.legend(handles=[red_patch,green_patch])
grafic.show()