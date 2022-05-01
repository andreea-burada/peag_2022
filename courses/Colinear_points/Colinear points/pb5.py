import numpy as np
import random
import matplotlib.pyplot as grafic
from CrossoverFunctions import crossover_uniform
from Mutation_operators import m_ra
from Selection import SUS, elitism


#Genotype representation
# - x=(x1,x2,x3), x1<>x2<>x3, x1,x2,x3 in {0,1,...,n-1}
# n - the number of points

#the fitness function
# S - the set of n points
#A=S[x[0]], B=S[x[1]], C=S[x[2]]
# f(x)=min(AC+CB-AB;AB+BC-AC;BA+AC-BC)
#fitness(x)=1/(1+f(x)) - the maximum value is 1

def E_Dist(A,B):
    return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def fitness(x,S):
    A=S[x[0]]
    B=S[x[1]]
    C=S[x[2]]
    fx=min([E_Dist(A,C)+E_Dist(C,B)-E_Dist(A,B),E_Dist(A,B)+E_Dist(B,C)-E_Dist(A,C),E_Dist(B,A)+E_Dist(A,C)-E_Dist(B,C)])
    return 1/(1+fx)



# the initial population is randomly generated
#I:
# nf - input file - set of n points (xA,yA)
# dim - population size
#O:
# pop - the population matrix - size dimxn
# val - the fitness vector - size dim
# S, n - the set of points and its size
def generate_p(nf,dim):
    S=np.genfromtxt(nf)
    n=len(S)
    pop=np.zeros([dim,3],dtype=int)
    val=np.zeros(dim)
    for i in range(dim):
        # randomly generate 3 unique numbers within {0,1,...,n-1}
        pop[i]=random.sample(range(0,n),3)
        val[i]=fitness(pop[i],S)
    return pop,val,S

#test the feasibility of x - unique values
def feasible(x):
    ok=True
    if x[0]==x[1] or x[0]==x[2] or x[1]==x[2]:
        ok=False
    return ok


# crossover procedure - population level
# the children should be feasible candidate solutions - vectors having unique values
#I:
#p_pop, p_val, dim - parent population matrix, parent fitness vector, size
#pc - recombination probability
#S - the set of points --> to compute the fitness values of the newly created individuals
#O:
# o_pop,o_val - offspring and their fitness values
def crossover_pop(p_pop, p_val,dim, S, pc):
    # initialize the offspring
    o_pop = p_pop.copy()
    o_val=p_val.copy()
    for i in range(0, dim - 1, 2):
        # select the parent pairs
        x = p_pop[i]
        y = p_pop[i + 1]
        r = np.random.uniform(0, 1)
        if r <= pc:
            # apply the crossover
            c1, c2 = crossover_uniform(x, y, 3)
            # test the feasibility
            if feasible(c1):
                o_pop[i]=c1.copy()
                o_val[i]=fitness(c1,S)
            if feasible(c2):
                o_pop[i+1]=c2.copy()
                o_val[i+1]=fitness(c2,S)
    return o_pop,o_val

# mutation procedure - population level
# the mutated offspring should be feasible candidate solutions - vectors having unique values
#I:
#o_pop, o_val, dim - offspring population matrix, offspring fitness vector, size
#pm - probability of mutation
#S - the set of points --> to compute the fitness values of the newly created individuals
#O:
# mo_pop,mo_val - mutated offspring and their fitness values
def mutation_pop(o_pop, o_val,dim, S, pm):
    # initialize the mutated offspring
    mo_pop = o_pop.copy()
    mo_val=o_val.copy()
    n=len(S)
    for i in range(dim):
        # select an individual
        x = o_pop[i]
        for j in range(3):
            # select a gene
            r = np.random.uniform(0, 1)
            if r <= pm:
                # apply the mutation
                x[j]= m_ra(0,n)
        # test the feasibility
        if feasible(x):
            mo_pop[i]=x.copy()
            mo_val[i]=fitness(x,S)
    return mo_pop,mo_val


# show the search space and a solution
# I: sol - the computed solution
#    P - the set of points

def disp_sol(sol, P):
    nor=grafic.figure()
    n=len(P)
    x=[P[i,0] for i in range(n)]
    y=[P[i,1] for i in range(n)]
    grafic.plot(x,y,color='k', linestyle='none', marker='.',
                markerfacecolor='blue', markersize=4)
    x = [P[sol[i], 0] for i in range(3)]
    y = [P[sol[i], 1] for i in range(3)]
    grafic.plot(x,y,"ro-")

# GA solver
#I:
# nf - input file - set of n points (xA,yA)
# dim - population size
# NMAX - maximum number of evolutionary cycles
# pc - crossover probability
# pm - mutation probability
#O:
# sol, max_val - computed solution and its fitness value - the error (1-max_val)/max_val
def GA_solver(nf,dim,NMAX,pc,pm):
    # compute the initial population
    pop, val, S=generate_p(nf,dim)
    # t - the time
    t=0
    max_val=max(val)
    pos=np.argmax(val)
    sol=pop[pos]
    # stop - a logical variable that controls the termination condition
    stop=False
    # max_val = 1 --> solution
    if max_val>=0.99999:
        stop=True
    history=[max_val]
    while t<NMAX and not stop and max_val<0.99999:
        # parent selection
        p_pop,p_val=SUS(pop, val, dim, 3)
        # crossover
        o_pop,o_val=crossover_pop(p_pop,p_val,dim,S,pc)
        #mutation
        mo_pop,mo_val=mutation_pop(o_pop,o_val,dim,S,pm)
        #survivor selection
        new_pop,new_val=elitism(pop,val,mo_pop,mo_val,dim)
        max_val=max(new_val)
        pos=np.argmax(new_val)
        sol=new_pop[pos]
        min_val=min(new_val)
        #check the variability
        if min_val==max_val:
            stop=True
        history.append(max_val)
        pop=new_pop.copy()
        val=new_val.copy()
        t+=1
    #display the evolution
    fig = grafic.figure()
    x = [i for i in range(t)]
    y = [history[i] for i in range(t)]
    grafic.plot(x, y, 'ro-')
    grafic.ylabel("Fitness")
    grafic.xlabel("Generation")
    grafic.title("Quality evolution")
    fig.show()
    if max_val<0.99999:
        print('No solution')
    else:
        P=[S[sol[0]],S[sol[1]],S[sol[2]]]
        print('3 colinear points are: ',P[0],P[1],P[2])
    disp_sol(sol, S)
    return sol,max_val,(1-max_val)/max_val

#import pb5
# sol,fit,er=pb5.GA_solver('points.txt',300,250,0.8,0.2)
