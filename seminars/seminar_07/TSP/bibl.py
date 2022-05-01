import numpy as np
import matplotlib.pyplot as grafic


#f. obiectiv
def foTSP(p,c,n):
    val = 0
    for i in range(n - 1):
        val = val + c[p[i]][p[i+1]]
    val = val+c[p[0]][p[n-1]]
    return 100/val


#genereaza populatia initiala
#I:
# fc - numele fisierului costurilor
# dim - numarul de indivizi din populatie
#E: lista cu 2 componente [pop,val] - populatia initiala si vectorul valorilor
#  pentru testul crossover si matricea c
def gen(fc,dim):
    #citeste datele din fisierul nxn al costurilor
    c=np.genfromtxt(fc)
    #n=dimensiunea problemei
    n = len(c)
    #defineste o variabila ndarray dimx(n+1) cu toate elementele 0
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        #genereaza candidatul permutare cu n elemente
        pop[i] = np.random.permutation(n)
        # evalueaza candidat
        val[i] = foTSP(pop[i,:n],c,n)
    #[pop,val]=lista L cu primul element populatia, al doilea element vectorul valorilor
    #ca referire, pop=L[0], val=L[1]
    return [pop, val],c

def crossover_PMX(x,y,n):
    p=np.random.randint(0,n,2)
    while p[0]==p[1]:
        p=np.random.randint(0,n,2)
    p1=np.min(p)
    p2=np.max(p)
    c1=PMX(x,y,n,p1,p2)
    c2=PMX(y,x,n,p1,p2)
    return c1,c2

def PMX(x,y,n,p1,p2):
    c=-np.ones(n,dtype="int")
    c[p1:p2+1]=x[p1:p2+1]
    for i in range(p1,p2+1):
        a=y[i]
        if a not in c:
            plasat=False
            curent=i
            while not plasat:
                b=x[curent]
                [poz]=[k for k in range(n) if y[k]==b]
                if c[poz]==-1:
                    c[poz]=a
                    plasat=True
                else:
                    curent=poz
    vn=[y[i] for i in range(n) if y[i] not in c]
    pl=[i for i in range(n) if c[i]==-1]
    for i in range(len(vn)):
        c[pl[i]]=vn[i]
    return c

def crossover_populatie(lparinti,dim,n,pc,c):
    parinti=lparinti[0]
    valori=lparinti[1]
    copii=np.zeros([dim,n],dtype="int")
    valc=np.zeros(dim)
    noip=np.random.permutation(dim)
    for i in range(0,dim-1,2):
        x=parinti[noip[i]]
        y=parinti[noip[i+1]]
        r=np.random.uniform(0,1)
        if r<=pc:
            c1,c2=crossover_PMX(x,y,n)
            v1=foTSP(c1,c,n)
            v2=foTSP(c2,c,n)
        else:
            c1=x.copy()
            c2=y.copy()
            v1=valori[noip[i]]
            v2=valori[noip[i+1]]
        copii[noip[i]]=c1.copy()
        copii[noip[i+1]]=c2.copy()
        valc[noip[i]]=v1
        valc[noip[i+1]]=v2
    deseneaza(valori,valc,dim,noip)
    return [copii,valc]

def deseneaza(vp,vc,dim,noip):
    #x=range(dim)
    x=[noip[i] for i in range(dim)]
    vp1=[vp[noip[i]] for i in range(dim)]
    vc1=[vc[noip[i]] for i in range (dim)]
    grafic.plot(x,vp1,"go",markersize=14,label="Parinti")
    grafic.plot(x,vc1,"ro",markersize="11",label="Copii")
    grafic.legend(loc="lower left")
    grafic.xlabel("Indicii din populatii")
    grafic.ylabel("Fitness indivizi")
    grafic.show()



