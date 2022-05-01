import numpy as np

#PARENT SELECTION
#INPUT POPULATION/ SELECTED POPULATION - REPRESENTATION MATRIX AND FITNESS VECTOR

#K MEMBERS TOURNEMENT SELECTION
#I: pop,qual,dim,n,k - population matrix, fitness vector,  population size, k-members
#E: spop,squal - selected population, fitness vector
def turneu(pop,qual,dim,n,k):
    spop=pop.copy()
    squal=np.zeros(dim)
    for it in range(dim):
        poz=np.random.randint(0,dim,k)
        v=[qual[poz[i]] for i in range(k)]
        M=max(v)
        p=np.where(v==M)
        imax=p[0][0]
        isel=poz[imax]
        spop[it][:]=pop[isel][:]
        squal[it]=qual[isel]
    return spop, squal


# ROULETTE WHEEL & SUS MECHANISMS
#
# FPS selection probability
# I: qual,dim - fitness vector of size dim
# E: qfps - cumulated distribution
def fps(qual,dim):
    fps=np.zeros(dim)
    suma=np.sum(qual)
    for i in range (dim):
        fps[i] = qual[i]/suma
    qfps=fps.copy()
    for i in range(1, dim):
        qfps[i]=qfps[i-1]+fps[i]
    return qfps

#SIGMA SCALING FPS
# I: qual,dim - fitness vector of size dim
# E: qfps - cumulated distribution
def sigmafps(qual, dim):
    med=np.mean(qual)
    var=np.std(qual)
    newq=[max(0,qual[i]-(med-2*var)) for i in range(dim)]
    if np.sum(newq)==0:
        qfps=fps(qual,dim)
    else:
        qfps=fps(newq,dim)
    return qfps


# RANKING SELECTION - LINEAR
# I: dim - population size
#    s - selection pressure
# E: qlr - cumulated distribution
def lrang(dim,s):
    lr=[(2-s)/dim+2*(i+1)*(s-1)/(dim*(dim+1)) for i in range(dim)]
    qlr=lr.copy()
    for i in range(1, dim):
        qlr[i]=qlr[i-1]+qlr[i]
    return np.array(qlr)

# ROULETTE WHEEL -SIGMA-SCALING FPS
#I: pop,qual,dim,n- population matrix, fitness vector,  population size
#E: spop,squal - selected population and fitness vector


def ruleta(pop,qual,dim,n):
    spop=pop.copy()
    squal=np.zeros(dim)
    qfps=sigmafps(qual,dim)
    for it in range(dim):
        r=np.random.uniform(0,1)
        poz=np.where(qfps>=r)
        isel=poz[0][0]
        spop[it][:]=pop[isel][:]
        squal[it]=qual[isel]
    return spop, squal

# sort pop based on qual, ascending order
#I: pop,qual,dim- population matrix, fitness vector,  population size
# E: pops, quals - sorted versions
def sort_pop(pop,qual):
    indici=np.argsort(qual)
    pops=pop[indici]
    quals=qual[indici]
    return pops,quals

#ROULETTE WHELE - LINEAR RANKING SELECTION
# THE INPUT POPULATION IS SORTED
# I: pop,qual,dim,n,s - population matrix, fitness vector,  population size pop-dim x n, selection pressure
#E: spop,squal - selected population and fitness vector
def ruleta_rang(pop,qual,dim,n,s):
    spop=pop.copy()
    squal=np.zeros(dim)
    qr=lrang(dim,s)
    for it in range(dim):
        r=np.random.uniform(0,1)
        poz=np.where(qr>=r)
        isel=poz[0][0]
        spop[it][:]=pop[isel][:]
        squal[it]=qual[isel]
    return spop, squal


#SUS - LINEAR RANKING SELECTION
# THE INPUT POPULATION IS NOT SORTED
# I: pop,qual,dim,n,s - population matrix, fitness vector,  population size pop-dim x n, selection pressure
#E: pop_s,qual_s - selected population and fitness vector
def SUS_rangl(pop,qual,dim,n,s):
    pop,qual=sort_pop(pop, qual)
    spop=pop.copy()
    squal=np.zeros(dim)
    qfps=lrang(dim,s)
    r=np.random.uniform(0,1/dim)
    k,i=0,0
    while (k<dim):
        while (r<=qfps[i]):
            spop[k][:]=pop[i][:]
            squal[k]=qual[i]
            r=r+1/dim
            k=k+1
        i=i+1
    newp = np.random.permutation(dim)
    pop_r = spop[newp]
    qual_r = squal[newp]
    return pop_r, qual_r

#SUS - SIGMA-SCALING FPS
# I: pop,qual,dim,n - population matrix, fitness vector,  population size pop-dim x n
#E: pop_s,qual_s - selected population and fitness vector
def SUS(pop,qual,dim,n):
    spop=pop.copy()
    squal=np.zeros(dim)
    qfps=sigmafps(qual,dim)
    r=np.random.uniform(0,1/dim)
    k,i=0,0
    while (k<dim):
        while (r<=qfps[i]):
            spop[k][:]=pop[i][:]
            squal[k]=qual[i]
            r=r+1/dim
            k=k+1
        i=i+1
    return spop, squal


#SURVIVOR SELECTION

#ELITISM
#I: pop_c,qual_c,pop_mo,qual_mo - current population & fitness values, mutated offspring & fitness vector
#E: pop,qual - selected population, fitness vector
def elitism(pop_c,qual_c,pop_mo,qual_mo,dim):
    pop=np.copy(pop_mo)
    qual=np.copy(qual_mo)
    max_c=np.max(qual_c)
    max_mo=np.max(qual_mo)
    if max_c>max_mo:
        p1=np.where(qual_c==max_c)
        imax=p1[0][0]
        ir=np.random.randint(dim)
        pop[ir]=pop_c[imax].copy()
        qual[ir]=max_c
    return pop,qual



#GENITOR
#I: pop_c,qual_c,pop_mo,qual_mo, dim, dimc - current population & fitness vector, mutated offspring & fitness vector, populations sizes
#E: pop_r,qual_r - selected population, fitness vector

def genitor(pop_c,qual_c,pop_mo,qual_mo,dim,dimc):
    pops,quals=sort_pop(pop_c,qual_c)
    pop=pops.copy()
    qual=quals.copy()
    for i in range(dimc):
        pop[i]=pop_mo[i].copy()
        qual[i]=qual_mo[i]
    newp=np.random.permutation(dim)
    pop_r=pop[newp]
    qual_r=qual[newp]
    return pop_r,qual_r

#DETERMINISTIC FITNESS BASED SELECTION

#I: pop_c,qual_c,pop_mo,qual_mo, dim, L - current population & fitness vector, mutated offspring & fitness vector, populations sizes
#E: pop_r,qual_r - selected population, fitness vector

def sel_det(pop_c,qual_c,pop_mo,qual_mo,dim,L):
    pop=np.append(pop_c,pop_mo)
    pop.resize(2*dim,L)
    qual=np.append(qual_c,qual_mo)
    p,q=sort_pop(pop, qual)
    pop_1=p[dim:2*dim].copy()
    qual_1=q[dim:2*dim].copy()
    newp = np.random.permutation(dim)
    pop_r = pop_1[newp]
    qual_r = qual_1[newp]
    return pop_r,qual_r