import numpy as np
from FunctiiMutatieIndivizi import m_uniforma, m_neuniforma
import matplotlib.pyplot as grafic

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


# generates the initial population
# I: fc, fv - the names of the files cost, value
#    max - the maximum capacity
#    dim - the number of individuals from the population
# O: dim,n,c,v,max - output parameters necessary for the call of the mutation
#
#genereaza populatia initiala
#I:
# fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
#    dim,n,c,v,max - parametri de iesire necesari apelului mutatiei

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
    # works with the population as the list of dim elements - lists with n+1 individuals
    #
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    vectv=[]
    for i in range(dim):
        gata=False
        while gata == False:
            # generate the candidate x with elements on [0, 1]
            #
            #genereaza candidatul x cu elemente pe [0,1]
            x=np.random.uniform(0,1,n)
            gata,val=ok(x,n,c,v,max)
        # we have found a feasible candidate solution, of type ndarray (array) x
        # x is transformed in a list
        #
        #am gasit o solutie candidat fezabila, in data de tip ndarray (vector) x
        # x este transformat in lista
        x=list(x)
        # add the value
        #
        # adauga valoarea
        x=x+[val]
        vectv=vectv+[val]
        # add to the population the new individual with the value of the objective function f - add another list with n + 1 elements as an element of the list pop
        #
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    ind=[i for i in range(dim)]
    grafic.plot(ind,vectv,"gs",markersize=12)
    return pop, dim, n, c, v, max


# mutation on the children's population
# I:   pop,dim,n - population of dimension dimx(n+1)
#      pm - the mutation probability
#      sigma - the fluaj step to the non-uniform mutation
# O: - mpop - mutated population
#
#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#   sigma - pasul de fluaj la mutatia neuniforma
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,c,v,max,pm,sigma):
    # we copy the current population in the result mpop
    #
    # copiem populatia curenta in rezultatul mpop
    mpop=pop.copy()
    valv=[]
    for i in range(dim):
        # we copy in x the individual i
        #
        #copiem in x individul i
        x=pop[i][:n].copy()
        for j in range(n):
            # randomly generates if the mutation in the individual i, gene j is being made
            #
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                #uniform mutation
                #
                #mutatie uniforma
                #x[j]=m_uniforma(0,1)
                # non-uniform mutation
                #
                #mutatie neuniforma
                x[j]=m_neuniforma(x[j],sigma,0,1)
        # the resulted individual can possibly suffer multiple mutations
        # if it is feasible, it is kept
        #
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        fez, val = ok(x, n, c, v, max)
        if fez:
            x=x+[val]
            mpop[i]=x.copy()
            valv=valv+[val]
        else:
            valv=valv+[pop[i][n]]
    ind=[i for i in range(dim)]
    grafic.plot(ind,valv,"rs",markersize=9)
    return mpop

# Function Calling Example in Python Console:
#
#Apel
#1
#import mutatie_test as mt
#2
#p,dim,n,c,v,max=mt.gen("cost.txt","valoare.txt",50,20)
# figura trebuie sa ramana activa- nu o inchideti
#3
#o=mt.mutatie_populatie(p,dim,n,c,v,max,0.8,0.7)


