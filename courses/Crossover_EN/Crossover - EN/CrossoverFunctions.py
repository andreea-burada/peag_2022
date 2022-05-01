import numpy as np


# CROSSOVER - BINARY/INTEGER VECTORS
#
# one-point crossover
# I :x,y,n - input vectors and their length
#E: c1,c2 - resulted children
def crossover_unipunct(x,y,n):
    #choose the random crossover point in the range 1,..., n-1
    i = np.random.randint(0,n)
    c1=x.copy()
    c2=y.copy()
    # first child
    c1[0:i] = x[0:i]
    c1[i:n] = y[i:n]
    # second child
    c2[0:i] = y[0:i]
    c2[i:n] = x[i:n]
    return c1,c2


# uniform crossover
# I :x,y,n - input vectors and their length
#E: c1,c2 - resulted children
def crossover_uniform(x,y,n):
    #set the initial values of the children
    c1=x.copy()
    c2=y.copy()
    for i in range(n):
        r = np.random.randint(0,2)
        # inverse the alleles
        if r == 1:
            c1[i] = y[i]
            c2[i] = x[i]
    return c1,c2



# CROSSOVER PERMUTATIONS - a n sized permutation is an arrangement of {0,1,...,n-1}

#PMX
#I: x,y,n - input permutations, their size
#E: c1,c2 - resulted children (permutations)
def crossover_PMX(x,y,n):
    #select the random crossover sequence
    poz=np.random.randint(0,n,2)
    while poz[0]==poz[1]:
        poz=np.random.randint(0,n,2)
    p1=np.min(poz)
    p2=np.max(poz)
    c1=PMX(x,y,n,p1,p2)
    c2=PMX(y,x,n,p1,p2)
    return c1,c2

#compute a child of x,y given the crossover sequence (p1,p2)
def PMX(x,y,n,p1,p2):
    #initialization
    c=-np.ones(n,dtype=int)
    #copy the crossover sequence
    c[p1:p2+1]=x[p1:p2+1]
    # analize the crossover sequence in y
    for i in range(p1,p2+1):
        # place a
        a=y[i]
        if a not in c:
            curent=i
            plasat=False
            while not plasat :
                b=x[curent]
                # poz = the position of b in y
                [poz]=[j for j in range(n) if y[j]==b]
                if c[poz]==-1 :
                    c[poz]=a
                    plasat=True
                else:
                    curent=poz
    # z = vector of the alleles in y yet not placed in c
    z=[y[i] for i in range(n) if y[i] not in c]
    # poz - the free positions in c
    poz=[i for i in range(n) if c[i]==-1]
    m=len(poz)
    for i in range(m):
        c[poz[i]]=z[i]
    return c


#OCX
#I: x,y,n - input permutations, their size
#E: c1,c2 - resulted children (permutations)
def crossover_OCX(x,y,n):
    #select the random crossover sequence
    poz=np.random.randint(0,n,2)
    while poz[0]==poz[1]:
        poz=np.random.randint(0,n,2)
    p1=np.min(poz)
    p2=np.max(poz)
    c1=OCX(x,y,n,p1,p2)
    c2=OCX(y,x,n,p1,p2)
    return c1,c2

#compute a child of x,y given the crossover sequence (p1,p2)
def OCX(x,y,n,p1,p2):
    c2=[x[i] for i in range(p1,p2+1)]
    z1=[y[i] for i in range(p2,n) if y[i] not in c2]
    z2=[y[i] for i in range(p2) if y[i] not in c2]
    z=np.append(z1,z2)
    c3=[z[i] for i in range(n-p2-1)]
    c1=[z[i] for i in range(n-p2-1,len(z))]
    #resulted child c
    c=np.append(c1,c2)
    c=np.append(c,c3)
    return c

#CX
#I: x,y,n - input permutations, their size
#E: c1,c2 - resulted children (permutations)
def crossover_CX(x,y,n):
    ciclu=cicluri(x,y,n)
    c1=x.copy()
    c2=y.copy()
    for i in range(n):
        cat, rest = np.divmod(ciclu[i], 2)
        #interchange the even cycles
        #first cycle is odd
        if not rest:
            c1[i]=y[i]
            c2[i]=x[i]
    return c1,c2


def cicluri(x,y,n):
    #number of cycles
    index=1
    ciclu=np.zeros(n)
    gata=0
    while not gata:
        p=np.where(ciclu==0)
        #if there exists an unassigned gene
        if np.size(p):
            i=p[0][0]
            a=x[i]
            ciclu[i]=index
            b=y[i]
            while b!=a:
                r=np.where(x==b)
                j=r[0][0]
                ciclu[j]=index
                b=y[j]
            index+=1
        else:
            gata=1
    return ciclu


#EDGE CROSSOVER

#compute the edge table
def constr_tabel(x,y,n):
    muchii=[0]*n
    x1=np.zeros(n+2, dtype='int')
    x1[1:n+1]=x[:]
    x1[0]=x[n-1]
    x1[n+1]=x[0]
    y1 = np.zeros(n + 2, dtype='int')
    y1[1:n + 1] = y[:]
    y1[0] = y[n - 1]
    y1[n + 1] = y[0]
    for i in range(1,n+1):
        a=x1[i]
        r=np.where(y==a)
        j=r[0][0]+1
        vx={x1[i-1],x1[i+1]}
        vy={y1[j-1],y1[j+1]}
        dx=vx-vy
        dy=vy-vx
        cxy=vx & vy
        lcxy=list(cxy)
        dx=list(dx)
        dy=list(dy)
        for j in range(len(lcxy)):
            lcxy[j]=str(lcxy[j])+'+'
        for j in range(len(dx)):
            dx[j]=str(dx[j])
        for j in range(len(dy)):
            dy[j]=str(dy[j])
        muchii[a]=lcxy+list(dx)+list(dy)
    return muchii

# delete an element
def sterge(x,a):
    p=[i for i in range(len(x)) if x[i]==a]
    if len(p):
        del(x[p[0]])
    return x

#select the allele to be placed
def alege(lp,muchii,n):
    dim=len(lp)
    lliste=np.zeros(dim)
    gata=0
    k=0
    while k<dim and not gata:
        a=str(lp[k])+'+'
        i=0
        while i<n and not gata :
            l=muchii[i]
            p=[j for j in range(len(l)) if l[j]==a]
            if len(p):
                gata=1
                alela=lp[k]
            else:
                p=[j for j in range(len(l)) if l[j]==str(lp[k])]
                i=i+1
                lliste[k]=len(l)
        if not gata:
            k=k+1
    if not gata:
        x=[j for j in range(dim) if lliste[j]==min(lliste)]
        alela=lp[x[0]]
    return alela

# ECX - Edge crossover
def ECX(x,y,n):
    muchii=constr_tabel(x,y,n)
    z=np.zeros(n, dtype='int')
    ales=np.zeros(n)
    lp=[x[0]]
    for i in range(n):
        print(muchii)
        if len(lp)==0:
            a=np.random.randint(n)
            while ales[a]:
                a = np.random.randint(n)
        else:
            if len(lp)>1:
                a=alege(lp,muchii,n)
            else:
                a=lp[0]
        z[i]=a
        ales[a]=1
        print(a)
        for k in range(n):
            sterge(muchii[k],str(a))
            sterge(muchii[k],str(a)+'+')
        lp=[int(muchii[a][i][0]) for i in range(len(muchii[a]))]
    return z

#APEL ECX
#import numpy as np
#import FunctiiCrossoverIndivizi as c
#n=10
#x=np.random.permutation(n)
#y=np.random.permutation(n)
#z=c.ECX(y,x,10)


# CROSSOVER - REAL-VALUED VECTORS

# single arithmetic crossover
#I: x,y,n - input vectors, size
#   alpha - weigth
#E: c1,c2 - resulted children

def crossover_singular (x, y, n,alpha):
    i = np.random.randint(0,n)
    c1 = x.copy()
    c2 = y.copy()
    c1[i]=(alpha*x[i]+(1-alpha)*y[i])
    c2[i] = (alpha * y[i] + (1 - alpha) * x[i])
    return c1, c2


# simple arithmetic crossover
#I: x,y,n - input vectors, size
#E: c1,c2 - resulted children
def crossover_simplu (x, y, n,alpha):
    i = np.random.randint(0,n)
    c1 = x.copy()
    c2 = y.copy()
    for j in range(i,n):
        c1[j]=(alpha*x[j]+(1-alpha)*y[j])
        c2[j] = (alpha * y[j] + (1 - alpha) * x[j])
    return c1, c2

# whole arithmetic crossover
#I: x,y,n - input vectors, size
#   alpha - weigth
#E: c1,c2 - resulted children
def crossover_total (x, y, n,alpha):
    c1 = x.copy()
    c2 = y.copy()
    for j in range(n):
        c1[j]=(alpha*x[j]+(1-alpha)*y[j])
        c2[j] = (alpha * y[j] + (1 - alpha) * x[j])
    return c1, c2
