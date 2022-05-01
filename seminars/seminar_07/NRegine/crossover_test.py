import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_OCX


#f. obiectiv
def foNR(x,n):
    # the objective function - for the queens problem
    # I: x - the individual (permutation) evaluated (a), n - the dimension of the problem
    # O: c - the quality (the number of pairs of queens which are not attacking each other)
    #
    # functia obiectiv pentru problema reginelor
    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca

    c = n*(n-1)/2
    for i in range(n):
        for j in range(i+1,n):
            if abs(i-j)==abs(x[i]-x[j]):
                c=c-1
    return c


# generates the initial population
# I: n - the dimension of the problem
#    dim - the number of individuals from the population
# O: pop - the initial population
#
#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    #define a variable ndarray with all elements zero
    #
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        # generate the permutation candidate with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n],n)
    return pop


# crossover on the population of parents pop, dimx(n+1) dimension
# I:    pop,dim,n - the population of dimx(n+1) dimension
#     c, v, max - as above
#     pc - crossover probability
#E: po - children population
# asexual recombination is implemented
#
#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop,dim,n - ca mai sus
#     c, v, max - datele problemei
#     pc- probabilitatea de crossover
#E: po - populatia copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,dim,n,pc):
    #initializes the population of children po with the population of parents
    #
    #initializeaza populatia de copii, po, cu populatia parintilor
    po=pop.copy()
    #the individuals from the population are selected 0,1, then 2,3 samd
    #
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #select parents
        #
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            #crossover x with y - OCX -
            #
            # crossover x cu y - OCX - suitable for NQueens
            c1,c2 = crossover_OCX(x,y,n)
            val1=foNR(c1, n)
            val2= foNR(c2, n)
            po[i][:n]=c1.copy()
            po[i][n]=val1
            po[i+1][:n]=c2.copy()
            po[i+1][n]=val2
    figureaza(pop[:,n],po[:,n],dim)
    return po

def figureaza(valori,val,dim):
    x = [i for i in range(dim)]
    grafic.plot(x, valori, "go", markersize=12,label='Parinti')
    grafic.plot(x, val, "ro", markersize=9,label='Copii')
    #include legends
    #
    #includerea unei legende
    grafic.legend(loc="lower left")
    grafic.xlabel('Indivizi')
    grafic.ylabel('Fitness')
    grafic.show()

# Function Calling Example in Python Console:
#1
#import crossover_test as ct
#2
#p=ct.gen(10,20)
#3
#o=ct.crossover_populatie(p,20,10,0.8)
#
#Apel
#import crossover_test as ct
#p=ct.gen(10,20)
#o=ct.crossover_populatie(p,20,10,0.8)

