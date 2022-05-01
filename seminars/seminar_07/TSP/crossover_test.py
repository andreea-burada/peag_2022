import numpy as np
from FunctiiCrossoverIndivizi import crossover_PMX
import matplotlib.pyplot as grafic

# objective function
#
#f. obiectiv
def foTSP(p,c,n):
    val = 0
    for i in range(n - 1):
        val = val + c[p[i]][p[i+1]]
    val = val+c[p[0]][p[n-1]]
    return 100/val


# Initial Population
# generate the initial population
# I: fc - the name of the file of costs
#    dim - the number of individuals from the population
# O: the list with 2 components [pop, val] - the initial population and the array of values
#    for the test of the crossover and the matrix c
#
#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: lista cu 2 componente [pop,val] - populatia initiala si vectorul valorilor
#  pentru testul crossover si matricea c
def gen(fc,dim):
    #read the data from the file nxn of the costs
    #
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    #n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n = len(c)
    #define a variable ndarray dimx(n+1) with all elements 0
    #
    #defineste o variabila ndarray dimx(n+1) cu toate elementele 0
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #generate the permutation candidate with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        #evaluate candidate
        #
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c,n)
    # [pop, val] = the list L with the first element the population, the second element the array of values
    # as a reference, pop=L[0], val=L[1]
    #
    #[pop,val]=lista L cu primul element populatia, al doilea element vectorul valorilor
    #ca referire, pop=L[0], val=L[1]
    return [pop, val],c

#crossover on the parent population pop, size dimxn
# I: l,dim,n - l=[pop,valori], as in the gen function
#     c - problem data
#     pc- crossover probability
#O: [po,val] - children population, accompanied by qualities
# asexual recombination is implemented
#
#crossover pe populatia de parinti pop, de dimensiune dimxn
# I: l,dim,n - l=[pop,valori], ca in functia de generare
#     c - datele problemei
#     pc- probabilitatea de crossover
#E: [po,val] - populatia copiilor, insotita de calitati
# este implementata recombinarea asexuata
def crossover_populatie(l,dim,n,c,pc):
    pop=l[0]
    valori=l[1]
    # initialize the children population po with the matrix of 0 elements
    #
    # initializeaza populatia de copii, po, cu matricea cu elementele 0
    po=np.zeros((dim,n),dtype=int)
    # initialize the children values val with the matrix of 0 elements
    #
    # initializeaza valorile populatiei de copii, val, cu matricea cu elementele 0
    val=np.zeros(dim,dtype=float)
    #2 individuals are randomly selected - the matrix is accessed after a permutation of the set of lines 0.2, ..., dim-1
    #
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizi - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    poz=np.random.permutation(dim)
    #or 2 consecutive individuals are selected
    #
    #sau populatia este parcursa astfel incat sunt selectati 2 indivizi consecutivi
    #poz=range(dim) #- pentru pastrarea ordinii
    for i in range(0,dim-1,2):
        #select parents
        #
        #selecteaza parintii
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x with y - PMX - suitable for problems with adjacent dependence
            #
            # crossover x cu y - PMX - potrivit pentru probleme cu dependenta de adiacenta
            c1,c2 = crossover_PMX(x,y,n)
            v1=foTSP(c1,c,n)
            v2=foTSP(c2,c,n)
        else:
            #asexual recombination
            #
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
            v1=valori[poz[i]]
            v2=valori[poz[i+1]]
        #copy the result to the offspring population
        #
        #copiaza rezultatul in populatia urmasilor
        po[i] = np.copy(c1)
        po[i+1] = np.copy(c2)
        val[i]=v1
        val[i+1]=v2
    valori=[valori[poz[i]] for i in range(dim)]
    figureaza(valori,val,dim)
    return [po, val]

def figureaza(valori,val,dim):
    x = range(dim)
    grafic.plot(x, valori, "go", markersize=14,label="Calitate parinti")
    grafic.plot(x, val, "ro", markersize=10,label="Calitate copii")
    #define the legend
    #
    #definire legenda
    grafic.legend(loc="upper left")
    grafic.xlabel("Indicii indivizilor")
    grafic.ylabel("Calitatile indivizilor")
    grafic.show()

# Function Calling Example in Python Console:
#1
#import crossover_test as ct
#2
#[p,v],c=ct.gen("costuri.txt",20)
#3
#[o,vo]=ct.crossover_populatie([p,v],20,10,c,0.8)
#
#Apel
#import crossover_test as ct
#[p,v],c=ct.gen("costuri.txt",20)
#[o,vo]=ct.crossover_populatie([p,v],20,10,c,0.8)

