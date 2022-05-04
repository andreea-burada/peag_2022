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

def HC(intx, inty, nrv, step):
    # hill climbing algorithm - applied on an initial, randomly generated point
    # the procedure holds the evolution toward the result

    # I: intx, inty - the definition domain
    #    nrp - the number of  initial points
    #    nrv - the number of neighbors
    #    step - the distance between two consecutive neighbors
    # E: x - the maximum solution
    #    fx - the maximum value

    pc=[0,0]
    # hillclimbing
    pc[0] = numpy.random.uniform(intx[0],intx[1])
    pc[1] = numpy.random.uniform(inty[0],inty[1])
    # hold the initial point
    Evolution=[pc]
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
            # hold the current point
            Evolution = Evolution+[pc]
        else:
            # the local optimum has been reached
            local = 1
    X=pc[0]
    Y=pc[1]
    Z=f_ob(pc)

    print("The maximum value: ", Z)
    print("The solution: (", X,",",Y,")")
    display(intx, inty, Evolution)

    return [[X,Y], Z]

def display(intx,inty,Evolution):
    # graphical representation

    fig=grafic.figure()
    ax=fig.gca(projection='3d')

    x=numpy.arange(intx[0],intx[1],0.01)
    y=numpy.arange(inty[0],inty[1],0.01)
    x, y = numpy.meshgrid(x, y)
    z=numpy.exp(-x**2-y**2)+y*numpy.cos(5*x)-x*numpy.sin(3*y)

    surf=ax.plot_surface(x,y,z,cmap='binary')

    nr_points=len(Evolution)
    X=[Evolution[i][0] for i in range(1,nr_points)]
    Y = [Evolution[i][1] for i in range(1,nr_points)]
    Z=[f_ob(Evolution[i]) for i in range(1,nr_points)]
    ax.plot3D([X[0]], [Y[0]], [f_ob(Evolution[0])], 'y*', markersize=10)
    ax.plot3D(X,Y,Z,'bo')
    ax.plot3D([X[nr_points-2]], [Y[nr_points-2]], [Z[nr_points-2]], 'r*', markersize=10)
    grafic.show()

#    import HC_2var_int_1initialPoint as H2
#    x,fx=H2.HC([-2,2],[-2,2],3,0.01) # - max. 3 neighbours to the left, max. 3 neighbours to the right
