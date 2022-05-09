import numpy
import matplotlib.pyplot as grafic


def verificare(sol, oferta, cerere):
    o_r = oferta - numpy.sum(sol, axis=1)
    c_r = cerere - numpy.sum(sol, axis=0)

    mino = min(o_r)
    maxo = max(o_r)
    minc = min(c_r)
    maxc = max(c_r)
    print("Oferta rămasă:", o_r)
    if mino < 0:
        print("Eroare la ofertă: se consumă mai mult decât e disponibil")
    if maxo > 0:
        print("Eroare la ofertă: se consumă mai puțin decât e disponibil")
    if mino == 0 and maxo == 0:
        print("Oferta e consumată în totalitate")

    print("Cerere rămasă:", c_r)
    if minc < 0:
        print("Eroare la cerere: se transportă mai mult decât se cere")
    if maxc > 0:
        print("Eroare la cerere: se transportă mai putin decât se cere")
    if minc == 0 and maxc == 0:
        print("Cererea e acoperită în totalitate")


def gen_alocare(permutare, oferta, cerere):
    m = len(oferta)
    n = len(cerere)
    x = numpy.zeros((m, n))
    i = 0
    CR = sum(cerere)
    o_r = oferta.copy()
    c_r = cerere.copy()
    while CR > 0:
        lin, col = numpy.unravel_index(int(permutare[i]), (m, n))
        x[lin, col] = min([o_r[lin], c_r[col]])
        o_r[lin] -= x[lin, col]
        c_r[col] -= x[lin, col]
        CR -= x[lin, col]
        i += 1
    return x


def fo(x, oferta, cerere, costuri):
    a = gen_alocare(x, oferta, cerere)
    c = 1000. / numpy.sum(a * costuri)
    return c


def gen(dim, oferta, cerere, costuri):
    m = len(oferta)
    n = len(cerere)
    pop = numpy.zeros((dim, m * n + 1))
    for i in range(dim):
        x = numpy.random.permutation(m * n)
        pop[i, :-1] = x
        pop[i, -1] = fo(x, oferta, cerere, costuri)
    return (pop)


def cicluri(x, y, n):
    index = 1
    ciclu = numpy.zeros(n)
    gata = 0
    while not gata:
        p = numpy.where(ciclu == 0)
        if numpy.size(p):
            i = p[0][0]
            a = x[i]
            ciclu[i] = index
            b = y[i]
            while b != a:
                r = numpy.where(x == b)
                j = r[0][0]
                ciclu[j] = index
                b = y[j]
            index += 1
        else:
            gata = 1
    return ciclu


def crossover_CX(x, y, n):
    ciclu = cicluri(x, y, n)
    c1 = x.copy()
    c2 = y.copy()
    for i in range(n):
        cat, rest = numpy.divmod(ciclu[i], 2)
        if not rest:
            c1[i] = y[i]
            c2[i] = x[i]
    return c1, c2


def recombinare(parinti, pr, oferta, cerere, costuri):
    dim, n = numpy.shape(parinti)
    desc = parinti.copy()
    perechi = numpy.random.permutation(dim)
    for i in range(0, dim, 2):
        x = parinti[perechi[i], :n - 1]
        y = parinti[perechi[i + 1], :n - 1]
        r = numpy.random.uniform(0, 1)
        if r <= pr:
            d1, d2 = crossover_CX(x, y, n - 1)
            desc[i, :n - 1] = d1
            desc[i][n - 1] = fo(d1, oferta, cerere, costuri)
            desc[i + 1, :n - 1] = d2
            desc[i + 1][n - 1] = fo(d2, oferta, cerere, costuri)
    return desc


def m_perm_interschimbare(x, n):
    poz = numpy.random.randint(0, n, 2)
    while poz[0] == poz[1]:
        poz = numpy.random.randint(0, n, 2)
    p1 = numpy.min(poz)
    p2 = numpy.max(poz)
    y = x.copy()
    y[p1] = x[p2]
    y[p2] = x[p1]
    return y


def mutatie(desc, pm, oferta, cerere, costuri):
    dim, n = numpy.shape(desc)
    descm = desc.copy()
    for i in range(dim):
        x = descm[i, :n - 1]
        r = numpy.random.uniform(0, 1)
        if r <= pm:
            y = m_perm_interschimbare(x, n - 1)
            descm[i, :n - 1] = y
            descm[i, n - 1] = fo(y, oferta, cerere, costuri)
    return descm


def fps(qual, dim):
    fps = numpy.zeros(dim)
    suma = numpy.sum(qual)
    for i in range(dim):
        fps[i] = qual[i] / suma
    qfps = fps.copy()
    for i in range(1, dim):
        qfps[i] = qfps[i - 1] + fps[i]
    return qfps


def sigmafps(qual, dim):
    med = numpy.mean(qual)
    var = numpy.std(qual)
    newq = [max(0, qual[i] - (med - 2 * var)) for i in range(dim)]
    if numpy.sum(newq) == 0:
        qfps = fps(qual, dim)
    else:
        qfps = fps(newq, dim)
    return qfps


def SUS(pop, qual, dim, n):
    spop = pop.copy()
    squal = numpy.zeros(dim)
    qfps = sigmafps(qual, dim)
    r = numpy.random.uniform(0, 1 / dim)
    k, i = 0, 0
    while (k < dim):
        while (r <= qfps[i]):
            spop[k][:] = pop[i][:]
            squal[k] = qual[i]
            r = r + 1 / dim
            k = k + 1
        i = i + 1
    return spop, squal


def elitism(pop_c, qual_c, pop_mo, qual_mo, dim):
    pop = numpy.copy(pop_mo)
    qual = numpy.copy(qual_mo)
    max_c = numpy.max(qual_c)
    max_mo = numpy.max(qual_mo)
    if max_c > max_mo:
        p1 = numpy.where(qual_c == max_c)
        imax = p1[0][0]
        ir = numpy.random.randint(dim)
        pop[ir] = pop_c[imax].copy()
        qual[ir] = max_c
    return pop, qual


def GA_Transport(fo, fc, fcost, dim, nmax, pr, pm):
    oferta = numpy.genfromtxt(fo)
    cerere = numpy.genfromtxt(fc)
    costuri = numpy.genfromtxt(fcost)
    n = len(oferta) * len(cerere)
    pop = gen(dim, oferta, cerere, costuri)
    v = [min(1000. / pop[:, -1])]
    ok = True
    t = 0
    while t < nmax and ok:
        sp, vp = SUS(pop[:, :-1], pop[:, -1], dim, n + 1)
        parinti = numpy.zeros([dim, n + 1])
        parinti[:, :-1] = sp.copy()
        parinti[:, -1] = vp.copy()
        desc = recombinare(parinti, pr, oferta, cerere, costuri)
        descm = mutatie(desc, pm, oferta, cerere, costuri)
        popn, valn = elitism(pop[:, :-1], pop[:, -1], descm[:, :-1], descm[:, -1], dim)
        pop = numpy.zeros([dim, n + 1])
        pop[:, :-1] = popn.copy()
        pop[:, -1] = valn.copy()
        vmax = min(1000. / pop[:, -1])
        i = numpy.argmin(pop[:, -1])
        best = pop[i][:-1]
        v.append(vmax)
        t += 1
        ok = max(pop[:, -1]) != min(pop[:, -1])
    print("Cel mai bun cost găsit: ", vmax)
    print("Soluția de transport:")
    sol = gen_alocare(best, oferta, cerere)
    print(sol)
    fig = grafic.figure()
    grafic.plot(v)
    verificare(sol, oferta, cerere)
    return sol, vmax


# exemplu apel
'''
import problemaTransportNebalansata
s,c=problemaTransportNebalansata.GA_Transport('oferta.txt','cerere.txt','costuri.txt',20,50,0.8,0.1)
'''
