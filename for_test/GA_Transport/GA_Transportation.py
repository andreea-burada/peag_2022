import numpy
import matplotlib.pyplot as grafic
from Selection import SUS, elitism
from CrossoverFunctions import crossover_CX
from MutationFunctions import m_perm_interschimbare


def GA_Transport(fo,fc,fcost,dim,nmax,pr,pm):
    # GA for solving the balanced transportation problem

    # phenotype: transportation plan matrix TP
    # genotype: the order in which the elements of TP  are assigned <=> permutation, UNCONSTRAINED PROBLEM
    # I: fo - supply file name (text, 1xm)
    #    fc - demand file name (text, 1 x n)
    #    fcost - cost file name (text, m x n)
    #    dim - population size
    #    nmax - maximum number of simulations
    #    pr - recombination probability
    #    pm - mutation probability
    # E: sol - solution
    #    cost - transportation cost
    #
    #  examples
    #    import GA_Transportation as GTR
    #    s,c=GTR.GA_Transport('T_oferta3.txt','T_cerere3.txt','T_costuri3.txt',20,50,0.8,0.1)
    # The best computed cost: 2316
    # An optimal solution:
    #      6     0     9     0     0
    #      2     0     0    10     8
    #      3    12     0     0     0
    #
    #    s,c=GTR.GA_Transport('T_oferta.txt','T_cerere.txt','T_Costuri.txt',300,300,0.85,0.2)
    # The best computed cost: 39736.1
    # An optimal solution:
    #      0    40     0     0     0     0     0     0     0    60
    #     60     0     0    90     0     0     0     0     0     0
    #      0     0     0     0     0    20     0     0    60     0
    #      0     0    10     0     0    10    70     0     0     0
    #      0     0     0     0     0    10     0     0     0     0
    #      0     0     0     0     0     0    10    50     0     0
    #     10     0     0     0     0    70     0     0     0     0
    #      0     0     0     0    20     0    30     0     0     0
    #      0     0    20     0     0     0     0     0     0     0
    #      0     0     0     0     0    70     0     0     0     0

    # An optimal solution:
    #   70  30    0    0   0    0    0     0    0    0
    #   0   10   10   90   0    0    40    0    0    0
    #   0    0    0    0   0   20     0    0   60    0
    #   0    0    0    0   0    0    30    0    0   60
    #   0    0    0    0   0   10     0    0    0    0
    #   0    0    0    0   0    0    10   50    0    0
    #   0    0    0    0   0   80     0    0    0    0
    #   0    0    0    0  20    0    30    0    0    0
    #   0    0   20    0   0    0     0    0    0    0
    #   0    0    0     0   0   70     0    0    0    0

    # initializations
    oferta=numpy.genfromtxt(fo)
    cerere=numpy.genfromtxt(fc)
    costuri=numpy.genfromtxt(fcost)
    n=len(oferta)*len(cerere)


    # initial population
    pop=gen_pop(dim,oferta,cerere,costuri)
    v=[min(1000./pop[:,n])]


    ok=True
    t=0
    while t<nmax and ok:
        # parent selection
        sp,vp = SUS(pop[:,:n],pop[:,n],dim,n+1)
        parinti=numpy.zeros([dim,n+1])
        parinti[:,:n]=sp.copy()
        parinti[:,n]=vp.copy()
        # recombination
        desc = recombinare(parinti, pr, oferta,cerere,costuri)
        # mutation
        descm = mutatie(desc, pm, oferta,cerere,costuri)
        # survivor selection
        popn,valn = elitism(pop[:,:n],pop[:,n],descm[:,:n],descm[:,n],dim)
        pop = numpy.zeros([dim, n + 1])
        pop[:, :n] = popn.copy()
        pop[:, n] = valn.copy()

        # record the best computed solution
        vmax = min(1000./pop[:,n])
        i = numpy.argmin(pop[:, n])
        best = pop[i][:n]
        v.append(vmax)
        t+=1
        ok=max(pop[:,n])!=min(pop[:,n])

    print("The best cost: ",vmax)
    print("A transportation plan:")
    sol=gen_alocare(best,oferta,cerere)
    print(sol)
    fig=grafic.figure()
    grafic.plot(v)
    verificare(sol,oferta,cerere)
    return (sol,vmax)

def f_obiectiv(x,oferta,cerere,costuri):
    # the objective function

    # I:  x - a chromosome
    #    oferta, cerere - the supply vector, the demand vector
    #    costuri - the cost matrix (/unit)
    #    E: c - the fitness value of x (1000/transportation cost)

    a=gen_alocare(x,oferta,cerere)
    c=1000./numpy.sum(a*costuri)
    return c

def gen_alocare(permutare,oferta,cerere):
    # DECODING

    # I: permutare - genotype
    #    oferta, cerere - the supply vector, the demand vector
    # E: x -the transportation plan corresponding to x

    m=len(oferta)
    n=len(cerere)
    x=numpy.zeros((m,n))
    i=0
    OR=sum(oferta)      #the remaining total offer
    o_r=oferta.copy()   #the remaining supplies
    c_r=cerere.copy()   #the remaining demands
    while OR>0:
        lin,col=numpy.unravel_index(int(permutare[i]),(m,n))
        x[lin,col]=min([o_r[lin],c_r[col]])
        o_r[lin]-=x[lin,col]
        c_r[col]-=x[lin,col]
        OR-=x[lin,col]
        i+=1
    return x

def gen_pop(dim,oferta,cerere,costuri):
    # the computation of the initial population

    # I: dim - population size
    #   oferta, cerere - the supply vector, the demand vector
    #   costuri - the cost matrix (/unit)
    # E: pop - populatia generata

    m=len(oferta)
    n=len(cerere)
    pop=numpy.zeros((dim,m*n+1))
    for i in range(dim):
        x=numpy.random.permutation(m*n)
        pop[i,:-1]=x # =pop[i,:m*n]
        pop[i,-1]=f_obiectiv(x,oferta,cerere,costuri)
    return(pop)

def recombinare(parinti,pr,oferta,cerere,costuri):
    # RECOMBINATION

    # I: parinti - the parents
    #    pr - recombination probability
    #    oferta, cerere, costuri
    # E: desc - the children

    dim,n=numpy.shape(parinti)
    desc=parinti.copy()
    #scramble the parents to randomly select pairs of individuals
    perechi=numpy.random.permutation(dim)
    for i in range(0,dim,2):
        x = parinti[perechi[i], :n - 1]
        y = parinti[perechi[i + 1], :n - 1]
        r=numpy.random.uniform(0,1)
        if r<=pr:
            d1, d2 = crossover_CX(x, y, n-1)
            desc[i, :n - 1] = d1
            desc[i][n - 1] = f_obiectiv(d1, oferta,cerere,costuri)
            desc[i + 1, :n - 1] = d2
            desc[i + 1][n - 1] = f_obiectiv(d2, oferta,cerere,costuri)
    return desc

def mutatie(desc,pm,oferta,cerere,costuri):
    # MUTATION

    # I: desc - offspring
    #    pm - mutation probability
    #    oferta,cerere,costuri
    # E: descm - mutated offspring

    dim,n=numpy.shape(desc)
    descm=desc.copy()
    for i in range(dim):
        x=descm[i,:n-1]
        r=numpy.random.uniform(0,1)
        if r<=pm:
            y=m_perm_interschimbare(x,n-1)
            descm[i,:n-1]=y
            descm[i,n-1]=f_obiectiv(y,oferta,cerere,costuri)
    return descm

def verificare(sol,oferta,cerere):
    # check the correctness of the solution

    # I: sol - the solution
    #    oferta,cerere - supplies and demands
    # E: -

    o_r=oferta-numpy.sum(sol,axis=1)
    c_r=cerere-numpy.sum(sol,axis=0)

    mino=min(o_r); maxo=max(o_r)
    minc=min(c_r); maxc=max(c_r)
    print("The remaining supply:", o_r)
    if mino<0:
        print("Error: it consumes more than available")
    if maxo>0:
        print("Error: it consumes less than available")
    if mino==0 and maxo==0:
        print("The supplies are consumed")

    print("The remaining demand:", c_r)
    if minc<0:
        print("Error: it is transported more than required")
    if maxc>0:
        print("Error: it is transported less than required")
    if minc==0 and maxc==0:
        print("The demand is covered")

