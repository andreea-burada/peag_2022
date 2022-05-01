# functie care deseneaza graficul gantt pentru prezentarea rezultatelor problemei de planificare a activitatilor

import numpy
import matplotlib.pyplot as plt

def grafic_gantt(p_m,cost):
    # vezi mai sus

    # I: p_m - plan_masina, masiv 3d cu planificarea operatiilor pe masini
    #          pt. fiecare masina: o matrice cu nr.sarcini linii si 3 coloane (operatie, start, stop),
    #          reprezentind cite o operatie din fiecare sarcina
    #    cost - momentul terminarii executiei tuturor operatiilor
    # E: -

    nrm,nrs,_=numpy.shape(p_m)

    fig=plt.figure(figsize=(10,5))      # se poate imbunatati stabilirea dimensiunilor figurii
    gnt = fig.add_subplot(111)

    gnt.set_ylim(0,nrm+1)           # domeniu vertical
    gnt.set_xlim(0,cost)            # domeniu orizontal

    gnt.set_xlabel("Time")
    gnt.set_ylabel("")

    gnt.set_yticks([i for i in range(1,nrm+1)])
    gnt.set_yticklabels(["Machine "+str(i) for i in range(1,nrm+1)])
    gnt.set_xticks([i for i in range(int(cost)+1)])
    xlabels=[""]*(int(cost)+1)
    for i in range(0,len(xlabels),5):
        xlabels[i]=str(i)
    gnt.set_xticklabels(xlabels)

    gnt.grid(True)
    gnt.set_title("The schedule computed by GA")

    for i in range(nrm):        # pentru fiecare masina
        # lista cu moment inceput si durata pentru fiecare operatie de pe masina i
        operatii=[(p_m[i,j,1], (p_m[i,j,2]-p_m[i,j,1])) for j in range(nrs)]
        inaltime=((i+1)-1.5/5,3/5)       # bara acopera +/-15% fata de linia masinii
        #deseneaza toate operatiile masinii ia
        gnt.broken_barh(operatii,inaltime,facecolors=('aqua','darkturquoise'))
        for j in range(nrs):    # eticheta pe fiecare operatie
            eticheta="O."+str(int(p_m[i,j,0]))
            gnt.text(p_m[i,j,1], i+1, eticheta, horizontalalignment='left', verticalalignment='center')

    # Nume culori utilizabile: https://matplotlib.org/stable/gallery/color/named_colors.html


#import Grafic_Gantt
#Grafic_Gantt.grafic_gantt(plan_masina,cost)


