import numpy as np
import matplotlib.pyplot as grafic


# EA for maximizing the objective function fob described below


#the objective (fitness) function
def fob(x):
    val=np.sign(x)*np.power(np.abs(x),3)-3*np.sin(7*x+0.2)+2*np.cos(x/5-0.4)+1
    return val

# generate the initial population
# pop: dimx2 matrix
#               - the first column correspond to a chromosome
#               - the second column keeps the fitness values
def initial_population(dim):
    #initialization with the null matrix
    pop=np.zeros([dim,2])
    for i in range(dim):
        x=np.random.uniform(-1,1)
        val=fob(x)
        pop[i][0]=x
        pop[i][1]=val
    return pop

#mating pool selection - tournament
def parents_selection(pop,dim):
    dim_p=int(dim/2)
    parents=np.zeros([dim_p,2])
    for i in range (dim_p):
        #randomly generate 2 positions in the population
        poz=np.random.randint(0,dim,2)
        chromosome1=pop[poz[0]]
        chromosome2=pop[poz[1]]
        #choose the better of the two in the parent population
        if chromosome1[1]>chromosome2[1]:
            parents[i]=chromosome1.copy()
        else:
            parents[i]=chromosome2.copy()
    return parents, dim_p



#mutation - population level
#each individual is mutated with the probability pm
def offspring_mutation(children,dimc,pm):
    #the resulted population - copii_m: the mutated children (offspring)
    mutated_children=children.copy()
    for i in range (dimc):
        #we check if we make a mutation in the ith individual
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutation - individual
            x=children[i][0]
            x_nou=-x
            v_nou=fob(x_nou)
            mutated_children[i][0]=x_nou
            mutated_children[i][1]=v_nou
    return mutated_children


#crossover on the parent population of size dimp with probability pc - maximum dimp / 2 individuals are obtained
def crossover_parents(parents,dimp,pc):
    dimc=int(dimp/2)
    # compute a list
    children=[]
    pozitii=[[-1,-1]]
    # recombinarea
    children_number=0
    for i in range(dimc):
        #we check if we make a crossover
        r=np.random.uniform(0,1)
        if r<=pc:
            p=np.random.randint(0,dimp,2)
            p=list(p)
            while p in pozitii:
                p = np.random.randint(0, dimp, 2)
                p=list(p)
            # generate a pair of positions that were not previously generated
            pozitii=pozitii+[p]
            chromosome1=parents[p[0]]
            chromosome2=parents[p[1]]
            copil=(chromosome1[0]+chromosome2[0])/2
            val=fob(copil)
            children=children+[[copil,val]]
            children_number=children_number+1
    #typecast the list into the array
    children=np.array(children)
    return children,children_number

#survivors selection
def next_generation(pop,dim,mutated_children,dimc):
    if dimc==0:
        pop_urm=pop.copy()
    else:
        pn = np.append(pop, mutated_children)
        pn = pn.reshape(dim+dimc, 2)
        #ascending sorting by second column - objective function
        pop_sort = pn[pn[:,1].argsort()]
        #select the best dim individuals
        pop_urm = pop_sort[dim+dimc:dimc - 1:-1, :]
    return pop_urm



def disp_results(pop,dim,text):
    # show the results
    x = np.arange(-1, 1, 0.0001)
    y=[fob(k) for k in x]
    fig=grafic.figure()
    grafic.plot(x,y,'k')
    x=[pop[i][0] for i in range(dim)]
    y=[pop[i][1] for i in range(dim)]
    grafic.plot(x,y,'ro')
    grafic.ylabel("OY")
    grafic.xlabel("OX")
    grafic.title(text)
    fig.show()


def EA(dim,pc,pm,MAX):
    pop=initial_population(dim)
    pop_ini=pop.copy()
    text="Objectiv function - initial population"
    disp_results(pop,dim,text)
    for k in range(MAX):
        parents,dim_p=parents_selection(pop, dim)
        children,dim_c=crossover_parents(parents, dim_p, pc)
        mutated_children=offspring_mutation(children, dim_c, pm)
        pop_urm=next_generation(pop,dim,mutated_children,dim_c)
        pop=pop_urm.copy()
        #disp_results(pop, dim, text)
        if k==5:
            text="Objectiv function - population after 5 simulations"
            disp_results(pop,dim,text)
    text="Objectiv function - final population"
    disp_results(pop,dim,text)
    return pop_ini,pop

# run: copy the lines below into Python Console
#import maximizef as solve
#initial_pop,final_pop=solve.EA(64,0.8,0.2,20)