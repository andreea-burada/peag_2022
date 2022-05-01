import numpy as np
nr_p=300
a=np.zeros([nr_p,2],dtype=int)
i=0
while i<nr_p:
    x=np.random.randint(-400,400,2)
    if not x in a:
        a[i]=x.copy()
        i+=1
np.savetxt('points1.txt',a)

