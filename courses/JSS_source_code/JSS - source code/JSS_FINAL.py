import numpy as np
import matplotlib.pyplot as grafic
from CrossoverFunctions import crossover_OCX, crossover_CX
from MutationFunctions import m_perm_interschimbare, m_perm_inserare
from Selection import elitism, ruleta
from Grafic_Gantt import grafic_gantt


#####
#JSS PROBLEM
#####

# write inputs from files
#I:
# machine_op - text file - allot a machine to each operation; the first element- nrm, number of machines
# duration_op - text file - allot a duration to each operation
#E:
# nrm - number of machines
# nrs - number of jobs; - nrm x nrs operations
# m_op - the vector that assigns a machine to each operation - (i,m_op[i]) - op i+1 performed by m_op[i]
# d_op - the vector of durations
def citeste(machine_op,duration_op):
    a = np.genfromtxt(machine_op,'int')
    nrm=a[0]
    nro=len(a)-1
    m_op=np.zeros(nro,'int')
    m_op[:]=a[1:nro+1]
    d_op=np.genfromtxt(duration_op)
    nrs=int(len(d_op)/nrm)
    return nrm,nrs,m_op,d_op

# computation of the list of predecessors and the list of successors corresponding to op
def pred_succ(op,nrm):
    cat,rest=np.divmod(op,nrm)
    if rest:
        pred=[cat*nrm+i for i in range(1,rest)]
        succ=[cat*nrm+i for i in range(rest+1,nrm+1)]
    else:
        pred=[(cat-1)*nrm+i for i in range(1,nrm)]
        succ=[]
    return pred,succ

# initializing plan_m, plan
#
#I:
# nrm, nrs, m_op -  citire
#E:
# i=0,...,nrm-1:
# plan_m[i] - plan_m[i][j]=(operation, start,stop), for j=0,...,nrs-1
# plan_m[i][j]=(operation,0,0)
# i =0,nro-1:
# plan[i]=0 - the starting time of i
# assigned[i]=0 - i is not scheduled

def init_plan(nrm,nrs,m_op):
    nro=nrm*nrs
    plan_m = np.zeros([nrm, nrs, 3])
    plan=np.zeros(nro)
    assigned = np.zeros(nro)
    for i in range(nro):
        m = m_op[i] - 1
        p = np.where(plan_m[m])
        nr = int(np.size(p) / 2)
        plan_m[m][nr][0] = i + 1
    return plan,assigned,plan_m


# schedule computation
# chromosome x=[p1,p2,...,pnrm], pj a permutation corresponding to j
def calcul_plan(x,nrm,nrs,m_op,d_op):
    plan,assigned,plan_m=init_plan(nrm,nrs,m_op)
    plan_machine=np.copy(plan_m)
    for i in range(nrm):
        px=np.zeros(nrs,'int')
        px[:]=x[nrs*i:nrs*(i+1)]
        for k in range(nrs):
            plan_machine[i][k][0]=plan_m[i][px[k]][0]
    gata=0
    while not gata:
        for k in range(nrs):
            for j in range(nrm):
                a=int(plan_machine[j][k][0])
                if not assigned[a-1]:
                    # schedule a
                    plan_machine,assigned,plan=programare(j,k,plan_machine,assigned,plan,nrm,nrs,m_op,d_op)
        ex=np.where(assigned==0)
        if np.size(ex)==0:
            gata=1
    # sort the schedule ascending by the ending time
    for i in range(nrm):
        aux = plan_machine[i]
        aux = aux[aux[:, 2].argsort()]
        plan_machine[i] = aux
    #cost
    cost = max([plan_machine[i][nrs - 1][2] for i in range(nrm)])
    return plan_machine,assigned,plan, cost

# schedule the operation plan_machine[j][k][0]
def programare(j,k,plan_machine,assigned, plan,nrm,nrs,m_op,d_op):
    a=int(plan_machine[j][k][0])
    plan[a-1]=0
    pred,succ=pred_succ(a,nrm)
    s=np.size(pred)
    for i in range(s):
        b=pred[i]
        if assigned[b-1]:
            jp=m_op[b-1]-1
            c = np.where(np.transpose(plan_machine[jp])[0] == b)
            kp=c[0][0]
            if plan[a-1]<plan_machine[jp][kp][2]:
                plan[a-1]=plan_machine[jp][kp][2]
    gata=0
    while not gata:
        gata=1
        for i in range(nrs):
            b=int(plan_machine[j][i][0])
            if (assigned[b-1]) and (plan_machine[j][i][2]>plan[a-1]) and (plan[a-1]+d_op[a-1]>plan_machine[j][i][1]):
                plan[a-1]=plan_machine[j][i][2]
                gata=0
                break
    # plan a
    plan_machine[j][k][1]=plan[a-1]
    plan_machine[j][k][2]=plan[a-1]+d_op[a-1]
    assigned[a-1]=1
    # for each assigned successor of a
    s=np.size(succ)
    for i in range(s):
        b=succ[i]
        if assigned[b - 1]:
            js=m_op[b-1]-1
            c = np.where(np.transpose(plan_machine[js])[0] == b)
            ks=c[0][0]
            # discard the scheduling
            if plan_machine[js][ks][1]<plan_machine[j][k][2]:
                assigned[b-1]=0
                plan[b-1]=0
    return plan_machine,assigned,plan


# GA SOLVER

#THE INITIAL POPULATION
#I: nrm,nrs,m_op,d_op - as described above
#E: [pop,val] - the population and the fitness vector

def gen(nrm,nrs,m_op,d_op,dim):
    n=nrm*nrs
    pop=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    for i in range(dim):
        a=np.zeros(n)
        for j in range(nrm):
            px = np.random.permutation(nrs)
            a[nrs * j:nrs * (j + 1)] = px[:]
        pop[i] = a
        plan_machine, assigned, plan, cost = calcul_plan(a, nrm, nrs, m_op, d_op)
        val[i] = 1/cost
    return [pop, val]

#CROSSOVER
# I: - l=[pop,valori], parents, as described above
#     nrm, nrs, m_op, d_op - as described above
#     pc- crossover probability
#E: [po,val] - children and their fitness values
def crossover(l,dim,nrm, nrs, m_op, d_op,pc):
    pop=l[0]
    valori=l[1]
    n=nrm*nrs
    po=np.zeros((dim,n),dtype=int)
    val=np.zeros(dim,dtype=float)
    poz=np.random.permutation(dim)
    for i in range(0,dim-1,2):
        x = pop[poz[i]]
        y = pop[poz[i+1]]
        r = np.random.uniform(0,1)
        c1 = x.copy()
        c2 = y.copy()
        if r<=pc:
            xx=np.zeros(nrs)
            yy=np.zeros(nrs)
            k=np.random.randint(0,nrm)
            xx[:]=x[k*nrs:(k+1)*nrs]
            yy[:] = y[k * nrs:(k + 1) * nrs]
            #cc1, cc2 = crossover_CX(xx, yy, nrs)
            cc1, cc2 = crossover_OCX(xx, yy, nrs)
            c1[k*nrs:(k+1)*nrs]=cc1[:]
            c2[k * nrs:(k + 1) * nrs] = cc2[:]
            plan_machine, assigned, plan, cost = calcul_plan(c1, nrm, nrs, m_op, d_op)
            v1=1/cost
            plan_machine, assigned, plan, cost = calcul_plan(c2, nrm, nrs, m_op, d_op)
            v2 = 1 / cost
        else:
            v1=valori[poz[i]]
            v2=valori[poz[i+1]]
        po[i] = np.copy(c1)
        po[i+1] = np.copy(c2)
        val[i]=v1
        val[i+1]=v2
    return [po, val]

# MUTATION
    # I: desc - [po,vo] - children and their fitness values
    #   dim - population size (dimension)
    #   nrm, nrs, m_op, d_op - as described above
    #    pm - mutation probability
    # E: descm - [mpo,mvo] - mutated offspring
def mutatie(desc,dim,nrm, nrs, m_op, d_op, pm):
    po=desc[0]
    vo=desc[1]
    mpo=po.copy()
    mvo=vo.copy()
    for i in range(dim):
        r=np.random.uniform(0,1)
        if r<=pm:
            x=mpo[i]
            xx = np.zeros(nrs)
            k = np.random.randint(0, nrm)
            xx[:] = x[k * nrs:(k + 1) * nrs]
            yy=m_perm_inserare(xx,nrs)
            #yy = m_perm_interschimbare(xx, nrs)
            mpo[i][k * nrs:(k + 1) * nrs]=yy[:]
            plan_machine, assigned, plan, cost = calcul_plan(mpo[i], nrm, nrs, m_op, d_op)
            mvo[i]=1/cost
    return [mpo,mvo]


def arata(sol,v,plan):
    t=len(v)
    cost=min(v)
    print("The best cost: ",cost)
    print("Schedule: ",plan)
    fig=grafic.figure()
    x=[i for i in range(t)]
    y=[v[i] for i in range(t)]
    grafic.plot(x,y,'ro-')
    grafic.ylabel("Cost")
    grafic.xlabel("Generation")
    grafic.title("The evolution of the fittest individual/generation")
    fig.show()



## GA
#I: machine_op,duration_op: - the input files
#   dim - population size - generational model
#   NMAX - the maximum number of simulations
#   pc - crossover probability
#   pm - mutation probability
#
#E: sol - solution computed by GA
#   val - 1/maximum fitness value - minimum cost
#  plan,plan_machine - as described above
def GA(machine_op,duration_op,dim,NMAX,pc,pm):
    #initial population
    nrm, nrs, m_op, d_op = citeste(machine_op,duration_op)
    list=gen(nrm,nrs,m_op,d_op,dim)
    pop=list[0]
    qual=list[1]
    n=nrm*nrs
    #other initializations
    it=0
    gata=False
    #istoric_v - the quality of the current population (best fitness value)
    istoric_v=[1/np.max(qual)]
    # while
    #                - it< NMAX  and
    #                - the population diversity is not null
    while it<NMAX and not gata:
        #parent selection
        spop,sval=ruleta(pop,qual,dim,n)
        #crossover
        lpop_o=crossover([spop,sval],dim, nrm, nrs, m_op, d_op, pc)
        #mutation
        lpop_mo=mutatie(lpop_o,dim,nrm, nrs, m_op, d_op, pm)
        #survivor selection
        newpop,newval=elitism(pop,qual,lpop_mo[0],lpop_mo[1],dim)
        #other updates
        minim=np.min(newval)
        maxim=np.max(newval)
        if maxim==minim:
            gata=True
        else:
            it=it+1
        istoric_v.append(1/np.max(newval))
        pop=newpop.copy()
        qual=newval.copy()
    i_sol=np.where(qual==maxim)
    sol=pop[i_sol[0][0]]
    plan_machine, assigned, plan, cost = calcul_plan(sol, nrm, nrs, m_op, d_op)
    val=maxim
    arata(sol,istoric_v,plan)
    grafic_gantt(plan_machine,1/val)
    return sol,1/val, plan_machine, plan


# import JSS_FINAL as t
#sol,cost, plan_machine, plan=t.GA('masini-operatii.txt','operatii-durata.txt',200,50,0.8,3/200)
#sol,cost, plan_machine, plan=t.GA('masini-operatii11.txt','operatii-durata11.txt',500,50,0.8,20/500)
#sol,cost, plan_machine, plan=t.GA('masini-operatii2.txt','operatii-durata2.txt',700,80,0.8,60/700)
#sol,cost, plan_machine, plan=t.GA('masini-operatii3.txt','operatii-durata3.txt',700,50,0.8,60/700)
#sol,cost, plan_machine, plan=t.GA('masinioperatii.txt','operatiidurate.txt',1000,70,0.8,80/1000)

