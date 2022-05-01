import numpy as np
import matplotlib.pyplot as grafic


#Algoritm evolutiv pentru maximizarea functieiobiectiv f de mai jos


#definitia functiei obiectiv
def fobiectiv(x):
    #functii standard np.power (x,p) - merge pt x>=0 , np.sin(x), np.cos(x)
    val=np.sign(x)*np.power(np.abs(x),3)-3*np.sin(7*x+0.2)+2*np.cos(x/5-0.4)+1
    return val

#generarea populatiei de dimensiune dim la momentul initial; dim--> multiplu de 4
# pop: matrice cu dim linii si 2 coloane
#               - in prima coloana x, candidatul la solutie
#               - in a doua coloana calitatea lui prin functia obiectiv
def genpop(dim):
    #initializarea cu matricea nula
    pop=np.zeros([dim,2])
    for i in range(dim):
        x=np.random.uniform(-1,1)
        val=fobiectiv(x)
        pop[i][0]=x
        pop[i][1]=val
    return pop

#selectia parintilor - turneu din 2 indivizi --- rezulta dim/2 parinti
def selectie_parinti(pop,dim):
    dim_p=int(dim/2)
    parinti=np.zeros([dim_p,2])
    for i in range (dim_p):
        #genereaza aleator 2 pozitii din populatie
        poz=np.random.randint(0,dim,2)
        individ1=pop[poz[0]]
        individ2=pop[poz[1]]
        #alege cel mai bun individ din cei doi
        if individ1[1]>individ2[1]:
            parinti[i]=individ1.copy()
        else:
            parinti[i]=individ2.copy()
    return parinti, dim_p



#mutatia la nivelul populatiei
#un individ este mutat cu probabilitatea pm
def mutatie_pop(copii,dimc,pm):
    #populatia rezultata - copii_m: copiii dupa mutatie
    copii_m=copii.copy()
    for i in range (dimc):
        #verificam daca facem mutatie in individul i
        r=np.random.uniform(0,1)
        if r<=pm:
            #mutatie
            x=copii[i][0]
            x_nou=-x
            v_nou=fobiectiv(x_nou)
            copii_m[i][0]=x_nou
            copii_m[i][1]=v_nou
    return copii_m


#crossover pe populatia de parinti, de dimensiune dimp cu probabilitatea pc - rezulta maxim dimp/2 indivizi
def crossover_populatie(parinti,dimp,pc):
    dimc=int(dimp/2)
    #se lucreaza cu liste cu indivizi
    copii=[]
    pozitii=[[-1,-1]]
    # recombinarea
    nrcopii=0
    for i in range(dimc):
        #verificam daca se face crossover
        r=np.random.uniform(0,1)
        if r<=pc:
            p=np.random.randint(0,dimp,2)
            p=list(p)
            while p in pozitii:
                p = np.random.randint(0, dimp, 2)
                p=list(p)
            # am generat o pereche de pozitii care nu au mai fost generate anterior
            pozitii=pozitii+[p]
            individ1=parinti[p[0]]
            individ2=parinti[p[1]]
            copil=(individ1[0]+individ2[0])/2
            val=fobiectiv(copil)
            copii=copii+[[copil,val]]
            nrcopii=nrcopii+1
    #trecem de la liste la matrice
    copii=np.array(copii)
    return copii,nrcopii

#selectia generatiei urmatoare
def gen_urm(pop,dim,copii_m,dimc):
    if dimc==0:
        pop_urm=pop.copy()
    else:
        pn = np.append(pop, copii_m)
        pn = pn.reshape(dim+dimc, 2)
        #sortare crescatoare dupa a doua coloana - functia obiectiv
        pop_sort = pn[pn[:,1].argsort()]
        #aleg ultimii dim indivizi
        pop_urm = pop_sort[dim+dimc:dimc - 1:-1, :]
    return pop_urm



def arata(pop,dim,text):
    # vizualizare rezultate - calitatile indivizilor din populatie pe functia obiectiv
    x = np.arange(-1, 1, 0.0001)
    y=[fobiectiv(k) for k in x]
    fig=grafic.figure()
    grafic.plot(x,y,'k')
    x=[pop[i][0] for i in range(dim)]
    y=[pop[i][1] for i in range(dim)]
    grafic.plot(x,y,'ro')
    grafic.ylabel("OY")
    grafic.xlabel("OX")
    #grafic.title("Graficul functiei pe [-1,1]")
    grafic.title(text)
    fig.show()


def EA(dim,pc,pm,MAX):
    pop=genpop(dim)
    pop_ini=pop.copy()
    text="Graficul functiei pe [-1,1] si populatia initiala"
    arata(pop,dim,text)
    for k in range(MAX):
        parinti,dim_p=selectie_parinti(pop, dim)
        copii,dim_c=crossover_populatie(parinti, dim_p, pc)
        copiim=mutatie_pop(copii, dim_c, pm)
        pop_urm=gen_urm(pop,dim,copiim,dim_c)
        pop=pop_urm.copy()
        #arata(pop, dim, text)
        if k==5:
            text="Graficul functiei pe [-1,1] si populatia dupa 5 generatii"
            arata(pop,dim,text)
    text="Graficul functiei pe [-1,1] si populatia finala"
    arata(pop,dim,text)
    return pop_ini,pop


#import pbcurs1 as p1
#p1.EA(64,0.8,0.2,20)