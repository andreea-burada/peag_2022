import matplotlib.pyplot as grafic
import numpy as np

#objective function
#
#f. obiectiv
def foTSP(p,c,n):
    val = 0
    for i in range(n - 1):
        val = val + c[p[i]][p[i+1]]
        #val+=c[p[i],p[i+1]]
    val = val+c[p[0]][p[n-1]]
    return 100/val

#population representation by points (individual index, quality) - to see the variability in the population 
#
# figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(val, dim, n):
    x = [i for i in range(dim)]
    y = [val[i] for i in range(dim)]
    grafic.plot(x, y, "gs-", markersize=11)

# generate initial population
# I: fc - the name of the file of the costs
#    dim - the number of individuals from the population
# O: the list with 2 components [pop, val] - initial population and the array of values
#
#genereaza populatia initiala
#I: fc - numele fisierului costurilor
#   dim - numarul de indivizi din populatie
#E: lista cu 2 componente [pop,val] - populatia initiala si vectorul valorilor
def gen(fc,dim):
    #read the data from the file nxn of costs
    #
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    #n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n = len(c)
    #define a variable ndarray dim(n+1) with all elements 0
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #generate the permutation candidate with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        #evaluate candidate
        #
        #evalueaza candidat
        val[i] = foTSP(pop[i,:n],c,n)
    # [pop, val] = the list with the first element the population, the second element the array of values
    # as reference, pop=L[0], val=L[1]
    #
    #[pop,val]=lista L cu primul element populatia, al doilea element vectorul valorilor
    #ca referire, pop=L[0], val=L[1]
    reprezinta_pop(val,dim,n)
    return [pop, val]

# Function Calling Example:
#
#Exemplu de apel:
#1
#import generare_init as gi
#2
#[p,v]=gi.gen("costuri.txt",30)