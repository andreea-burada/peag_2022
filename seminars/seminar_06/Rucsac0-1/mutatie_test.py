import numpy as np
from FunctiiMutatieIndivizi import m_binar
import matplotlib.pyplot as grafic

#checks the feasibility of the chosen x and computes the objective function f
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
# O: dim,n,c,v,max - output parameters necessary for the mutation call
#
#genereaza populatia initiala
#I:  fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
# E:dim,n,c,v,max - parametri de iesire necesari apelului mutatiei

def gen(fc,fv,max,dim):
    # reads the data from the files cost and value
    #
    #citeste datele din fisierele cost si valoare
    c=np.genfromtxt(fc)
    v=np.genfromtxt(fv)
    # n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n=len(c)
    # works with the population as a list of dim elements - lists with n+1 individuals
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

        # we have found a feasible candidate solution, of type ndarray (array) x
        # x is transformed in list
        #
        #am gasit o solutie candidat fezabila, in data de tip ndarray (vector) x
        # x este transformat in lista
        x=list(x)
        # add the value
        #
        # adauga valoarea
        x=x+[val]
        # add to the population the new individual with the objective function value - add another list of n+1 elements as an elements of the list pop
        #
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    ind = [i for i in range(dim)]
    vect = [pop[i][n] for i in range(dim)]
    grafic.plot(ind, vect, "gs", markersize=12)
    return pop,dim,n,c,v,max


# mutation on the population of children
# I:    pop,dim,n - the population of dimensions dimx(n+1)
#       pm - the mutation probability
# O:    mpop - the mutated population
#
#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,c,v,max,pm):
    # we copy the population in the result variable
    #
    #copiem populatia in rezultat
    mpop=pop.copy()
    for i in range(dim):
        # we copy in x the individual i from the input population
        #
        #copiem in x individul i din populatia intrare
        x=pop[i][:n].copy()
        for j in range(n):
            # randomly generate if the mutation in the individual i, gene j is being made
            #
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                # mutation
                #
                #mutatie
                x[j]=m_binar(x[j])
        # the resulted individual can possibly suffer multiple mutations
        # if it is feasible, it is preserved
        #
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        fez, val = ok(x, n, c, v, max)
        if fez:
            x=x+[val]
            mpop[i]=x.copy()
    ind = [i for i in range(dim)]
    vect = [mpop[i][n] for i in range(dim)]
    grafic.plot(ind, vect, "rs", markersize=9)
    return mpop

# Function Calling Example in Python Console:
#
#Apel
#1
#import mutatie_test as mt
#2
#p,dim,n,c,v,max=mt.gen("cost.txt","valoare.txt",50,18)
# figura rezultata ramane activa - nu o inchideti
#3
#o=mt.mutatie_populatie(p,dim,n,c,v,max,0.8)

