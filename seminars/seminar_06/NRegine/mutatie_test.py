import numpy as np
from FunctiiMutatieIndivizi import m_perm_interschimbare, m_perm_inserare
import matplotlib.pyplot as grafic

# the objective function - for the queens problem#
# I: x - the individual (permutation) evaluated (a), n - the dimension of the problem
# O: c - the quality (the number of pairs of queens which are not attacking each other)
#
# functia obiectiv pentru problema reginelor
# I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
# E: c - calitate (numarul de perechi de regine care nu se ataca)

def foNR(x,n):
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
    # define a variable ndarray with all elements zero
    #
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        # generate the permutation candidate with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n],n)
    ind = [i for i in range(dim)]
    grafic.plot(ind, pop[:,n], "gs", markersize=12)
    return pop


# mutation on the children's population
# I:pop,dim,n - the population of dimensions dimx(n+1)
#   pm - mutation probability
# O: - mpop - the mutated population
#
#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,pm):
    mpop=pop.copy()
    for i in range(dim):
        # randomly generates if the mutation is being made
        #
        #genereaza aleator daca se face mutatie
        r=np.random.uniform(0,1)
        if r<=pm:
            # mutation on the individual i - through interchange
            #
            #mutatie in individul i - prin interschimbare
            #x=m_perm_interschimbare(mpop[i,:n],n)
            # mutation on the individual i - through insertion
            #
            #mutatie in individul i - prin inserare
            x=m_perm_inserare(mpop[i,:n],n)
            mpop[i,:n]=x.copy()
            mpop[i,n]=foNR(x,n)
    ind = [i for i in range(dim)]
    grafic.plot(ind, mpop[:,n], "rs", markersize=9)
    return mpop

# Program Calling Example - in Python Console:
#
#Apel
#1
#import mutatie_test as mt
#2
#p=mt.gen(8,10)
# pastram figura rezultata activa
#3
#o=mt.mutatie_populatie(p,10,8,0.2)

