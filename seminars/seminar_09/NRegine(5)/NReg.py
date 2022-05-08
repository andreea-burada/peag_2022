import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_OCX
from FunctiiMutatieIndivizi import m_perm_inserare, m_perm_interschimbare
from FunctiiSelectii import elitism, ruleta


#f. obiectiv
def foNR(x,n):
    # functia obiectiv pentru problema reginelor

    # I: x - individul (permutarea) evaluat(a), n-dimensiunea problemei
    # E: c - calitate (numarul de perechi de regine care nu se ataca

    c = n*(n-1)/2
    for i in range(n):
        for j in range(i+1,n):
            if abs(i-j)==abs(x[i]-x[j]):
                c=c-1
    return c


#genereaza populatia initiala
#I:
# n - dimensiunea prolemei
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
def gen(n,dim):
    #defineste o variabila ndarray cu toate elementelo nule
    pop=np.zeros((dim,n+1),dtype=int)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i,:n]=np.random.permutation(n)
        pop[i,n]=foNR(pop[i,:n],n)
    return pop

#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop,dim,n - ca mai sus
#     c, v, max - datele problemei
#     pc- probabilitatea de crossover
#E: po - populatia copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,dim,n,pc):
    #initializeaza populatia de copii, po, cu populatia parintilr
    po=pop.copy()
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - OCX - potrivit pentru NRegine
            c1,c2 = crossover_OCX(x,y,n)
            val1=foNR(c1, n)
            val2= foNR(c2, n)
            po[i][:n]=c1.copy()
            po[i][n]=val1
            po[i+1][:n]=c2.copy()
            po[i+1][n]=val2
    return po



#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,pm):
    mpop=pop.copy()
    for i in range(dim):
        #genereaza aleator daca se face mutatie
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutatie in individul i - prin inserare
            x=m_perm_inserare(mpop[i,:n],n)
            mpop[i,:n]=x.copy()
            mpop[i,n]=foNR(x,n)
    return mpop

#MUTATIE


def arata(sol,v):
    # vizualizare asezare regine pe tabla de sah

    # I: sol - permutarea care defineste asezarea
    #    v - vectorul cu cea mai buna calitate din fiecare generatie
    # E: -

    n=len(sol)
    t=len(v)
    minim=min(v)
    t1="Evoluția calității (cel mai bun individ din fiecare generație).\nRezultatul "
    t2="Cea mai bună așezare a reginelor găsită.\nRezultatul "
    t4="este optim (" + str(minim) + " vs 0" + ")"
    if minim>0:
        t3="nu "
    else:
        t3=""
    titlu1=f'{t1}{t3}{t4}'
    titlu2=t2+t3+t4

    fig1=grafic.figure()
    x=[i for i in range(t)]
    grafic.plot(x,v,'ro-')
    grafic.ylabel("Calitate")
    grafic.xlabel("Generația")
    grafic.title(titlu1)

    fig=grafic.figure()
    ax=fig.gca()
    x=[i+0.5 for i in range(n)]
    y=[sol[i]+0.5 for i in range(n)]
    grafic.plot(x,y,'r*',markersize=10)
    grafic.xticks(range(n+1))
    grafic.yticks(range(n+1))
    grafic.grid(True,which='both',color='k', linestyle='-', linewidth=1)
    ax.set_aspect('equal')
    grafic.title(titlu2)
    fig.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI CELOR N REGINE
#I: n - dimensiunea problemei
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - maximul functiei fitness - n*(n-1)/2 - nr de perechi de regine aflate in pozitie de atac
def GA(n,dim,NMAX,pc,pm):
    #generarea populatiei la momentul initial
    pop=gen(n,dim)
    #initializari pentru GA
    it=0
    gata=False
    maxim=np.max(pop[:,n])
    istoric_v=[n*(n-1)/2-maxim]
    #conditia de terminare:
        # am depasit un numar maxim de repetari, NMAX SAU
        # populatia contine indivizi cu aceeasi calitate SAU
        # nu a fost atins maximul functiei obiectiv, n*(n-1)/2
    while it<NMAX and not gata and maxim<n*(n-1)/2 :
        #selectia parintilor
        spop,sval=ruleta(pop[:,:n],pop[:,n],dim,n)
        pop_s=np.zeros([dim,n+1])
        pop_s[:,:n]=spop.copy()
        pop_s[:,n]=sval.copy()
        # recombinarea
        pop_o=crossover_populatie(pop_s,dim,n,pc)
        # mutatia
        pop_mo=mutatie_populatie(pop_o,dim,n,pm)
        #selectia generatiei urmatoare
        newpop,newval=elitism(pop[:,:n],pop[:,n],pop_mo[:,:n],pop_mo[:,n],dim)
        minim=np.min(newval)
        maxim=np.max(newval)
        #opreste evolutia la populatia cu toti indivizii de aceeasicalitate
        if maxim==minim:
            gata=True
        else:
            it=it+1
        istoric_v.append(n*(n-1)/2-np.max(newval))
        pop[:,:n]=newpop.copy()
        pop[:,n]=newval.copy()
    i_sol=np.where(pop[:,n]==maxim)
    sol=pop[i_sol[0][0]][:n]
    val=n*(n-1)/2-maxim
    arata(sol,istoric_v)
    return sol, val

#import NReg as nr
#sol,val=nr.GA(12,50,250,0.8,0.1)