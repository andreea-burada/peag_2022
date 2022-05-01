import numpy
import matplotlib.pyplot as grafic

def fitness(x,val,cost,cmax):
    v=numpy.dot(val,x)
    # c= x[0]*v[0]+x[1]*v[1]+...+x[n-1]*v[n-1], n=len(x), the vector size
    c=numpy.dot(cost,x)
    return c<=cmax, v

def pop_ini(dim,n,val,cost,cmax):
    # compute the initial population
    # I: dim - population size
    #      n - number of objects
    #    val -the value vector
    #    cost - the cost vector
    #    cmax - maximum cost
    # E: pop,fit - the resulted population, the fitness values

    pop=numpy.zeros((dim, n),dtype="int")
    fit=numpy.zeros(dim, dtype="float")
    i=0
    while i<dim:
        x=numpy.random.randint(0, 2, n)
        ok,v = fitness(x,val,cost,cmax)
        if ok:
            pop[i]=x
            fit[i]=v
            i+=1
    return pop, fit

def mutation(x, poz):
    # the mutation operator
    # I: x - the input individual
    #    poz - the gene
    # E: y - the resulted individual

    y=x.copy()
    y[poz]=1-x[poz]
    return y

def mutation_pop(children,fit,dim,n,pm,val,cost,cmax):
    # mutate the children population
    # I: children, fit, dim, n -  children population, fitness values, sizes
    #    pm - mutation probability
    #    val,cost - value vector, cost vector
    #    cmax - maximum cost
    # E: new, fitn - mutated offspring, fitness values
    new=children
    fitn=fit
    for i in range(dim):
        r=numpy.random.uniform(0,1)
        if r<pm:
            poz = numpy.random.randint(n)
            x = new[i]
            y = mutation(x, poz)
            f,v=fitness(y,val,cost,cmax)
            if f:
                new[i] = y
                fitn[i]=v
    return new, fitn


def crossover(x1,x2,poz):
    # crossover operator

    # I: x1, x2 - parents
    #    poz - the gene
    # E: y1, y2 - children
    y1=x1.copy()
    y2=x2.copy()
    y1[poz:]=x2[poz:]
    y2[poz:]=x1[poz:]
    return y1, y2

def crossover_pop(parents,fitp,dim,n,pc,val,cost,cmax):
    # recombine parents to get the children population
    # I: parents, fitp, dim, n -  parent population, fitness values, sizes
    #    pc - crossover probability
    #    val,cost - value vector, cost vector
    #    cmax - maximum cost
    # E: new, fitn - offspring, fitness values

    new = numpy.zeros((dim, n), dtype="int")
    fitn = numpy.zeros(dim, dtype="float")
    # recombination
    for i in range(0, dim, 2):
        p1 = numpy.random.randint(dim)
        x1 = parents[p1]
        p2 = p1
        while p2 == p1:
            p2 = numpy.random.randint(dim)
        x2 = parents[p2]
        r = numpy.random.uniform(0, 1)
        if r < pc:
            poz = numpy.random.randint(n)
            y1, y2 = crossover(x1, x2, poz)
            f1, v1 = fitness(y1, val, cost, cmax)
            f2, v2 = fitness(y2, val, cost, cmax)
            feasible = f1 and f2
            if feasible:
                new[i] = y1
                fitn[i] = v1
                new[i + 1] = y2
                fitn[i + 1] = v2
            else:
                new[i] = parents[p1]
                new[i + 1] = parents[p2]
                fitn[i] = fitp[p1]
                fitn[i + 1] = fitp[p2]
        else:
            new[i] = parents[p1]
            new[i + 1] = parents[p2]
            fitn[i] = fitp[p1]
            fitn[i + 1] = fitp[p2]
    return new, fitn

def parent_sel(pop,fit,dim,n):
    # parent selection - tournament

    # I: pop, fit, dim, n -  current population, fitness values, sizes
    # E: parents, fitp - selected mating pool, fitness values

    parents=numpy.zeros((dim,n),dtype="int")
    fitp = numpy.zeros(dim, dtype="float")
    for i in range(dim):
        p1=numpy.random.randint(dim)
        p2=numpy.random.randint(dim)
        while p1==p2:
            p2=numpy.random.randint(dim)
        if fit[p1]>fit[p2]:
            parents[i]=pop[p1].copy()
            fitp[i]=fit[p1]
        else:
            parents[i] = pop[p2].copy()
            fitp[i] = fit[p2]
    return parents, fitp

def evolution(pop,fit,dim,n,pc,pm,val,cost,cmax):
    # evolution stage

    # I: pop, fit, dim, n - current population, fitness values, sizes
    #    pc - probability of crossover
    #    pm - probability of mutation
    #    val - value vector
    #    cost - cost vector
    #    cmax - maximum cost
    # E: new, fitn - survivors, fitness values

    # parent selection
    parents,fitp=parent_sel(pop,fit,dim,n)
    # crossover
    new,fitn=crossover_pop(parents,fitp,dim,n,pc,val,cost,cmax)
    # mutation
    newg, fitng=mutation_pop(new, fitn, dim, n, pm, val, cost, cmax)
    # the survivors = the mutated children
    return newg, fitng

def EA(namec,namev,cmax,dim,pc,pm,Nmax):
    # EA

    # I: namec, namev - cost file and value file
    #    cmax - maximum cost
    #    dim - population size
    #    pc - crossover probability
    #    pm - mutation probability
    #    Nmax - maximum number of simulations
    # E: sol - computed solution
    #    maximum - fitness of sol

    cost=numpy.genfromtxt(namec)
    val=numpy.genfromtxt(namev)
    n=len(val)
    pop,fit=pop_ini(dim,n,val,cost,cmax)
    fitini=fit
    for i in range(Nmax):
        pop, fit=evolution(pop,fit,dim,n,pc,pm,val,cost,cmax)
        if i==3:
            fit5=fit
    fitfinal= fit

    maximum=max(fitfinal)
    index=numpy.argmax(fitfinal)
    sol=pop[index].copy()
    print("The best value: ", maximum)
    print("Solution ", sol)

    fig=grafic.figure()
    x=range(dim)
    grafic.plot(x,fitini,'r-',label='Initial')
    grafic.plot(x,fit5,'k-',label='after three simulations')
    grafic.plot(x,fitfinal,'b-',label='Final')
    grafic.legend(loc="lower left")
    grafic.xlabel('Population')
    grafic.ylabel('Fitness')
    fig.show()

    return sol,maximum

# import EA_DKP
# sol, maximum=EA_DKP.EA("cost.txt","value.txt",26.3,500,0.8,0.2,200)
