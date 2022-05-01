import numpy as np
from FunctiiMutatieIndivizi import m_perm_inversiune
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
#    for the test of the mutations and the matrix c
#
#POPULATIA INITIALA
#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: lista cu 2 componente [pop,val] - populatia initiala si vectorul valorilor
#  pentru testul mutatiei si matricea c
def gen(fc,dim):
    # read the data from the file nxn of the costs
    #
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    # n = the dimension of the problem
    #
    #n=dimensiunea problemei
    n = len(c)
    # define a variable ndarray dimx(n+1) with all elements 0
    #
    #defineste o variabila ndarray dimx(n+1) cu toate elementele 0
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        # generate the permutation candidate with n elements
        #
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evaluate candidate
        #
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c,n)
    # [pop, val] = the list L with the first element the population, the second element the array of values
    # as a reference, pop=L[0], val=L[1]
    #
    #[pop,val]=lista L cu primul element populatia, al doilea element vectorul valorilor
    #ca referire, pop=L[0], val=L[1]
    ind=[i for i in range(dim)]
    grafic.plot(ind,val,"gs",markersize=12)
    return [pop, val],c



# Mutation
# the mutation operation of the descendants obtained through recombination

    # I: desc - [po,vo] - the population of the children followed by the array of qualities
    #    dim,n - the dimensions
    #    pm - the mutation probability
    #    c - the costs matrix
    # O: descm - [mpo,mvo] - the obtained individuals
#
#MUTATIE
 # operatia de mutatie a descendentilor obtinuti din recombinare

    # I: desc - [po,vo] - populatia copiilor insoltita de vectorul calitatilor
    #   dim,n - dimensiunile
    #    pm - probabilitatea de mutatie
    #    c - matricea costurilor
    # E: descm - [mpo,mvo] - indivizii obtinuti
def mutatie_populatie(desc,dim,n,c,pm):
    po=desc[0]
    vo=desc[1]
    mpo=po.copy()
    mvo=vo.copy()
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpo[i]
            y=m_perm_inversiune(x,n)
            mpo[i]=y
            mvo[i]=foTSP(y,c,n)
    ind = [i for i in range(dim)]
    grafic.plot(ind, mvo, "rs", markersize=9)
    return [mpo,mvo]

# Program Calling Example in the Python Console
#
#Apel
#1
#import mutatie_test as ct
#2
#[p,v],c=ct.gen("costuri.txt",30)
# figura trebuie sa ramana activa - nu o inchideti
#3
#[o,vo]=ct.mutatie_populatie([p,v],30,10,c,0.2)