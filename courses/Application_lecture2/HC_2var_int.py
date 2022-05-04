import numpy
from math import sin, cos, exp
import matplotlib.pyplot as grafic
from mpl_toolkits.mplot3d import Axes3D

# the fitness (objective) function
def f_ob(a):
    # multimodal objective function - to be maximized

    # I: a - the input vector
    # E: z - f_ob(a)

    x=a[0]
    y=a[1]
    z= exp(-x**2-y**2)+y*cos(5*x)-x*sin(3*y)
    return z

def neighbors(x, nr, pas, intx, inty):
    # compute a set of neighbors

    # I: x - the input vector
    #    nr - the number of neighbors are less than or equal to 2*nr
    #    pas - the distance between two consecutive neighbors
    #    intx, int y - the intervals: x[0] in [intx[0],intx[1]], x[1] in [inty[0],inty[1]]
    # E: v - neighbors list(x, y, value=f(x,y))

    neighbor_x=[x[0]+i*pas for i in range(-nr, nr+1) if ((x[0]+i*pas>intx[0]) and (x[0]+i*pas<=intx[1]))]
    neighbor_y=[x[1]+i*pas for i in range(-nr, nr+1) if ((x[1]+i*pas>inty[0]) and (x[1]+i*pas<=inty[1]))]
    neighbor=[[x,y] for x in neighbor_x for y in neighbor_y]
    val=[f_ob(p) for p in neighbor]
    return [neighbor,val]

def HC(intx, inty, nrp, nrv, step):
    # hill climbing algorithm - applied on nrp initial points

    # I: intx, inty - the definition domain
    #    nrp - the number of  initial points
    #    nrv - the number of neighbors
    #    step - the distance between two consecutive neighbors
    # E: x - the maximum solution
    #    fx - the maximum value

    X=[None]*nrp
    Y=[None]*nrp
    Z=[None]*nrp
    pc=[0,0]
    # for each initial point pc
    for i in range(nrp):
        # hillclimbing
        pc[0] = numpy.random.uniform(intx[0],intx[1])
        pc[1] = numpy.random.uniform(inty[0],inty[1])
        neighbor_max=pc       # the best neighbor
        local=0         # the local optimum has'n been reached yet
        while not local:
            # compute the neighbors
            nvec, nval = neighbors(pc, nrv, step, intx, inty)
            val_max = max(nval)
            poz = nval.index(val_max)
            neighbor_max = nvec[poz]
            if val_max > f_ob(pc):
                # update the current element
                pc = neighbor_max
            else:
                # the local optimum has been reached
                local = 1
        X[i]=neighbor_max[0]
        Y[i]=neighbor_max[1]
        Z[i]=f_ob(neighbor_max)

    # compute the best solution
    fx = max(Z)
    poz = Z.index(fx)
    x = [X[poz],Y[poz]]

    print("The maximum value: ", fx)
    print("The solution: (", x[0],",",x[1],")")
    display(intx, inty, X, Y, Z, x, fx)

    return [x, fx]

def display(intx, inty, X, Y, Z, xmax, zmax):
    # graphical representation

    fig=grafic.figure()
    ax=fig.gca(projection='3d')

    x=numpy.arange(intx[0],intx[1],0.01)
    y=numpy.arange(inty[0],inty[1],0.01)
    x, y = numpy.meshgrid(x, y)
    z=numpy.exp(-x**2-y**2)+y*numpy.cos(5*x)-x*numpy.sin(3*y)

    surf=ax.plot_surface(x,y,z,cmap='binary')
    ax.plot3D(X,Y,Z,'bo')
    ax.plot3D([xmax[0]],[xmax[1]],[zmax],'r*',markersize=10)

    grafic.show()

#    import HC_2var_int as H2
#    x,fx=H2.HC([-2,2],[-2,2],50,2,0.01) # - 50 HCs, 2 neighbours to the left, 2 neighbours to the right
#    x,fx=H2.HC([-2,2],[-2,2],100,10,0.01) # - 100 HCs, 10 neighbours to the left, 10 neighbours to the right