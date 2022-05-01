import matplotlib.pyplot as grafic
import numpy as np
from FunctiiCrossoverIndivizi import crossover_uniform


# checks the feasibility of the chosen x and computes the objective function f
#
#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,n,c,v,max):
    val=0
    cost=0
    for i in range(n):
        val=val+x[i]*v[i]
        cost=cost+x[i]*c[i]
    return cost<=max,val


# generate the initial population
# I: fc, fv - the name of the files cost, value
#    max - the maximum capacity
#    dim - the number of individuals from the population
# O: pop - initial population
#
#genereaza populatia initiala
#I:
# fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(fc,fv,max,dim):
    #reads the data from the files cost and value
    #
    #citeste datele din fisierele cost si valoare
    c=np.genfromtxt(fc)
    v=np.genfromtxt(fv)
    # n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n=len(c)
    #works with the population as a list of dim elements - lists with n+1 individuals
    #
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            # generates the candidate x with elements 0, 1
            #
            #genereaza candidatul x cu elemente 0,1
            x=np.random.randint(0,2,n)
            gata,val=ok(x,n,c,v,max)
        #we have found a feasible candidate solution in type ndarray (array) x
        # x is transformed in list
        #
        #am gasit o solutie candidat fezabila, in data de tip ndarray (vector) x
        # x este transformat in lista
        x=list(x)
        # add the value
        #
        # adauga valoarea
        x=x+[val]
        # add to the population the new individual with the objective function value
        # - add another list of n+1 elements as an elements of the list pop
        #
        #adauga la populatie noul individ cu valoarea f. obiectiv
        #- adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    return pop,dim,n,c,v,max


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
def crossover_populatie(pop,dim,n,c,v,max,pc):
    po=[]
    # the individuals are selected 0,1, then 2,3 samd
    #
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #select parents
        #
        #selecteaza parintii
        x = pop[i].copy()
        y = pop[i+1].copy()
        r = np.random.uniform(0,1)
        if r<=pc:
            #crossover x with y - uniform - more suitable here
            #
            # crossover x cu y - uniform: mai potrivit aici
            c1,c2=crossover_uniform(x[:n] ,y[:n] ,n)
            fez, val = ok(c1, n, c, v, max)
            if fez:
               c1=c1+[val]
            else:
                c1 = x.copy()
            fez, val = ok(c2, n, c, v, max)
            if fez:
               c2=c2+[val]
            else:
                c2 = y.copy()
        else:
            # asexual recombination
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
        #copy the results in children population
        #
        #copiaza rezultatul in populatia urmasilor
        po = po+[c1]
        po = po+[c2]
    valorip=[pop[i][n] for i in range(dim)]
    valoric=[po[i][n] for i in range (dim)]
    figureaza(valorip,valoric, dim)
    return po


def figureaza(valori, val, dim):
    x = [i for i in range(dim)]
    grafic.plot(x, valori, "go", markersize=12, label='Parinti')
    grafic.plot(x, val, "ro", markersize=9, label='Copii')
    #define legend
    #
    #definire legenda
    grafic.legend(loc="lower left")
    grafic.xlabel('Indivizi')
    grafic.ylabel('Fitness')
    grafic.show()


# Function Calling Example in Python Console:
#1
#import crossover_test as ct
#2
#p,dim,n,c,v,max=ct.gen("cost.txt","valoare.txt",50,10)
#3
#o=ct.crossover_populatie(p,dim,n,c,v,max,0.8)
#
#Apel
#import crossover_test as ct
#p,dim,n,c,v,max=ct.gen("cost.txt","valoare.txt",50,10)
#o=ct.crossover_populatie(p,dim,n,c,v,max,0.8)

