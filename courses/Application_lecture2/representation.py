import numpy as np

def r_bin(x,a,b,nrz):
    m = int(np.log2((b - a) * np.power(10, nrz))) + 1
    n = int((x - a) * (np.power(2, m) - 1) / (b - a))
    t=bin(n)[2:]
    result=t.zfill(m)
    return result

def r_dec(sir,a,b):
    m = len(sir)
    n = int(sir, 2)
    x = a + n * (b - a) / (2 ** m - 1)
    return x

# import representation as r
# sir=r.r_bin(1.234567,-5,12,4)
# x=r.r_dec(sir,-5,12)


