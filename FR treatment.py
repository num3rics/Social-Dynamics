# Coder: Lozano Rodriguez, Pablo
# Project: TFG
#
# Notes: Todo el código, itera sobre los archivos y saca todos los resultados
# Instructions: Elegir un tamaño de la red y un número de rondas, y él solo itera sobre todos los valores de factor y porcentaje_falsos.

#                             ====== IMPORTAR PAQUETES ======
import networkx as nx
import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import os
import ast
import collections
from collections import defaultdict
from collections import Counter
#from itertools import izip


def dsum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


from matplotlib.pyplot import cm

contador_vueltas = 0


#                               ====== VARIABLES ======

# Valores de los parametros
##################################################################
# factores=[0.95, 1]                                               #
factores = input("Introduce _factor_ values (separated by spaces): ")
factores = np.array(factores.split())
##################################################################

# Tamanio y conectividad de la red
##################################################################
#N = 20   # N = numero de agentes (nodos) en la red               #
N = input("Introduce the number of nodes in the network: ")
N = int(N)
d = 4   # d = grado inicial de los nodos en la red               #
##################################################################

# Pagos
##################################################################
CC = 7   # R                                                     #
CD = 0   # S                                                     #
DC = 10  # T                                                     #
DD = 0   # P                                                     #
##################################################################

# Reputacion falseada
##################################################################
coste_min = 4   # coste de subir 1u. de reputacion               #
subidas = 0                                                      #
max_subidas = 5   # numero maximo de subidas permitido           #
porcentajes_falsos = [0.5]  # % aprovechados                     #
probsHonestComprar = [0.25]                                      #
probsCheatersNoColab = [0.2, 0.3, 0.4, 0.5]                      #
##################################################################

# Duracion juegos
##################################################################
#NUMrondas = 100   # numero de rondas jugadas                      #
NUMrondas = input("Introduce the number of rounds: ")
NUMrondas = int(NUMrondas)
##################################################################

# Cantidad de los programas
##################################################################
#NUMprogram = 5  # veces que se repite el programa                #
NUMprogram = input("Introduce the number of programs to be run: ")
NUMprogram = int(NUMprogram)
##################################################################

# Variables para crear los heatmaps
# HM_grado = [aprov][factores][rhoD][rhoC]
HM_grado = [[[[0 for u in range(len(probsHonestComprar))] for uu in range(len(probsCheatersNoColab))] for w in range(len(factores))] for h in range(len(porcentajes_falsos))]
HM_colabMreal = [[[[0 for u in range(len(probsHonestComprar))] for uu in range(len(probsCheatersNoColab))] for w in range(len(factores))] for h in range(len(porcentajes_falsos))]
HM_ultcolab = [[[[0 for u in range(len(probsHonestComprar))] for uu in range(len(probsCheatersNoColab))] for w in range(len(factores))] for h in range(len(porcentajes_falsos))]
HM_colabMvisible = [[[[0 for u in range(len(probsHonestComprar))] for uu in range(len(probsCheatersNoColab))] for w in range(len(factores))] for h in range(len(porcentajes_falsos))]
u = 0
uu = 0
w = 0
h = 0

for factor in factores:
    
    if factor==factores[0]:
        h = 0
    else:
        h += 1
    
    for porcentaje_falsos in porcentajes_falsos:
    
        if porcentaje_falsos==porcentajes_falsos[0]:
            u = 0
        else:
            u += 1
        
        for probHonestComprar in probsHonestComprar:
                
            if probHonestComprar==probsHonestComprar[0]:
                uu = 0
            else:
                uu += 1

            for probCheatersNoColab in probsCheatersNoColab:
            
                if probCheatersNoColab==probsCheatersNoColab[0]:
                    w = 0
                else:
                    w += 1
                #                                     ==== Rutas a las carpetas ====
                #pathCarpetas
                if(probHonestComprar==probsHonestComprar[0] and probCheatersNoColab==probsCheatersNoColab[0] and factor==factores[0] and porcentaje_falsos==porcentajes_falsos[0]):
                    os.makedirs('%i' %N + ' nodos y %i' %NUMrondas + ' rondas')
                pathCarpetas='%i' %N + ' nodos y %i' %NUMrondas + ' rondas'

                #pathPrograma y pathScatters
                if (probHonestComprar==probsHonestComprar[0] and probCheatersNoColab==probsCheatersNoColab[0] and factor==factores[0]):
                    os.makedirs(pathCarpetas + '/Proporcion aprovechados %i' %(porcentaje_falsos*100))
                    os.makedirs(pathCarpetas + '/Scatters')
                    os.makedirs(pathCarpetas + '/Histos')
                    os.makedirs(pathCarpetas + '/Wealth')
                pathProporcion=pathCarpetas + '/Proporcion aprovechados %i' %(porcentaje_falsos*100)
                pathScatters=pathCarpetas + '/Scatters'
                pathHistos=pathCarpetas + '/Histos'
                pathWealth=pathCarpetas + '/Wealth'

                #pathHonestComprar
                if(probCheatersNoColab==probsCheatersNoColab[0] and factor==factores[0]):
                    os.makedirs(pathProporcion + '/Probabilidad honestos comprando %i' %(probHonestComprar*100))
                pathHonestComprar=pathProporcion + '/Probabilidad honestos comprando %i' %(probHonestComprar*100)

                #pathCheatersNoColab
                if(factor==factores[0]):
                    os.makedirs(pathHonestComprar + '/Probabilidad cheaters no colab %i' %(probCheatersNoColab*100))
                pathCheatersNoColab=pathHonestComprar + '/Probabilidad cheaters no colab %i' %(probCheatersNoColab*100)

                #pathCheatersNoColab
                #if(factor==factores[0]):
                os.makedirs(pathCheatersNoColab + '/Factor %.2f' %factor)
                pathPrograma=pathCheatersNoColab + '/Factor %.2f' %factor

                #pathGraficas
                os.makedirs(pathPrograma + '/Graficas de %i' %N +' nodos y %i' %NUMrondas + ' rondas')
                pathGraficas=pathPrograma + '/Graficas de %i' %N +' nodos y %i' %NUMrondas + ' rondas'

                #pathArchivos
                os.makedirs(pathPrograma + '/Archivos de %i' %N +' nodos y %i' %NUMrondas + ' rondas')
                pathArchivos=pathPrograma + '/Archivos de %i' %N +' nodos y %i' %NUMrondas + ' rondas'

                #pathJuntar
                if factor==factores[0]:
                    os.makedirs(pathCheatersNoColab + '/Juntar con rhoD %.2f' %probCheatersNoColab)
                pathJuntar=pathCheatersNoColab + '/Juntar con rhoD %.2f' %probCheatersNoColab
                #os.makedirs(pathPrograma + '/Juntar con proporcion %.2f' %porcentaje_falsos)
                #pathJuntar=pathPrograma + '/Juntar con proporcion %.2f' %porcentaje_falsos



                #                                           ====== FUNCIONES ======
                def nuevaAccion(accion, nodo):
                    global pastActions

                    pastActions[nodo] = pastActions[nodo][1:5]+accion

                def actualizaralfa(nodo):
                    global alfa, pastActions

                    d=pastActions[nodo]
                    coop = 0
                    for e in d:
                        if e=='c':
                            coop+=1
                    alfa[nodo] = coop

                def vecinosronda(ronda):
                    global N, red, vecRonda, numvecmedio

                    for i in range(N):
                        vecRonda[ronda-1][i]=len(red.neighbors(i)) 
                    numvecmedio[ronda-1] = np.mean(vecRonda[ronda-1])

                def reputacionmedia(ronda):
                    global alfa, repmedia
                    repmedia[ronda-1]=np.mean(alfa)

                def reputacionmedia_falsa(ronda):
                    global alfa_falso, repmedia_falsa
                    repmedia_falsa[ronda-1]=np.mean(alfa_falso)

                def reputacionmediavecindario(nodo):
                    global red, alfa_falso, repmediavecindario
                    vecs = red.neighbors(nodo)
                    temp = 0
                    temp2 = 0
                    
                    for yy in vecs:
                        temp = temp + alfa_falso[yy]
                    
                    if len(vecs)>0:
                        temp2 = temp/len(vecs)
                    repmediavecindario = temp2
                    
                    return temp2

                def plotrepmedia(repmedia):
                    x = np.arange(len(repmedia))
                    #labels = ['%i' %i for i in range(1,len(repmedia)+1)]
                    plt.bar(x,repmedia, label='Alfa', width=0.5, color='#add8e6')
                    #plt.xticks(x, labels, ha='left')
                    plt.ylabel('Reputacion media real')
                    plt.ylim([0,5])
                    plt.xlabel('Ronda')
                    plt.title('Reputacion media real (RR) en funcion de la ronda')
                    #plt.legend()
                    plt.savefig(pathGraficas +'/Rep Media (RR) por ronda - iteracion %i.png' % (zz+1))
                    plt.close()

                def plotrepmedia_falsa(repmedia):
                    x = np.arange(len(repmedia))
                    #labels = ['%i' %i for i in range(1,len(repmedia)+1)]
                    plt.bar(x,repmedia_falsa, label='Alfa Falso', width=0.5, color='#add8e6')
                    #plt.xticks(x, labels, ha='left')
                    plt.ylabel('Reputacion media visible')
                    plt.ylim([0,5])
                    plt.xlabel('Ronda')
                    plt.title('Reputacion media visible (FR) en funcion de la ronda')
                    #plt.legend()
                    plt.savefig(pathGraficas +'/Rep Media (FR) por ronda - iteracion %i.png' % (zz+1))
                    plt.close()

                def plotnumvecmedio(numvecmedio):
                    x = np.arange(len(numvecmedio))
                    plt.bar(x,numvecmedio,label='Media vecinos', width=0.5, color='#add8e6')
                    plt.ylim([0,N])
                    plt.ylabel('Media')
                    plt.xlabel('Ronda')
                    plt.title('Numero medio de vecinos en funcion de la ronda')
                    #plt.legend()
                    plt.savefig(pathGraficas +'/Media de vecinos por ronda - iteracion %i.png' % (zz+1))
                    plt.close()

                def plothistAlfa():
                    global alfa, N
                    x = np.arange(6)
                    plt.hist(alfa, x, histtype='bar', color='#add8e6')
                    plt.ylabel('Cantidad de nodos')
                    plt.xlabel('Reputacion real')
                    plt.title('Histograma de la reputacion')
                    plt.savefig(pathGraficas +'/Histograma reputacion RR - iteracion %i.png' % (zz+1))
                    plt.close()

                def plothistAlfa_falso():
                    global alfa_falso, N
                    x = np.arange(6)
                    plt.hist(alfa_falso, x, histtype='bar', color='#add8e6')
                    plt.ylabel('Cantidad de nodos')
                    plt.xlabel('Reputacion visible')
                    plt.title('Histograma de la reputacion')
                    plt.savefig(pathGraficas +'/Histograma reputacion FR - iteracion %i.png' % (zz+1))
                    plt.close()

                def plothistVec():
                    global red, N
                    hist = [0 for x in range(N)]
                    temp = [0 for x in range(N)]
                    for i in range(N):
                        temp[i] = len(red.neighbors(i))
                    # hist = [i,j,k,l...,N-1] => i pers. con 0 enlaces, j pers. con 1 enlace, k pers. con 2 enlaces...
                    for j in range(N):   # gente que tenga j enlaces (0,1,2...)
                        for k in range(N):   # recorro la lista temp comparando j con el numero de Vecinos
                            if j==temp[k]:
                                hist[j] = hist[j] + 1
                    #plt.hist(vecRonda[NUMrondas],np.arange(len(vecRonda[NUMrondas])),histtype='bar',color='#add8e6')
                    plt.bar(np.arange(len(hist)),hist,width=0.5,color='#add8e6')
                    plt.ylabel('Cantidad de nodos')
                    plt.xlabel('Numero vecinos')
                    plt.title('Histograma de vecinos')
                    plt.savefig(pathGraficas +'/Histograma vecinos - iteracion %i.png' % (zz+1))
                    plt.close()

                def calcularpagos():
                    global red, colabSig, pagos, acumpagos

                    for q in range(N):
                        vecinosAux = red.neighbors(q)
                        for r in vecinosAux:
                            if((colabSig[q]==True) & (colabSig[r]==True)):
                                pagos[q] = pagos[q] + CC
                                acumpagos[q] = acumpagos[q] + CC
                            if((colabSig[q]==True) & (colabSig[r]==False)):
                                pagos[q] = pagos[q] + CD
                                acumpagos[q] = acumpagos[q] + CD
                            if((colabSig[q]==False) & (colabSig[r]==True)):
                                pagos[q] = pagos[q] + DC
                                acumpagos[q] = acumpagos[q] + DC
                            if((colabSig[q]==False) & (colabSig[r]==False)):
                                pagos[q] = pagos[q] + DD
                                acumpagos[q] = acumpagos[q] + DD

                def probAceptar (nodo):
                    global alfa, alfa_falso
                    delta = reputacionmediavecindario(i)
                    if (alfa_falso[nodo] <= 0):
                        prob = 0
                    elif delta <= alfa_falso[nodo]:
                        prob = 1
                    else:
                        prob = (alfa_falso[nodo])/(delta)

                    return prob

                def probCortar(nodo):
                    probAux = probAceptar(nodo)
                    prob = 1 - probAux

                    return prob

                def agente():
                    # traigo las variables globales
                    global alfa, alfa_falso, colabSig, colabAux, pastActions, red, redSig, repmediavecindario, diccio_nuevo_tc, diccio_nuevo_tr, diccio_nuevo_vc, diccio_nuevo_vr, diccio_antiguo_tc, diccio_antiguo_tr, diccio_antiguo_vc, diccio_antiguo_vr, contador_vueltas, paraScatter, acumpagos, acumpagos_media, acumpagos_media_cheaters, acumpagos_media_reliable
                    # confirmamos que han sido traidas
                    #print("Creadas las variables y la red")

                    ronda = 0

                    ###########################################################################
                    while(ronda < NUMrondas):
                        ronda = ronda + 1
                        alfa_falso = alfa.copy()

                        # Voy a cada nodo
                        # 
                        for i in range(N):
                            # Miro que vecinos tiene
                            # 
                            vecinos=red.neighbors(i)

                            # Compruebo cuanta reputacion tiene cada agente
                            # 
                            colabAux[i]=0
                            for k in vecinos:
                                if pastActions[k][4]=='c':
                                    colabAux[i]+=1

                            # Colaborar o no, y en funcion de ello, comprar o no reputacion
                            # 
                            if i in range(round(porcentaje_falsos*N)):
                                # Cheaters
                                if random.random()<probCheatersNoColab:
                                    colabSig[i]=False
                                else:
                                    if random.random()<=factor*(reputacionmediavecindario(i)/5):
                                        colabSig[i]=True
                                    else:
                                        colabSig[i]=False
                                # Siempre compran reputacion
                                while pagos[i]>coste_min and alfa_falso[i]<reputacionmediavecindario(i):
                                    alfa_falso[i]+=1
                                    pagos[i] = pagos[i] - coste_min
                                    puntos[i] = puntos[i] + 1
                            else:
                                # Honest
                                if random.random()<=factor*(reputacionmediavecindario(i)/5):
                                    colabSig[i]=True
                                else:
                                    colabSig[i]=False
                                    # Solo compran reputacion si no colaboran
                                    if random.random()<probHonestComprar:
                                        while pagos[i]>coste_min and alfa_falso[i]<reputacionmediavecindario(i):
                                            alfa_falso[i]+=1
                                            pagos[i] = pagos[i] - coste_min
                                            puntos[i] = puntos[i] + 1


                            minimoalfa = 5
                            # Recorro todos los vecinos mirando cual tiene menor alfa
                            for m in vecinos:
                                if alfa_falso[m] < minimoalfa:
                                    # Almaceno el valor del alfa mas pequeno y de que vecino es
                                    minimoalfa = alfa_falso[m]
                                    minimo = m
                                elif ronda==1:
                                    minimoalfa = alfa_falso[vecinos[0]]
                                    minimo = vecinos[0]
                            # Elimino el enlace con el que tenga menos alfa
                            for p in red.edges():   # if ((p==(i,minimo)) and (minimoalfa < Tmin)):
                                if ((p==(i,minimo)) and (random.random()<=probCortar(i))):
                                    redSig.remove_edge(i,minimo)
                            # Propongo un enlace aleatoriamente
                            dentro = True
                            c = 0
                            while(dentro==True):
                                aleat1=random.randint(0,N-1)   # enlace a alguien aleatorio
                                if ((aleat1!=i) and (not (aleat1 in vecinos))):   # no enlace el mismo, no haya enlazado ya
                                    if random.random() <= probAceptar(i):   # que yo quiera enlazar con el otro
                                        if random.random() <= probAceptar(aleat1):   # que el otro quiera enlazar conmigo
                                            redSig.add_edge(i,aleat1)   # creo el enlace
                                            dentro = False   # salgo del bucle
                                        else:
                                            dentro = False   # si no cumplo, salgo del bucle sin crearlo
                                    else:
                                        dentro = False   # si no cumple, salgo del bucle sin crearlo
                                else:
                                    c+=1
                                if c==20:
                                    break

                            # Saco la reputacion media real y la falsa de la ronda
                            reputacionmedia(ronda)
                            reputacionmedia_falsa(ronda)
                            # Actualizo el numero de vecinos que tiene cada nodo en la ronda
                            vecinosronda(ronda)

                        # Recalculo alfa y actualizo el pastActions
                        for i in range(N):
                            if colabSig[i]==True:
                                nuevaAccion('c',i)
                            else:
                                nuevaAccion('d',i)
                            
                            actualizaralfa(i)

                            
                            # Y cuantos han colaborado
                            if pastActions[i][4]=='c':
                                cooperadores_reales[ronda-1] += 1
                                porcent_colab[i] += 1
                        #print(alfa[i])

                        if (ronda == 20):
                            fileAlfa.write(str(alfa[0:round(porcentaje_falsos*N)])+'\n')
                            fileAlfa.write(str(alfa[round(porcentaje_falsos*N):N])+'\n')
                            plt.hist((alfa[0:round(porcentaje_falsos*N)],alfa[round(porcentaje_falsos*N):N]), histtype='bar', label=('Cheaters', 'Reliable'), color=('#FFA500','#176117'), alpha=0.5)
                            #plt.hist(alfa[round(porcentaje_falsos*N):N], bins=5, normed=True, histtype='bar', label='Reliable', color='b', alpha=0.5)
                            plt.xlim([0,5])
                            plt.legend(loc='best')
                            #plt.xticks(np.arange(6))
                            plt.ylabel('Frecuency')
                            plt.xlabel('True cooperation index')
                            plt.title('COMP P %.2f ' %porcentaje_falsos + 'F %.2f' %factor + ', rhoD %.2f' %probCheatersNoColab + ', rhoC %.2f' %probHonestComprar)
                            plt.savefig(pathCarpetas + '/T_COMP_P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '.png')
                            plt.close()

                            plt.hist((alfa_falso[0:round(porcentaje_falsos*N)],alfa_falso[round(porcentaje_falsos*N):N]), normed='TRUE', bins=5, histtype='bar', label=('Cheaters', 'Reliable'), color=('#FFA500','#176117'), alpha=0.5)
                            #plt.hist(alfa[round(porcentaje_falsos*N):N], bins=5, normed=True, histtype='bar', label='Reliable', color='b', alpha=0.5)
                            plt.xlim([0,5])
                            plt.legend(loc='best')
                            #plt.xticks(np.arange(6))
                            plt.ylabel('Frecuency')
                            plt.xlabel('Visible cooperation index')
                            plt.title('COMP P %.2f ' %porcentaje_falsos + 'F %.2f' %factor + ', rhoD %.2f' %probCheatersNoColab + ', rhoC %.2f' %probHonestComprar)
                            plt.savefig(pathCarpetas + '/V_COMP_P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '.png')
                            plt.close()

                                
                        # Actualizo la red con los nuevos enlaces
                        red = redSig.copy()
                        # Calculo los pagos con la nueva red
                        calcularpagos()
                        #file.write(str(pagos))
                        
                        acumpagos_media[ronda-1] = np.mean(acumpagos)
                        acumpagos_media_cheaters[ronda-1] = np.mean(acumpagos[0:round(porcentaje_falsos*N)])
                        acumpagos_media_reliable[ronda-1] = np.mean(acumpagos[round(porcentaje_falsos*N):N])
                        acumpagos_sd[ronda-1] = np.std(acumpagos)
                        
                        
                    file.write(str(numvecmedio)+'\n')
                    file.write('fin')
                    file2.write(str(repmedia)+'\n')
                    file2.write('fin')

                    # Guardar la media de puntos comprados y el porcentaje de veces colaboradas
                    for i in range(N):
                        puntos[i] = puntos[i] / NUMrondas
                        porcent_colab[i] = porcent_colab[i] / NUMrondas

                        #alfa_falso[i] = alfa_falso[i]/NUMprogram

                    fileTp.write(", ".join(str(round(e,4)) for e in puntos) + "\n")
                    fileTc.write(", ".join(str(round(e,4)) for e in porcent_colab) + "\n")

                    for i in range(len(porcent_colab)):
                        paraScatter[i]=porcent_colab[i]/N
                    plt.hist(paraScatter, bins=500, range=(0,5))#histtype='bar', color='#add8e6', bins=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,])
                    plt.ylabel('Porcentaje colaboración')
                    plt.xlabel('Puntos')
                    plt.title('Histograma puntos vs percent colab')
                    plt.savefig(pathScatters + '/HistosScatters_P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '.png')
                    plt.close()

                    for key, value in d_tc.items():
                        d_tc[key] = value + alfa[0:round(porcentaje_falsos*N)].count(key)

                    for key, value in d_tr.items():
                        d_tr[key] = value + alfa[round(porcentaje_falsos*N):N].count(key)

                    for key, value in d_vc.items():
                        d_vc[key] = value + alfa_falso[0:round(porcentaje_falsos*N)].count(key)

                    for key, value in d_vr.items():
                        d_vr[key] = value + alfa_falso[round(porcentaje_falsos*N):N].count(key)


                    for i in range(NUMrondas):
                        cooperadores_reales[i] = cooperadores_reales[i]/N


                    file3.write(str(cooperadores_reales)+'\n')
                    file3.write('fin')

                    file4.write(str(repmedia_falsa)+'\n')
                    file4.write('fin')


                def redppal():
                    agente()
                    

                    d = nx.degree(red)
                    node_color=[float(redSig.degree(v)) for v in red] # nx.draw(red, nodelist=d.keys(), node_size=[v * 100 for v in d.values()], node_color=node_color)
                    nx.draw(red, nodelist=d.keys(), node_color=node_color)
                    plt.savefig(pathGraficas +'/red - iteracion %i.png' % (zz+1))
                    plt.close()


                #                                    ====== ITERACION DEL PROGAMA ======

                for zz in range(NUMprogram):   # repeticion del programa
                    #                           ====== VARIABLES PARA GESTIONAR LA RED ======
                    file = open(pathArchivos + "/archivo_red %i tfg.txt" % (zz+1),'w')   # Almacena los vecinos
                    file2 = open(pathArchivos + "/archivo_red %i tfgC.txt" % (zz+1),'w')   # Almacena la reputacion media real
                    file3 = open(pathArchivos + "/archivo_red %i tfgC_ult.txt" % (zz+1),'w')   # Almacena el número real de cooperadores en la ultima ronda
                    file4 = open(pathArchivos + "/archivo_red %i tfgC_FR.txt" % (zz+1),'w')   # Almacena la reputacion media falseada
                    fileTc = open(pathScatters + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '_porcentaje.txt','a')   # Almacena el numero de veces colaboradas
                    fileTp = open(pathScatters + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar+ '_puntos.txt','a')   # Almacena el numero de puntos comprados
                    # True: Reliable
                    fileUtr = open(pathHistos + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '_trueR.txt','a')   # Almacena el numero de veces colaboradas realmente por agente
                    # True: Cheaters
                    fileUtc = open(pathHistos + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '_trueC.txt','a')   # Almacena el numero de veces colaboradas realmente por agente que se aprovecha
                    # Visible: Reliable
                    fileUvr = open(pathHistos + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '_visibleR.txt','a')   # Almacena el numero de veces colaboradas visiblemente por agente
                    # Visible: Cheaters 
                    fileUvc = open(pathHistos + '/P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '_visibleC.txt','a')   # Almacena el numero de veces colaboradas visiblemente por agente que se aprovecha
                    filePagos = open(pathWealth + '/P_%.2f_' %porcentaje_falsos + 'rhoC_%.2f' %probHonestComprar + '_rhoD_%.2f' %probCheatersNoColab + '_F_%.2f' %factor + '_pagos.txt','a')   # Almacena las ganancias acumuladas de toda la red
                    filePagosCheaters = open(pathWealth + '/P_%.2f_' %porcentaje_falsos + 'rhoC_%.2f' %probHonestComprar + '_rhoD_%.2f' %probCheatersNoColab + '_F_%.2f' %factor + '_pagosC.txt','a')   # Almacena las ganancias acumuladas de los cheaters
                    filePagosReliable = open(pathWealth + '/P_%.2f_' %porcentaje_falsos + 'rhoC_%.2f' %probHonestComprar + '_rhoD_%.2f' %probCheatersNoColab + '_F_%.2f' %factor + '_pagosR.txt','a')   # Almacena las ganancias acumuladas de los reliable
                    fileAlfa = open(pathCarpetas + '/T_COMP_P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '.txt','w')
                    red = nx.random_regular_graph(d, N)   # crea un grafo aleatorio de N nodos con grado d
                    redSig = red.copy()
                    
                    # creo y expando las listas hasta los N agentes, con los valores por defecto
                    alfa = [0 for x in range(N)]   # alfa visible de cada integrante de la red
                    alfa_falso = [0 for x in range(N)]   # alfa en el tratamiento falseado (FR)
                    colabSig = [False for x in range(N)]   # indica si el agente colaborara en la ronda o no
                    colabAux = [0 for x in range(N)]   # indica cuantos vecinos de cada agente colaboran
                    pastActions = ['aaaaa' for x in range(N)]   # colaboraciones y defects en las ultimas 5 rondas
                    repmedia = [0 for x in range(NUMrondas)]   # reputacion media por cada ronda
                    acumpagos_media = [0 for x in range(NUMrondas)]   # media de los pagos acumulados
                    acumpagos_media_cheaters = [0 for x in range(NUMrondas)]   # media de los pagos acumulados de los cheaters
                    acumpagos_media_reliable = [0 for x in range(NUMrondas)]   # media de los pagos de los reliable
                    acumpagos_sd = [0 for x in range(NUMrondas)]   # error estandar de la media de los pagos acumulados
                    repmedia_falsa = [0 for x in range(NUMrondas)]   # reputacion media FALSA por cada ronda
                    repmediavecindario = 0   # el alfa medio del vecindario de un nodo
                    vecRonda = [[4 for x in range(N)] for x in range(NUMrondas)]    # vecinos de cada nodo por ronda
                    numvecmedio = [4 for x in range(NUMrondas)]   # numero medio de vecinos en cada ronda
                    pagos = [0 for x in range(N)]   # cuanto lleva ganado cada jugador
                    acumpagos = [0 for x in range(N)]   # cuanto lleva acumulado cada jugador
                    cooperadores_reales = [0 for x in range(NUMrondas)]   # cuantos han colaborado realmente en la ronda
                    cooperadores_falsos = [0 for x in range(NUMrondas)]   # cuantos se ve que han colaborado en la ronda
                    acc = 0   # para ver el progreso de las iteraciones
                    puntos = [0 for x in range(N)]  # puntos que compra un jugador, de media, en las 30 rondas 
                    porcent_colab = [0 for x in range(N)]  # porcentaje de veces que colabora un agente en las 30 rondas
                    paraScatter = [0 for x in range(N)]
                    diccio_temporal = [0 for x in range(8)]
                    if zz==0:
                        d_tc = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
                        d_tr = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
                        d_vc = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
                        d_vr = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}

                    acumuladosR = [0 for x in range(N)]
                    acumuladosC = [0 for x in range(N)]
                    acumuladosR_F = [0 for x in range(N)]
                    acumuladosC_F = [0 for x in range(N)]

                    for i in range (N):   # a cada nodo le asigno un historial aleatorio de acciones
                        for j in range(5):
                            if random.random()>0.5:
                                pastActions[i] = pastActions[i][1:5]+'c'
                            else:
                                pastActions[i] = pastActions[i][1:5]+'d'

                    for i in range(N):  
                        if pastActions[i][4]=='c':
                            colabSig[i] = True
                        else:
                            colabSig[i] = False
                    #cooperadores[0]=cooperadores[0]/N
                    #print(cooperadores)
                    for i in range(N):
                        actualizaralfa(i)

                    # llamo  las funciones
                    file.write("Iteracion %i\n" % (zz+1))
                    file2.write("Iteracion %i\n" %(zz+1))
                    #file3.write("Iteracion %i\n" %(zz+1))
                    file4.write("Iteracion %i\n" %(zz+1))
                    redppal()
                    
                    if zz==NUMprogram-1:
                        contador_vueltas += 1
                        #print("contador vueltas %i" %contador_vueltas)
                        #print("NUMprogram %i" %NUMprogram)

                        #for key, val in d_tc.items():
                        #    d_tc[key]=val/(NUMprogram)
                        diccio_temporal=list(d_tc.values())
                        #print(diccio_temporal)
                        fileUtc.write(", ".join(str(e) for e in diccio_temporal) + "\n")
                        #for key, val in d_tr.items():
                        #    d_tr[key]=val/(NUMprogram)
                        diccio_temporal=list(d_tr.values())
                        #print(diccio_temporal)
                        fileUtr.write(", ".join(str(e) for e in diccio_temporal) + "\n")

                        #for key, val in d_vc.items():
                        #    d_vc[key]=val/(NUMprogram)
                        diccio_temporal=list(d_vc.values())
                        #print(diccio_temporal)
                        fileUvc.write(", ".join(str(e) for e in diccio_temporal) + "\n")
                        #for key, val in d_vr.items():
                        #    d_vr[key]=val/(NUMprogram)
                        diccio_temporal=list(d_vr.values())
                        #print(diccio_temporal)
                        fileUvr.write(", ".join(str(e) for e in diccio_temporal) + "\n")

                    file.close()
                    file2.close()
                    
                    #acumpagos_media_total = acumpagos_media_total / 5
                    #filePagos.write(", ".join(str(e) for e in acumpagos_media_total) + "\n")
                    #acumpagos_media_total = np.around(acumpagos_media_total, decimals=5)
                    # Toda la red
                    filePagos.write(", ".join(str(e) for e in acumpagos_media) + "\n")
                    filePagos.close()
                    # Los cheaters
                    filePagosCheaters.write(", ".join(str(e) for e in acumpagos_media_cheaters) + "\n")
                    filePagosCheaters.close()
                    # Los reliable
                    filePagosReliable.write(", ".join(str(e) for e in acumpagos_media_reliable) + "\n")
                    filePagosReliable.close()
                    #    ====== FIN DEL PROGRAMA ======


                # Graficamos la evolucion de la red con los archivos de la parte anterior del programa

                aux0 = [0 for x in range(NUMrondas)]
                aux1 = [0 for x in range(NUMrondas)]
                aux2 = [0 for x in range(NUMrondas)]
                aux3 = [0 for x in range(NUMrondas)]

                std_error = [0 for x in range(NUMrondas)]
                std_errorC = [0 for x in range(NUMrondas)]
                std_errorC_FR = [0 for x in range(NUMrondas)]

                coop00 = [0 for x in range(NUMrondas)]

             
                ########################################################################################
                ########################################################################################


                # saco de todos los archivos los datos, y creo uno que los almacene
                graphicfile=open(pathArchivos + '/graficar.txt', mode='w')
                for i in range(zz):
                    filename = (pathArchivos + '/archivo_red %i tfg.txt' %(i+1))
                    with open(filename) as input_data:
                        # Se salta todo hasta el bloque que interesa:
                        for line in input_data:
                            if line.strip() == 'Iteracion %i'%(i+1):  # O la condicion que se requiera
                                break
                        # Lee hasta el siguiente bloque:
                        for line in input_data:  # Sigue leyendo el resto del archivo
                            if line.strip() == 'fin':
                                break
                            line = ast.literal_eval(line)
                            graphicfile.write(str(line)+'\n')
                graphicfile.close()


                graphicfile=open(pathArchivos + '/graficar.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux0[i]=line[i]+aux0[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux0[i]=round(aux0[i],4)
                #print('aux0:')
                #print(aux0)

                aux1=aux0.copy()
                for i in range(NUMrondas):
                    aux1[i]=aux1[i]/zz
                for i in range(NUMrondas):
                    aux1[i]=round(aux1[i],4)
                #print('aux1:')
                #print(aux1)
                # ya tengo la ecuacion [1]

                with open(pathJuntar + "/juntar.txt", "a") as myfile:
                    myfile.write(str(aux1)+"\n")

                # <Guardo el dato para el HEATMAP>
                HM_grado[u][h][w][uu]=aux1[-1]                 
                # </Guardo el dato para el HEATMAP>

                ###################################################################
                graphicfile=open(pathArchivos + '/graficar.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux2[i]=(line[i]-aux1[i])**2+aux2[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux2[i]=round(aux2[i],4)
                #print('aux2:')
                #print(aux2)

                aux3=aux2.copy()
                for i in range(NUMrondas):
                    aux3[i]=aux3[i]/zz
                for i in range(NUMrondas):
                    aux3[i]=round(aux3[i],4)
                #print('aux3:')
                #print(aux3)
                # ya tengo la ecuacion [2]

                sigmak = [0 for x in range(NUMrondas)]

                for i in range(NUMrondas):
                    sigmak[i]=math.sqrt(aux3[i])   # varianza = sigmak

                for i in range(NUMrondas):
                    sigmak[i]=round(sigmak[i],4)
                #print('sigmak')
                #print(sigmak)


                ##############
                # Standard error
                for i in range(NUMrondas):
                    std_error[i]=sigmak[i]/math.sqrt(zz)

                ##############
                with open(pathJuntar + "/juntar.txt", "a") as myfile:
                    myfile.write(str(std_error)+"\n")

                ########################################################################################

                # Graficar
                x=np.arange(NUMrondas)

                plt.plot(x, aux1)
                #plt.plot(x,aux1, label='Ec', width=0.5, color='#add8e6', yerr=std_error, errorevery=10)
                plt.errorbar(x, aux1, yerr=std_error, errorevery=10)
                plt.ylim([0,N])
                plt.ylabel('Valor medio del grado del nodo')
                plt.xlabel('Ronda')
                plt.title('Grado del nodo')
                #plt.legend()
                plt.savefig(pathPrograma + '/Grado del nodo.png')
                #plt.show()
                plt.close()



                ########################################################################################
                ########################################################################################


                aux00 = [0 for x in range(NUMrondas)]
                aux11 = [0 for x in range(NUMrondas)]
                aux22 = [0 for x in range(NUMrondas)]
                aux33 = [0 for x in range(NUMrondas)]

                # saco de todos los archivos los datos, y creo uno que los almacene
                graphicfile=open(pathArchivos + '/graficarC.txt', mode='w')
                for i in range(zz):
                    filename = (pathArchivos + '/archivo_red %i tfgC.txt' %(i+1))
                    with open(filename) as input_data:
                        # Skips text before the beginning of the interesting block:
                        for line in input_data:
                            if line.strip() == 'Iteracion %i'%(i+1):  # Or whatever test is needed
                                break
                        # Reads text until the end of the block:
                        for line in input_data:  # This keeps reading the file
                            if line.strip() == 'fin':
                                break
                            line = ast.literal_eval(line)
                            graphicfile.write(str(line)+'\n')
                graphicfile.close()


                graphicfile=open(pathArchivos + '/graficarC.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux00[i]=line[i]+aux00[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux00[i]=round(aux00[i],4)

                aux11=aux00.copy()
                for i in range(NUMrondas):
                    aux11[i]=aux11[i]/zz
                for i in range(NUMrondas):
                    aux11[i]=round(aux11[i],4)

                with open(pathJuntar + "/juntarC.txt", "a") as myfile:
                    myfile.write(str(aux11)+"\n")

                #print(aux11[-1])
                # <Guardo el dato para el HEATMAP>
                HM_colabMreal[u][h][w][uu]=aux11[-1] 
                # </Guardo el dato para el HEATMAP>
                # 
                ###################################################################
                graphicfile=open(pathArchivos + '/graficarC.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux22[i]=(line[i]-aux11[i])**2+aux22[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux22[i]=round(aux22[i],4)

                aux33=aux22.copy()
                for i in range(NUMrondas):
                    aux33[i]=aux33[i]/zz
                for i in range(NUMrondas):
                    aux33[i]=round(aux33[i],4)

                sigmac = [0 for x in range(NUMrondas)]

                for i in range(NUMrondas):
                    sigmac[i]=math.sqrt(aux33[i])

                for i in range(NUMrondas):
                    sigmac[i]=round(sigmac[i],4)

                ##############################
                #Standard error

                for i in range(NUMrondas):
                    std_errorC[i] = sigmac[i]/math.sqrt(zz)

                ##############################

                with open(pathJuntar + "/juntarC.txt", "a") as myfile:
                    myfile.write(str(std_errorC)+"\n")

                # Graficar
                x=np.arange(NUMrondas)   # antes xx = ...

                plt.plot(x, aux11)
                #plt.plot(x,aux1, label='Ec', width=0.5, color='#add8e6', yerr=std_error, errorevery=10)
                plt.errorbar(x, aux11, yerr=std_errorC, errorevery=10)
                plt.ylim([0,5])
                plt.ylabel('Valor medio de colaboraciones')
                plt.xlabel('Ronda')
                plt.title('Numero medio de colaboraciones reales')
                #plt.legend()
                plt.savefig(pathPrograma + '/Numero medio de colaboraciones reales.png')
                #plt.show()
                plt.close()


                ########################################################################################
                ########################################################################################


                graphicfile=open(pathArchivos + '/graficarC_ult.txt', mode='w')
                for i in range(zz):
                    filename = (pathArchivos + '/archivo_red %i tfgC_ult.txt' %(i+1))
                    with open(filename) as input_data:
                        # Reads text until the end of the block:
                        for line in input_data:  # This keeps reading the file
                            if line.strip() == 'fin':
                                break
                            line = ast.literal_eval(line)
                            graphicfile.write(str(line)+'\n')
                graphicfile.close()

                #print('ratio:')
                graphicfile=open(pathArchivos + '/graficarC_ult.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        coop00[i]=line[i]+coop00[i]
                for i in range(NUMrondas):
                    coop00[i]=coop00[i]/zz
                    coop00[i]=round(coop00[i],4)
                    
                #print(coop00)

                graphicfile.close()

                with open(pathJuntar + "/juntarC_ult.txt", "a") as myfile:
                    myfile.write(str(coop00)+"\n")

                # <Guardo el dato para el HEATMAP>
                # 
                HM_ultcolab[u][h][w][uu]=coop00[-1] 
                # </Guardo el dato para el HEATMAP>

                ########################################################################################

                # Graficar
                x=np.arange(NUMrondas)

                plt.plot(x,coop00)
                #plt.bar(x,coop00, label='Ec', width=0.5, color='#add8e6')
                plt.ylim([0,1])
                plt.ylabel('Ratio')
                plt.xlabel('Ronda')
                plt.title('Ratio "cooperadores reales / agentes totales"')
                #plt.legend()
                plt.savefig(pathPrograma + '/Ratio.png')
                #plt.show()
                plt.close()

                ########################################################################################
                ########################################################################################

                aux000 = [0 for x in range(NUMrondas)]
                aux111 = [0 for x in range(NUMrondas)]
                aux222 = [0 for x in range(NUMrondas)]
                aux333 = [0 for x in range(NUMrondas)]

                # saco de todos los archivos los datos, y creo uno que los almacene
                graphicfile=open(pathArchivos + '/graficarC_FR.txt', mode='w')
                for i in range(zz):
                    filename = (pathArchivos + '/archivo_red %i tfgC_FR.txt' %(i+1))
                    with open(filename) as input_data:
                        # Skips text before the beginning of the interesting block:
                        for line in input_data:
                            if line.strip() == 'Iteracion %i'%(i+1):  # Or whatever test is needed
                                break
                        # Reads text until the end of the block:
                        for line in input_data:  # This keeps reading the file
                            if line.strip() == 'fin':
                                break
                            line = ast.literal_eval(line)
                            graphicfile.write(str(line)+'\n')
                graphicfile.close()


                graphicfile=open(pathArchivos + '/graficarC_FR.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux000[i]=line[i]+aux000[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux000[i]=round(aux000[i],4)
                #print('aux00:')
                #print(aux00)

                aux111=aux000.copy()
                for i in range(NUMrondas):
                    aux111[i]=aux111[i]/zz
                for i in range(NUMrondas):
                    aux111[i]=round(aux111[i],4)
                #print('aux111:')
                #print(aux111)
                # ya tengo la ecuacion [1]

                with open(pathJuntar + "/juntarC_FR.txt", "a") as myfile:
                    myfile.write(str(aux111)+"\n")

                # <Guardo el dato para el HEATMAP>
                HM_colabMvisible[u][h][w][uu]=aux111[-1] 
                # </Guardo el dato para el HEATMAP>
                # 
                ###################################################################
                graphicfile=open(pathArchivos + '/graficarC_FR.txt', mode='r')
                for line in graphicfile:
                    line = line.strip()
                    line = ast.literal_eval(line)
                    for i in range(NUMrondas):
                        aux222[i]=(line[i]-aux111[i])**2+aux222[i]
                graphicfile.close()

                for i in range(NUMrondas):
                    aux222[i]=round(aux222[i],4)
                #print('aux22:')
                #print(aux22)

                aux333=aux222.copy()
                for i in range(NUMrondas):
                    aux333[i]=aux333[i]/zz
                for i in range(NUMrondas):
                    aux333[i]=round(aux333[i],4)
                #print('aux33:')
                #print(aux33)
                # ya tengo la ecuacion [2]

                sigmac = [0 for x in range(NUMrondas)]

                for i in range(NUMrondas):
                    sigmac[i]=math.sqrt(aux333[i])

                for i in range(NUMrondas):
                    sigmac[i]=round(sigmac[i],4)
                #print('sigmac')
                #print(sigmac)

                ##############################
                #Standard error

                for i in range(NUMrondas):
                    std_errorC_FR[i] = sigmac[i]/math.sqrt(zz)

                ##############################

                with open(pathJuntar + "/juntarC_FR.txt", "a") as myfile:
                    myfile.write(str(std_errorC_FR)+"\n")

                # Graficar
                x=np.arange(NUMrondas)

                plt.plot(x, aux111)
                #plt.plot(x,aux1, label='Ec', width=0.5, color='#add8e6', yerr=std_error, errorevery=10)
                plt.errorbar(x, aux111, yerr=std_errorC_FR, errorevery=10)
                plt.ylim([0,5])
                plt.ylabel('Valor medio de colaboraciones')
                plt.xlabel('Ronda')
                plt.title('Numero medio de colaboraciones visibles')
                #plt.legend()
                plt.savefig(pathPrograma + '/Numero medio de colaboraciones visibles.png')
                #plt.show()
                plt.close()


                ################################################################################################################
                ################################################################################################################

                ## JUNTANDO COLAB TRUE & FALSE
                x = np.arange(NUMrondas)
                plt.scatter(x, aux11, c='b',  marker='>', label="Real", s=80)
                plt.errorbar(x, aux11, yerr=std_errorC)
                plt.scatter(x, aux111, c='r', marker=">", label="Visible (falseada)", s=80)
                plt.errorbar(x, aux111, yerr=std_errorC_FR)
                plt.ylim([0,5])
                plt.xlim([0,NUMrondas])
                plt.ylabel('Índice de cooperación')
                plt.xlabel('Ronda')
                plt.title('CM P %.2f' %porcentaje_falsos + ', F %.2f' %factor + ', rhoD %.2f' %probCheatersNoColab + ', rhoC %.2f' %probHonestComprar)
                plt.legend(loc=4)
                plt.savefig(pathCarpetas + '/CM_P_%.2f_' %porcentaje_falsos + 'F_%.2f' %factor + '_rhoD_%.2f' %probCheatersNoColab + '_rhoC_%.2f' %probHonestComprar + '.png')
                plt.close()



                #########################################################################################
                ##################################   JUNTARLAS   ########################################
                #########################################################################################



                # Al llegar al final de los valores de Tmin o de Factores, promediamos todas las iteraciones

                if (factor==factores[-1]):# or (probHonestComprar==probsHonestComprar[-1]):

                    if(factor==factores[-1]):
                        NUMfactor = 2#len(factores)
                        #print("NUMfactor=len(factores)")
                    elif(probHonestComprar==probsHonestComprar[-1]):
                        NUMfactor = 2#len(probsHonestComprar)
                        #print("NUMfactor=len(probHonestComprar)")

                    vector_juntar = [[0 for x in range(NUMrondas)] for x in range(NUMfactor)]
                    vector_juntar_std_error = [[0 for x in range(NUMrondas)] for x in range(NUMfactor)]
                    j=0

                    graphicfile=open(pathJuntar + "/juntar.txt", mode='r')
                    for line in graphicfile:
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar[j] = line
                        line = graphicfile.readline()
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar_std_error[j] = line
                        j+=1
                    graphicfile.close()


                    x = np.arange(NUMrondas)
                    
                    color=iter(cm.rainbow(np.linspace(0,1,5)))
                    #j=NUMfactor-1
                    j=0

                    #for i in reversed(range(NUMfactor)):
                    for j in range(NUMfactor):
                        label="Factor: " + str(factores[j])
                        c=next(color)
                        #plt.plot(x,vector_juntar[j])
                        plt.errorbar(x,vector_juntar[j], yerr=vector_juntar_std_error[j], errorevery=10, label=label, color=c)
                        plt.ylim([0,N])
                        plt.ylabel('Grado del nodo')
                        plt.xlabel('Ronda')
                        plt.title('Grado del nodo en funcion de factor')
                        plt.legend(loc='best')
                        plt.savefig(pathCarpetas+ '/Grado aprovechados %.2f' %porcentaje_falsos + ', rhoC %.2f' %probHonestComprar +' y rhoD %.2f' %probCheatersNoColab + '.png')
                    #plt.show()
                    plt.close()

                    ###############################################################################
                    ###############################################################################
                    ###############################################################################
                    ###############################################################################

                    vector_juntar = [[0 for x in range(NUMrondas)] for x in range(NUMfactor)]
                    j=0

                    graphicfile=open(pathJuntar + "/juntarC.txt", mode='r')
                    for line in graphicfile:
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar[j] = line
                        line = graphicfile.readline()
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar_std_error[j] = line
                        j+=1
                    graphicfile.close()

                    x = np.arange(NUMrondas)

                    color=iter(cm.rainbow(np.linspace(0,1,5)))
                    j=0

                    for j in range(NUMfactor):
                        label="Factor: " + str(factores[j])
                        c=next(color)
                        #plt.plot(x,vector_juntar[j], label=label, color=c)
                        plt.errorbar(x,vector_juntar[j], yerr=vector_juntar_std_error[j], errorevery=10, label=label, color=c)
                        plt.ylim([0,5])
                        plt.ylabel('Colaboracion media real')
                        plt.xlabel('Ronda')
                        plt.title('Colaboracion media real en funcion de factor')
                        plt.legend(loc='best')
                        plt.savefig(pathCarpetas + '/Colab media real aprovechados %.2f' %porcentaje_falsos + ', rhoC %.2f' %probHonestComprar +' y rhoD %.2f' %probCheatersNoColab + '.png')
                    #plt.show()
                    plt.close()

                    ###############################################################################
                    ###############################################################################
                    ###############################################################################
                    ###############################################################################

                    vector_juntar = [[0 for x in range(NUMrondas)] for x in range(NUMfactor)]
                    j=0

                    graphicfile=open(pathJuntar + "/juntarC_ult.txt", mode='r')
                    for line in graphicfile:
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar[j] = line
                        j+=1
                    graphicfile.close()

                    x = np.arange(NUMrondas)

                    color=iter(cm.rainbow(np.linspace(0,1,5)))
                    j=0

                    for j in range(NUMfactor):
                        label="Factor: " + str(factores[j])
                        c=next(color)
                        plt.plot(x,vector_juntar[j], label=label, color=c)
                        plt.ylim([0,1])
                        plt.ylabel('Ratio ultima colaboracion')
                        plt.xlabel('Ronda')
                        plt.title('Ultima colaboracion en funcion de factor')
                        plt.legend(loc='best')
                        plt.savefig(pathCarpetas + '/Ultima colab aprovechados %.2f' %porcentaje_falsos + ', rhoC %.2f' %probHonestComprar +' y rhoD %.2f' %probCheatersNoColab + '.png')
                    #plt.show()
                    plt.close()

                    ###############################################################################
                    ###############################################################################
                    ###############################################################################
                    ###############################################################################

                    vector_juntar = [[0 for x in range(NUMrondas)] for x in range(NUMfactor)]
                    j=0

                    graphicfile=open(pathJuntar + "/juntarC_FR.txt", mode='r')
                    for line in graphicfile:
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar[j] = line
                        line = graphicfile.readline()
                        line = line.strip()
                        line = ast.literal_eval(line)
                        vector_juntar_std_error[j] = line
                        j+=1
                    graphicfile.close()

                    x = np.arange(NUMrondas)

                    color=iter(cm.rainbow(np.linspace(0,1,5)))
                    j=0

                    for j in range(NUMfactor):
                        label="Factor: " + str(factores[j])
                        c=next(color)
                        #plt.plot(x,vector_juntar[j], label=label, color=c)
                        plt.errorbar(x,vector_juntar[j], yerr=vector_juntar_std_error[j], errorevery=10, label=label, color=c)
                        plt.ylim([0,5])
                        plt.ylabel('Colaboracion media visible')
                        plt.xlabel('Ronda')
                        plt.title('Colaboracion media visible en funcion de factor')
                        plt.legend(loc='best')
                        plt.savefig(pathCarpetas + '/Colab media visible aprovechados %.2f' %porcentaje_falsos + ', rhoC %.2f' %probHonestComprar +' y rhoD %.2f' %probCheatersNoColab + '.png')
                    #plt.show()
                    plt.close()

with open(pathCarpetas + "/heatmap_grado.txt", "a") as myfile:
    myfile.write(str(HM_grado)+"\n")

with open(pathCarpetas + "/heatmap_ultcolab.txt", "a") as myfile:
    myfile.write(str(HM_ultcolab)+"\n")

with open(pathCarpetas + "/heatmap_colabMvisible.txt", "a") as myfile:
    myfile.write(str(HM_colabMvisible)+"\n")

with open(pathCarpetas + "/heatmap_colabMreal.txt", "a") as myfile:
    myfile.write(str(HM_colabMreal)+"\n")
