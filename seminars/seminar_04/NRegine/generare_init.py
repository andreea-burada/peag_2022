import numpy as np
import matplotlib.pyplot as grafic


# objective function
#
#f. obiectiv
def foNR(x,n):
    # the objective function for the N-queens problem
    # I: x - the individual (permutation) evaluated(a), n - the dimension of the problem
    # O: c - quality (the number of pairs of queens which are not attacking each other)
    #
    # functia obiectiv pentru problema reginelor
    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca)

    c = n*(n-1)/2
    for i in range(n-1):
        for j in range(i+1,n):
            if abs(i-j)==abs(x[i]-x[j]):
                c=c-1
                #c-=1
    return c

#population representation by points (individual index, quality) - to see the variability in the population 
#
#figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(pop,dim,n):
    x=[i for i in range(dim)]
    y=[pop[i][n] for i in range(dim)]
    grafic.plot(x,y,"gs-",markersize=11)


# generate the initial population
# I:
#  n - the dimension of the problem
#  dim - the number of individuals from the population
# O: pop - initial population
#
#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    # define a variable ndarray with all elements zero
    #
    #defineste o variabila ndarray cu toate elementele nule
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        # generate the candidate permutation with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:],n)
    reprezinta_pop(pop, dim, n)
    return pop

# Function calling example in Python Console:
#
#Exemplu de apel in consola:
#1
#import generare_init as gi
#2
#p=gi.gen(8,30)

