import numpy as np
import matplotlib.pyplot as grafic

## takes data from a test file in which every value is written on a line
#
#preia date float dintr-un fisier text in care fiecare valoare este scrisa pe o linie
def citeste(fis):
    c = np.genfromtxt(fis)
    return c


# check the feasibility of the x chosen and computed the objective function f
#
#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,n,c,v,max):
    val=0
    cost=0
    for i in range(n):
        val=val+x[i]*v[i]
        cost=cost+x[i]*c[i]
    return cost<=max,val


#population representation by points (individual index, quality) - to see the variability in the population 
#
#figurarea populatiei prin punctele (indice individ, calitate) - pentru a vedea variabilitatea in populatie
def reprezinta_pop(pop,dim,n):
    x=[i for i in range(dim)]
    y=[pop[i][n] for i in range(dim)]
    grafic.plot(x,y,"gs-",markersize=11)

# generate the initial population
# I: fc, fv - the name of the files cost, value
#    max - the maximum capacity
#    dim - the number of individuals from the population
# O: pop - initial population
#
#genereaza populatia initiala
#I: fc, fv - numele fisierelor cost, valoare
#   max - capacitatea maxima
#   dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(fc,fv,max,dim):
    #read the data from the files cost.txt and value.txt
    #
    #citeste datele din fisierele cost si valoare
    c=citeste(fc)
    v=citeste(fv)
    #n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n=len(c)
    #works with the population as the list with dim elements - lists with n+1 individuals
    #
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            # generate the candidate with elements 0, 1
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
        # add to the population the new individual with value objective function f -> add another list with n+1 elements as element of the list pop
        #
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    reprezinta_pop(pop, dim, n)
    return pop

# Function calling example:
#
#Exemplu de apel:
#1
#import generare_init as gi
#2
#p=gi.gen("cost.txt","valoare.txt",50,10)

