import numpy
from math import sin, cos
import matplotlib.pyplot as grafic


def f_obiectiv(x):
    # a function to maximize with more than one local maximum points
    # Input  (I): x - the point in which the value of the function is being computed
    # Output (O): y = the value of the function in the point x
    #
    # o functie de maximizat cu mai multe puncte de maxim local
    # I: x - punctul in care se calculeaza valoarea functiei
    # E: y - valoarea functiei in punctul x

    # some function with local extremes
    #
    # o functie oarecare cu extreme locale

    # x**3  - x la puterea 3
    y = x**3 * sin(x/3) + x**3 * cos(2*x) -x*sin(3*x) + x*cos(x)

    return y

def vecini(x, nr, pas, a, b):
    # computes the neighbours of a point (on an axis)
    # I: x - current point
    #    no - the number of neighbours in each direction
    #    dist - the distance between consecutive neighbours
    #    a, b - the ends of the working range
    # O: v - the list of neighbours (2 lines: points, values)
    #
    # calculează vecinii unui punct (pe o axă), impreuna cu calitatile acestora
    # I: x - punct curent
    #    nr - numar de vecini pe fiecare directie
    #    pas - distanta intre vecinii consecutivi
    #    a, b - capetele intervalului de lucru
    # E: v - lista vecini (2 linii: puncte, calitati)

    #we are using comprehensive lists
    #
    #sunt folosite liste comprehensive

    vec=[x+i*pas for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    valv=[f_obiectiv(x+i*pas) for i in range(-nr, nr+1) if ((x+i*pas>=a) and (x+i*pas<=b))]
    return [vec,valv]


def HC(a, b, nrp, nrv, pas):
    # The HillClimbing implementation for finding the maximum of a function of one variable
    # I: a, b - the ends of the working range on which the function is defined (an axis)
    #    nrp - the number of initial points used by the algorithm
    #    nrv - the number of utilized neighbours on each direction (total 2*nrv+1 - 1 is the current point)
    #    dist - the distance between two consecutive neighbours
    # O: x - maximum point
    #    fx - the maximum value of the function (in the point x)
    # Obs.: if the chart is not being closed after the execution of an example, on the next execution
    #       the chart will be added above the previous one
    #
    # implementare hillclimbing pentru gasirea maximului unei functii de o variabila
    # I: a, b - capetele intervalului pe care e definita functia  (o axa)
    #    nrp - numarul de puncte initiale folosite de algoritm
    #    nrv - numarul de vecini pe fiecare directie utilizati (total 2*nrv+1 - 1 e punctul curent)
    #    pas - distanta intre doi vecini consecutivi
    # E: x - punct de maxim
    #    fx - valoarea maxima a functiei (in punctul x)
    # Obs.: daca nu se inchide graficul dupa rularea unui exemplu, la rularea urmatorului exemplu
    #    graficul va fi adaugat peste cel anterior

    # the initialization of an empty list of coordinates
    #
    # initializare liste goale de coordonate
    X=[None]*nrp
    Y=[None]*nrp
    # for each initial point
    #
    # pentru fiecare punct initial
    for i in range(nrp):
        # the application of the HillClimbing algorithm for the current initial point randomly generated
        #
        # aplicare hillclimbing pentru punctul initial curent generat aleator
        pc=numpy.random.uniform(a,b)    # randomly choose a starting point / alege un punct de inceput aleator
        local=0                         # = 0 -> we did not reach at a local maximum / nu am ajuns in maxim local
        while not local:
            # computes the neighbours of the current point and the corresponding values of the function
            #
            # calculeaza vecinii punctului curent si valorile corespunzatoare ale functiei
            nvec, nval=vecini(pc,nrv,pas,a,b)
            valmax=max(nval)
            poz=nval.index(valmax)
            vecmax=nvec[poz]
            # replace the current point with the best neighbour, if a better one exists
            #
            # inlocuieste punctul curent cu cel mai bun vecin, daca exista unul mai bun
            if valmax>f_obiectiv(pc):
                pc=vecmax
            else:
                # there is no better neighbour, meaning we have reached a local maximum
                #
                # nici un vecin mai bun, inseamna ca am atins un maxim local
                local=1
        # memorizes the best found point and the corresponding value of the function
        #
        # memoreaza cel mai bun punct gasit si valoarea corespunzatoare a functiei
        X[i]=vecmax
        Y[i]=f_obiectiv(vecmax)

    # determines the best of the final points and the corresponding value of the objective function
    #
    #determina cel mai bun dintre punctele finale si valoarea corespunzatoare a functiei obiectiv
    fx=max(Y)
    poz=Y.index(fx)
    x=X[poz]

    # display the results and chart (if you know how to draw the chart)
    #
    # afiseaza rezultatele si graficul (daca stii sa desenezi graficul)
    print("Calculated maximum value/Valoare maxima calculata: ", fx)
    print("It's at the point/E atinsa in punctul: ", x)
    deseneaza(a, b, X, Y, x, fx)
    return [x,fx]


def deseneaza(a, b, X, Y, xmax, ymax):
    # The Visualisation fo the results for HillClimbing with 1 variable
    # I: a, b - the ends of the working range
    #    X, Y - lists with the coordinates of the final points computed l
    #    xmax, ymax - the coordinates of the best point found
    # O: -
    #
    # vizualizare rezultate pentru hillclimbing 1 variabila
    # I: a, b - capete interval de lucru
    #    X, Y - liste cu coordonatele punctelor finale calculate
    #    xmax, ymax - corrdonatele celui mai bun punct gasit
    # E: -

    x=numpy.arange(a,b,0.01)
    grafic.plot(x,[f_obiectiv(i) for i in x],'k-',X,Y,'bo',xmax,ymax,'r*',markersize=10)
    #grafic.plot(xmax,ymax,'r*',markersize=10)


# Function calling examples:
#
# Exemple de apel:
#1
#    import HC_1var_int as H
#2
#    x,fx=H.HC(1.5,10,100,5,0.1)
#    x,fx=H.HC(-1.5,20.2,100,5,0.1)
#    x,fx=H.HC(-15,2.2,100,5,0.1)
#    x,fx=H.HC(-15,23.2,100,5,0.1)
#    x,fx=H.HC(-15,23.2,100,100,0.01)
# Obs.: if the chart is not being closed after the execution of an example, on the next execution
#       the chart will be added above the previous one