import numpy as np


# check the feasibility of choosing x and calculate the objective function
#
# verifica fezabilitatea alegerii x si calculeaza si f. obiectiv
def ok(x, n, c, v, max):
    val = 0
    cost = 0
    for i in range(n):
        val = val + x[i] * v[i]
        cost = cost + x[i] * c[i]
    return cost <= max, val


# computes the neighbours of the current point using bitflip and so it is feasible
#
# calculul vecinilor punctului curent - prin bitflip si astfel incat este fezabil
def vecini(x, n, c, v, max):
    # we are using comprehensive lists
    #
    # sunt folosite liste comprehensive
    Vec = []
    Cal = []
    for i in range(n):
        y = x.copy()
        y[i] = not x[i]
        fez, val = ok(y, n, c, v, max)
        if fez:
            Vec = Vec + [y]
            Cal = Cal + [val]
    #
    return np.array(Vec), np.array(Cal)


##The HillClimbing implementation for solving Knapsack 0-1 problem
# I: fc,fv - cost / value files
#   dim - number of starting points - how many times do we call hill climbing function
#   max - maximum Knapsack capacity
#
# O: sol - calculated solution
#   val - maximum of the fitness function
#
##ALGORITMUL HILL CLIMBING PENTRU REZOLVAREA PROBLEMEI RUCSACULUI 0-1
# I: fc,fv - fisierele cu costuri/valori
#   dim - numărul punctelor de start - de cate ori apelam hill climbing
#   max=capacitatea maxima a rucsacului
#
# E: sol - solutia calculata
#   val - maximul functiei fitness

def HC(fc, fv, dim, max):
    # reading the inputs of our problem
    #
    # citirea datelor
    c = np.genfromtxt(fc)
    v = np.genfromtxt(fv)
    # n = the size of the problem
    #
    # n=dimensiunea problemei
    n = len(c)
    # the initialization of 2 empty list of points and qualities
    puncte = []
    calitati = []
    for timp in range(dim):
        # generate the initial point
        #
        # genereaza punctul initial
        local = False
        gata = False
        while gata == False:
            # generate candidate x with 0, 1 elements
            #
            # genereaza candidatul x cu elemente 0,1
            x = np.random.randint(0, 2, n)
            gata, val = ok(x, n, c, v, max)
        while not local:
            # computes the neighbours of the current point and the corresponding values of the function
            #
            # calculeaza vecinii punctului curent si valorile corespunzatoare ale functiei
            Vec, Cal = vecini(x, n, c, v, max)
            if len(Vec) == 0:
                local = True
            else:
                valm = np.max(Cal)
                i = np.where(Cal == valm)
                vn = Vec[i[0][0]]
                # replace the current point with the best neighbour, if a better one exists
                #
                # inlocuieste punctul curent cu cel mai bun vecin, daca exista unul mai bun
                if valm > val:
                    val = valm
                    x = vn
                else:
                    local = True
                    # memorizes the best found point and the corresponding value of the function
                    #
                    # memoreaza cel mai bun punct gasit si valoarea corespunzatoare a functiei
        puncte = puncte + [x]
        calitati = calitati + [val]

    calitati = np.array(calitati)
    puncte = np.array(puncte)
    # determines the best of the final points and the corresponding value of the objective function
    #
    # determina cel mai bun dintre punctele finale si valoarea corespunzatoare a functiei obiectiv
    vmax = np.max(calitati)
    i = np.where(calitati == vmax)
    sol = puncte[i[0][0]]
    print("The best calculated value/Cea mai buna valoare calculată: ", vmax)
    print("The right choice is/Alegerea corespunzatoare este: ", sol)
    return sol, vmax, puncte, calitati

# Function calling examples
#
# Exemple de apel:
# 1
# import Rucsac01_HillClimbing as r1
# 2
# sol,val,P,C=r1.HC("cost.txt","valoare.txt",30,50)
# sol,val,P,C=r1.HC("cost1.txt","valoare1.txt",90,50)
# sol,val,P,C=r1.HC("cost2.txt","valoare2.txt",500,56.6)
