import numpy as np
import matplotlib.pyplot as grafic
from FunctiiCrossoverIndivizi import crossover_PMX
from FunctiiMutatieIndivizi import m_perm_inversiune
from FunctiiSelectii import elitism, SUS

#f. obiectiv
def foTSP(p,c,n):
    val = 0
    for i in range(n - 1):
        val = val + c[p[i]][p[i+1]]
        #val+=c[p[i],p[i+1]]
    val = val+c[p[0]][p[n-1]]
    return 100/val

#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: lista cu 2 componente [pop,val] - populatia initiala si vectorul valorilor
def gen(fc,dim):
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    #n=dimensiunea problemei
    n = len(c)
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c,n)
    #[pop,val]=lista L cu primul element populatia, al doilea element vectorul valorilor
    #ca referire, pop=L[0], val=L[1]
    return [pop, val], c, n

#crossover pe populatia de parinti pop, de dimensiune dimxn
# I: l,dim,n - l=[pop,valori], ca in functia de generare
#     c - datele problemei
#     pc- probabilitatea de crossover
#E: [po,val] - populatia copiilor, insotita de calitati
# este implementata recombinarea asexuata
def crossover(l,dim,n,c,pc):
    pop=l[0]
    valori=l[1]
    # initializeaza populatia de copii, po, cu matricea cu elementele 0
    po=np.zeros((dim,n),dtype=int)
    # initializeaza valorile populatiei de copii, val, cu matricea cu elementele 0
    val=np.zeros(dim,dtype=float)
    #populatia este parcursa astfel incat sunt selectati aleator cate 2 indivizi - matricea este accesata dupa o permutare a multimii de linii 0,2,...,dim-1
    poz=np.random.permutation(dim)
    #sau populatia este parcursa astfel incat sunt selectati 2 indivizi consecutivi
    #poz=range(dim) #- pentru pastrarea ordinii
    for i in range(0,dim-1,2):
        #selecteaza parintii
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        if r<=pc:
            # crossover x cu y - PMX - potrivit pentru probleme cu dependenta de adiacenta
            c1,c2 = crossover_PMX(x,y,n)
            v1=foTSP(c1,c,n)
            v2=foTSP(c2,c,n)
        else:
            # recombinare asexuata
            c1 = x.copy()
            c2 = y.copy()
            v1=valori[poz[i]]
            v2=valori[poz[i+1]]
        #copiaza rezultatul in populatia urmasilor
        po[i] = np.copy(c1)
        po[i+1] = np.copy(c2)
        val[i]=v1
        val[i+1]=v2
    return [po, val]

#MUTATIE
 # operatia de mutatie a descendentilor obtinuti din recombinare
    # I: desc - [po,vo] - populatia copiilor insoltita de vectorul calitatilor
    #   dim,n - dimensiunile
    #    pm - probabilitatea de mutatie
    #    c - matricea costurilor
    # E: descm - [mpo,mvo] - indivizii obtinuti
def mutatie(desc,dim,n,c,pm):
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
    return [mpo,mvo]

def arata(sol,v):
    # vizualizare rezultate TSP
    # I: x - permutarea care defineste asezarea
    # E: -

    n=len(sol)
    t=len(v)
    cost=min(v)
    print("Cea mai mică distanță calculată: ",cost)
    print("Un drum cu costul ",cost," este: ",sol)

    fig=grafic.figure()
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Costul")
    grafic.xlabel("Generația")
    grafic.title("Evoluția calității celui mai bun individ din fiecare generație")

    fig.show()

def GA_TSP(fc,dim,NMAX,pc,pm):
    # populatia initiala
    lpop,c,n=gen(fc,dim)
    pop=lpop[0]
    qual=lpop[1]

    #alte operatii de initializare
    it=0
    contor=1
    gata=False
    istoric=[100/np.max(qual)]

    #itertiile
    while it<NMAX and not gata:
        #1. Selectia parintilor
        pop_p,qual_p=SUS(pop,qual,dim,n)
        #2. Recombinare
        copii=crossover([pop_p,qual_p],dim,n,c,pc)
        #3. Mutatia
        copiim=mutatie(copii,dim,n,c,pm)
        #4. Selectia supravietuitorilor
        pop_u,qual_u=elitism(pop,qual,copiim[0],copiim[1],dim)

        #alte operatii - controlul conditiei de continuare + istoric
        maxim=np.max(qual_u)
        minim=np.min(qual)
        if 100/maxim==istoric[it]:
            contor+=1
        else:
            contor=1
        if maxim==minim or contor==int(NMAX/3):
            gata=True
        else:
            it=it+1
        istoric=istoric+[100/maxim]

        #5. Inlocuirea efectiva a populatiei curente
        pop=pop_u.copy()
        qual=qual_u.copy()
    cost=100/maxim
    index=np.where(qual==maxim)
    solutie=pop[index[0][0]]
    arata(solutie,istoric)
    return solutie, cost