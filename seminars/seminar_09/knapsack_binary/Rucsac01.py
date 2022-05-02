import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_uniform, crossover_unipunct
from FunctiiMutatieIndivizi import m_binar
from FunctiiSelectii import elitism, ruleta

#verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x,n,c,v,max):
    val=0
    cost=0
    for i in range(n):
        val=val+x[i]*v[i]
        cost=cost+x[i]*c[i]
    return cost<=max,val


#genereaza populatia initiala
#I:
# fc, fv - numele fisierelor cost, valoare
# max - capacitatea maxima
# dim - numarul de indivizi din populatie
#E: pop - populatia initiala
#   dim,nc,v,max:datele problemei - pentru transferuri in alte functii
def gen(fc,fv,max,dim):
    #citeste datele din fisierele cost si valoare
    c=np.genfromtxt(fc)
    v=np.genfromtxt(fv)
    #n=dimensiunea problemei
    n=len(c)
    #lucreaza cu populatia ca lista de dim elemente - liste cu cate n+1 indivizi
    pop=[]
    for i in range(dim):
        gata=False
        while gata == False:
            #genereaza candidatul x cu elemente 0,1
            x=np.random.randint(0,2,n)
            gata,val=ok(x,n,c,v,max)
        #am gasit o solutie candidat fezabila, in data de tip ndarray (vector) x
        # x este transformat in lista
        x=list(x)
        # adauga valoarea
        x=x+[val]
        #adauga la populatie noul individ cu valoarea f. obiectiv - adauga inca o lista cu n+1 elemente ca element al listei pop
        pop=pop+[x]
    return pop,n,c,v


#crossover pe populatia de parinti pop, de dimensiune dimx(n+1)
# I: pop,dim,n - ca mai sus
#     c, v, max - datele problemei
#     pc- probabilitatea de crossover
#E: po - populatia copiilor
# este implementata recombinarea asexuata
def crossover_populatie(pop,dim,n,c,v,max,pc):
    po=[]
    #populatia este parcursa astfel incat sunt selectati indivizii 0,1 apoi 2,3 s.a.m.d
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[i]
        y = pop[i+1]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - unipunct
            c1,c2=crossover_unipunct(x[:n],y[:n],n)
            # crossover x cu y - uniform: mai potrivit aici
            #c1,c2=crossover_uniform(x[:n] ,y[:n] ,n)
            fez1, val1 = ok(c1, n, c, v, max)
            if fez1:
               c1=c1+[val1]
            else:
                c1 = x.copy()
            fez2, val2 = ok(c2, n, c, v, max)
            if fez2:
               c2=c2+[val2]
            else:
                c2 = y.copy()
        else:
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
        #copiaza rezultatul in populatia urmasilor
        po = po+[c1]
        po = po+[c2]
    return po



#mutatie asupra populatiei de copii
# I:pop,dim,n - populatia de dimensiuni dimx(n+1)
#   pm - probabilitatea de mutatie
#E: - mpop - populatia mutata
def mutatie_populatie(pop,dim,n,c,v,max,pm):
    #copiem populatia in rezultat
    mpop=pop.copy()
    for i in range(dim):
        #copiem in x individul i din populatia intrare
        x=pop[i][:n].copy()
        for j in range(n):
            #genereaza aleator daca se face mutatie in individul i gena j
            r=np.random.uniform(0,1)
            if r<=pm:
                #mutatie
                x[j]=m_binar(x[j])
        #individul rezultat sufera posibil mai multe mutatii
        #daca este fezabil, este pastrat
        fez, val = ok(x, n, c, v, max)
        if fez:
            x=x+[val]
            mpop[i]=x.copy()
    return mpop


def arata(sol,v):
    # vizualizare rezultate Rucsac 0-1
    n=len(sol)
    t=len(v)
    val=max(v)
    print("Cea mai buna valoare calculată: ",val)
    print("Alegerea corespunzatoare este: ",sol)
    fig=grafic.figure()
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Valoarea")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")
    fig.show()



##ALGORITMUL GENETIC PENTRU REZOLVAREA PROBLEMEI RUCSACULUI 0-1
#I: fc,fv - fisierele cu costuri/valori
#   dim - dimensiunea unei populatii
#   NMAX - numarul maxim de simulari ale unei evolutii
#   pc - probabilitatea de crossover
#   pm - probabilitatea de mutatie
#
#E: sol - solutia calculata de GA
#   val - maximul functiei fitness
def GA(fc,fv,max,dim,NMAX,pc,pm):
    #generarea populatiei la momentul initial
    pop,n,c,v=gen(fc, fv, max, dim)
    #initializari pentru GA
    it=0
    gata=False
    nrm=1
    # impartirea populatiei in lista indivizilor si lista calitatilor
    # lista indivizilor
    lp = []
    # lista calitatilor
    lval = []
    for i in range(dim):
        individ = pop[i][:n]
        lp = lp + [individ]
        lval = lval + [pop[i][n]]
    #in istoric_v pastram cel mai bun cost din populatia curenta, la fiecare moment al evolutiei
    istoric_v=[np.max(lval)]
    # evolutia - cat timp
    #                - nu am depasit NMAX  si
    #                - populatia are macar 2 indivizi cu calitati diferite  si
    #                - in ultimele NMAX/2 iteratii s-a schimbat macar o data calitatea cea mai buna
    while it<NMAX and not gata:
        #SELECTIA PARINTILOR
        spop, sval = ruleta(lp, lval, dim, n)
        # constituirea populatiei cu dim liste fiecare cu n+1 valori
        rez = []
        for i in range(dim):
            x = [None] * (n + 1)
            x[:n] = spop[i].copy()
            x[n] = sval[i]
            rez = rez + [x]
        # RECOMBINAREA
        pop_o = crossover_populatie(rez, dim, n, c, v, max, pc)
        # MUTATIA
        pop_mo = mutatie_populatie(pop_o,dim,n,c,v,max,pm)
        # impartirea populatiei urmasilor in lista indivizilor si lista calitatilor
        # lista indivizilor
        lpo = []
        # lista calitatilor
        lvalo = []
        for i in range(dim):
            individ = pop_mo[i][:n]
            lpo = lpo + [individ]
            lvalo = lvalo + [pop_mo[i][n]]
        # SELECTIA GENERATIEI URMATOARE
        newpop, newval = elitism(lp, lval, lpo, lvalo, dim)
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim==istoric_v[it]:
            nrm=nrm+1
        else:
            nrm=1
        if maxim==minim or nrm==int(NMAX/2):
            gata=True
        else:
            it=it+1
        istoric_v.append(np.max(newval))
        lp =newpop.copy()
        lval =newval.copy()
    #transformarea din lista in vector pentru a aplica functia where corect
    lval=np.array(lval)
    i_sol=np.argmax(lval)
    sol=lp[i_sol]
    val=maxim
    arata(sol,istoric_v)
    return sol,val

#import Rucsac01 as r1
#sol,val=r1.GA("cost.txt","valoare.txt",50,20,100,0.8,0.1)