# Experimento MOORA
# 31-Ago-2022
# MOORA: 
#        https://www.youtube.com/watch?v=4ikr_4OltUw

#
# Doctorado en Tecnología
# Universidad Autónoma de ciudad Juárez
# ACtualizado 06/Feb/2023

import math
import random
from cProfile import label
from decimal import Decimal
from ipaddress import v4_int_to_packed
from re import X

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlsxwriter
from flask import Flask, render_template, request
from matplotlib.transforms import Bbox
from openpyxl import load_workbook

print()
Resultados=[]
ResultadosMoora=pd.DataFrame()
Comparativo=pd.DataFrame()

print("-------------------------------------------")
print("Construcción de la matriz de decisión" )
n=5 # criterios
a=9 # alternativas

A1t={'C1':[0.048,0.053, 0.057, 0.062, 0.066, 0.070, 0.075, 0.079, 0.083],
    'C2':[0.047, 0.052, 0.057, 0.062, 0.066, 0.071, 0.075, 0.079, 0.083],
    'C3':[0.070, 0.066, 0.066, 0.063, 0.070, 0.066, 0.066, 0.066, 0.066],
    'C4':[0.087, 0.081, 0.076, 0.058, 0.085, 0.058, 0.047, 0.035, 0.051],
    'C5':[0.190, 0.058, 0.022, 0.007, 0.004, 0.003, 0.002, 0.002, 0.000] }
A1=pd.DataFrame(A1t)
# Datos para PSO

CP=pd.DataFrame(A1t) # Esta es la primera posición del enjambre
#V=pd.DataFrame(A1t) # Solo para pruebas
PBEST=pd.DataFrame(A1t) #Es la primera mejor posición
print(A1,"\n")

# Contien las evaluaciones cardinales de cada alternativa respecto a cada criterio
EV=["Min", "Min", "Min","Min", "Min"]
#EV=pd.DataFrame(Ev1) # Contien las evaluaciones cardinales de cada alternativa respecto a cada criterio
#print(EV,"\n")


print("-------------------------------------------")
print("Controles iniciales \n" )
wwi=0.7 # Tener un rango menor ayuda a
c1=2.5    # Este influye en la pobabilidad hacia
c2=2.5    # Este influye en la pobabilidad hacia
rangoMin=0 #este rango de valores
rangoMax=1  
T=3    #número de iteraciones para PSO
dim=n*a #dimensión del enjambre

#Pesos por cada criterio
#w=[float(0.123),float(0.099),float(0.043),float(0.343),float(0.392)]
#w=[float(0.2),float(0.2),float(0.2),float(0.2),float(0.2)]
w=[float(0.400),float(0.200),float(0.030),float(0.070),float(0.300)]
#print("Pesos por criterio",w)



######################################################################################################
## MOORA

#Normalizamos con distancia euclidiana
N1 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    P1=0
    St=[]
    for i in range(n):
        #print("A1.iat[i,j]",A1.iat[j,i])
        P1 = float(A1.iat[j,i]**2)
        #print("P1",P1)
        St.append(round((float(P1)),3))
        #print("St",St)
    N0 = pd.DataFrame({'C1':[St[0]],'C2':[St[1]],'C3':[St[2]],'C4':[St[3]],'C5':[St[4]]})
    #print("Norma",Normap)
    N1 = pd.concat([N1,N0], ignore_index=True)
    #print("Norma",Norma)
#print(N1,"\n")

Suma1 = round((N1.sum()),3)
#print("Suma \n", Suma1)
Raiz=[]
for i in range(n):
    Raiz1 = round((math.sqrt(Suma1[i])),3)
    Raiz.append(float(Raiz1))
#print("Raiz \n", Raiz)
#print()

N5 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    N3=[]
    for i in range(n):
        N2 = round((float(A1.iat[j,i]/Raiz[i])),3)
        #print("A",A1.iat[j,i],"raiz",Raiz[i])
        #print("N1", N1)
        N3.append(float(N2))
    #print("Norma", N3)
    N4 = pd.DataFrame({'C1':[N3[0]],'C2':[N3[1]],'C3':[N3[2]],'C4':[N3[3]],'C5':[N3[4]]})
    #print("Norma",N4)
    N5 = pd.concat([N5,N4], ignore_index=True)
#print("Normalización" )
#print(N5,"\n")

#Ponderamos la matriz normalizada por los pesos de los criterios
P4 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    P2=[]
    for i in range(n):
        P1= round((N5.iat[j,i]*w[i]),3)
        #print("w     ",w[i])
        #print("Norma ",N5.iat[j,i])
        #print("          Ponderación",Pond1)
        P2.append(float(P1))
    #print("Norma", N3)
    P3 = pd.DataFrame({'C1':[P2[0]],'C2':[P2[1]],'C3':[P2[2]],'C4':[P2[3]],'C5':[P2[4]]})
    #print("Norma",N4)
    P4 = pd.concat([P4,P3], ignore_index=True)
    #print("\n ------------------")
#print("Ponderamos la matriz normalizada por los pesos de los criterios" )
print(P4,"\n")

#Obtenemos la evaluación de cada alternativa a través de la función de agregación
E4 = pd.DataFrame(columns=['Value'])
for j in range(a):
    E2=[]
    EVL=0.0
    EVLS = 0.0
    EVLR = 0.0
    for i in range(n):
        print("EV[i]",EV[i])
        print("P4[i]",P4.iat[j,i])
        if EV[i]=="Max":
            EVLS = round((float(EVLS) + float(P4.iat[j,i])),3)
            print("SUMA",EVLS)
        else:
            EVLR = round((float(EVLR) + float(P4.iat[j,i])),3)
            print("RESTA",EVLR)
    EVL=round((float(EVLS) - float(EVLR)),3)
    print("      TOTAL",EVL)
    E2.append(float(EVL))
    print("----------------------------")
    #print()
    E3 = pd.DataFrame({'Value':[E2[0]]})
    E4= pd.concat([E4,E3], ignore_index=True)
    #print("E4",E4)

#E4.index = ['A1','A2','A3','A4','A5','A6','A7','A8','A9']
E4['Alternative'] = [1,2,3,4,5,6,7,8,9]
#print("Obtenemos la evaluación de cada alternativa a través de la función de agregación")
#print(E4,"\n")

#print("Ordenar alternativas")
RankFin  = pd.DataFrame(columns=['Value'])
RankFin  = E4.sort_values('Value',ascending=False)
print("Alternativas clasificadas \n",RankFin)
print()   


######################################################################################################
## PSO

# **********************************************************************PRIMERA ITERACIÓN
print("ITERACIÓN # 1 -----------------------")

# Asignamos las primeras posiciones de MOOORA como r1 y r2
Valor1 = int(RankFin.iat[0,1])-1
Valor2 = int(RankFin.iat[1,1])-1
#print("Valores", Valor1, Valor2)

# Dato para comparativos
ValorFin = []
ValorFin.append(int(RankFin.iat[0,1]))
ValorFin.append(0)
CMp1 = pd.DataFrame({'MOORA':[ValorFin[0]],'MOORAFIN':[ValorFin[1]]})
Comparativo = pd.concat([Comparativo,CMp1], ignore_index=True)
#print("Comparativo")
#print(Comparativo)

# Actualizar los valores para r1 y r2
r1 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
r2 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
r1t = []
r2t = []
for j in range(1):
    rP1=0
    rP2=0
    rSt=[]
    for i in range(n):
        rP1 = float(A1.iat[Valor1,i])
        r1t.append(round((float(rP1)),3))
        rP2 = float(A1.iat[Valor2,i])
        r2t.append(round((float(rP2)),3))
#print("r1t")
r1=pd.DataFrame(r1t)
#print("r1",r1,"\n")
#print("r2t")
r2=pd.DataFrame(r2t)
#print("r2",r2,"\n")

print("w(inertia) = ",wwi)
print("c1 = ",c1)
print("c2 = ",c2)
print("No. de iteraciones = ",T,"\n")
print("r1 = ", r1,"\n")
print("r2 = ", r2,"\n")
print("Rango de valores: (",rangoMin,",",rangoMax,")")
print("------------------------------------------- \n")

# CURRENT VELOCITY (V)
V = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for i in range(a):
    Vram1=[]
    for j in range(n):
        Vram=random.uniform(rangoMin,rangoMax)
        #print("Vram",Vram)
        Vram1.append(round((float(Vram)),3))
    Ver1 = pd.DataFrame({'C1':[Vram1[0]],'C2':[Vram1[1]],'C3':[Vram1[2]],'C4':[Vram1[3]],'C5':[Vram1[4]]})
    V = pd.concat([V,Ver1], ignore_index=True)
print("V(1)=")
print(V,"\n")

# CURRENT POSITION (CP)
   #LA PRIMERA MEJOR POSICIÓN, SIEMPRE SERA LA PRIMERA POSICIÓN, NO SE TIENE ANTEDECENTES
print("CP(1)=")
print(CP,"\n")


# FUNCIÓN OBJETIVO, CURRENT FITNESS (CF = Fx)
#print("   Evaluar la función objetivo para obtener el mejor local y global.")

# Normalizamos con distancia euclidiana
N1t0 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    P1t0=0
    Stt0=[]
    for i in range(n):
        #print("CP.iat[j,i]",CP.iat[j,i])
        P1t0 = float(CP.iat[j,i]**2)
        #print("P1",P1t0)
        Stt0.append(round((float(P1t0)),3))
        #print("Stt0",Stt0)
    N0t0 = pd.DataFrame({'C1':[Stt0[0]],'C2':[Stt0[1]],'C3':[Stt0[2]],'C4':[Stt0[3]],'C5':[Stt0[4]]})
    #print("Norma",N0t0)
    N1t0 = pd.concat([N1t0,N0t0], ignore_index=True)
    #print("Norma",N1t0)        
#print(N1t0,"\n")

Suma1t0 = round((N1t0.sum()),3)
#print("Suma \n", Suma1t0)
Raizt0=[]
for i in range(n):
    #print("Suma1t0[i]",Suma1t0[i])
    Raiz1t0 = round((math.sqrt(Suma1t0[i])),3)
    #print("Raiz1t0",Raiz1t0)
    Raizt0.append(float(Raiz1t0))
#print("Raiz \n", Raizt0)
#print()

#print("CP \n",CP)
N5t0 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    N3t0=[]
    for i in range(n):
        N2t0 = round((float(CP.iat[j,i]/Raizt0[i])),3)
        #print("CP",CP.iat[j,i],"raiz",Raizt0[i])
        #print("N2t0", N2t0)
        N3t0.append(float(N2t0))
    #print("Norma", N3t0)
    N4t0 = pd.DataFrame({'C1':[N3t0[0]],'C2':[N3t0[1]],'C3':[N3t0[2]],'C4':[N3t0[3]],'C5':[N3t0[4]]})
    #print("Norma",N4t0)
    N5t0 = pd.concat([N5t0,N4t0], ignore_index=True)
#print("Normalización" )
#print(N5t0,"\n")

#Ponderamos la matriz normalizada por los pesos de los criterios
P4t0 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
for j in range(a):
    P2t0=[]
    for i in range(n):
        P1t0= round((N5t0.iat[j,i]*w[i]),3)
        #print("w     ",w[i])
        #print("Norma ",N5t0.iat[j,i])
        #print("          Ponderación",P1t0)
        P2t0.append(float(P1t0))
    #print("Norma", P3t0)
    P3t0 = pd.DataFrame({'C1':[P2t0[0]],'C2':[P2t0[1]],'C3':[P2t0[2]],'C4':[P2t0[3]],'C5':[P2t0[4]]})
    #print("Norma",P4t0)
    P4t0 = pd.concat([P4t0,P3t0], ignore_index=True)
    #print("\n ------------------")
#print("Ponderamos la matriz normalizada por los pesos de los criterios" )
#print(P4t0,"\n")

#Obtenemos la evaluación de cada alternativa a través de la función de agregación
E4t0 = pd.DataFrame(columns=['Value'])
CF = pd.Series()
Fx= pd.Series()
for j in range(a):
    E2t0=[]
    CFt0=[]
    EVLt0=0.0
    EVLSt0 = 0.0
    EVLRt0 = 0.0
    for i in range(n):
        #print("EV[i]",EV[i])
        if EV[i]=="Max":
            #print("valor inicial",EVLSt0)
            #print("P4[i]",P4t0.iat[j,i])
            EVLSt0 = round((float(EVLSt0) + float(P4t0.iat[j,i])),3)
            #print("SUMA",EVLSt0)
        else:
            #print("valor inicial",EVLRt0)
            #print("P4[i]",P4t0.iat[j,i])
            EVLRt0 = round((float(EVLRt0) + float(P4t0.iat[j,i])),3)
            #print("RESTA",EVLRt0)
    EVLt0=round((float(EVLSt0) - float(EVLRt0)),3)
    #print("      TOTAL",EVLt0)
    E2t0.append(float(EVLt0))
    CFt0.append(float(EVLt0))
    #print("----------------------------")
    #print()

    E3t0 = pd.DataFrame({'Value':[E2t0[0]]})
    E4t0= pd.concat([E4t0,E3t0], ignore_index=True)

    #Este valor también corresponde a la PRIMERA mejor posicion local (CF) y Funcion objetivo(Fx)
    CFxe0 = pd.Series(CFt0)
    #print("CF")
    #print(CF)
    CF = pd.concat([CF,CFxe0], ignore_index=True)

    Fx120 = pd.Series(CFt0)
    Fx = pd.concat([Fx,Fx120], ignore_index=True)
#print("CF NUEVO=")
#print(CF,"\n")
#print("LBF=")
#print(Fx,"\n")
#E4.index = ['A1','A2','A3','A4','A5','A6','A7','A8','A9']

E4t0['Alternative'] = [1,2,3,4,5,6,7,8,9]
#print("Obtenemos la evaluación de cada alternativa a través de la función de agregación")
#print(E4t0,"\n")

#print("Ordenar alternativas")
RankFint0  = pd.DataFrame(columns=['Value'])
RankFint0  = E4t0.sort_values('Value',ascending=False)
#print()
#print("Alternativas clasificadas \n",RankFint0)
#print()
ResultadosMoora = pd.concat([ResultadosMoora,RankFint0], ignore_index=True)

#PAra valores comparativos en EXCEL
ValorFin = []
ValorFin.append(int(RankFint0.iat[0,1]))


# Asignamos las primeras posiciones de MOOORA como r1 y r2
Valor1 = int(RankFint0.iat[0,1])-1
Valor2 = int(RankFint0.iat[1,1])-1
#print("Valores", Valor1, Valor2)
r1 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
r2 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
r1t = []
r2t = []
for j in range(1):
    rP1=0
    rP2=0
    rSt=[]
    for i in range(n):
        rP1 = float(A1.iat[Valor1,i])
        r1t.append(round((float(rP1)),3))
        rP2 = float(A1.iat[Valor2,i])
        r2t.append(round((float(rP2)),3))
#print("r1t",r1t)
#print()
r1=pd.DataFrame(r1t)
#print("r1_Actualizado",r1,"\n")
#print("r2t",r2t)
#print()
r2=pd.DataFrame(r2t)
#print("r2_actualizado",r2,"\n")

# LOCAL BEST POSITION OF EACH PARTICLE UP TO FIRST ITERATION IS JUST ITS CURRENT POSITION
# SINCE THER IS NO PREVIUO ITERATION EXISTS
print()
print("pbest(1)=")
print(PBEST,"\n")

# GLOBAL BEST FITNESS OF ITERATION #1
GBF=[]
#print("FX")
#print(Fx)
pbestt=float(Fx.min())
GBF.append(pbestt)
print("GBF(1)=", GBF,"\n")

# GLOBAL BEST POSITION OF ITERATION 1
Fx_index=0
for j in range(a):
    val1=round(float(GBF[0]),3)
    val2=round(float(Fx[j]),3)
    #print(val1,"=",val2)
    if(val1==val2):
        Fx_index=j
    #print("Fx_index",Fx_index)

columna=[]
for i in range(n):    
    Fx_P1=float(A1.iat[Fx_index,i])
    columna.append(Fx_P1)
    #print(Fx_P1)
#print(columna)
GBP = pd.DataFrame(columna)
#print("gbest(1)=")
#print(GBP)
Resultados.append(Fx_index+1)
print()
print("                 Mejor alternativa= A", Fx_index+1," para la iteración 1")
print("       ------------------------------------------------------------------------------")
#print("Resultados de MOORA",ResultadosMoora)

# Dato para comparativos de EXCEL
ValorFin.append(Fx_index+1)
#print("ValorFin",ValorFin)
#print()
CMp1 = pd.DataFrame({'MOORA':[ValorFin[0]],'MOORAFIN':[ValorFin[1]]})
Comparativo = pd.concat([Comparativo,CMp1], ignore_index=True)
#print("Comparativo")
#print(Comparativo)


# ********************************************************************** ITERACIÓN 2 a N
t=1
par=0
longV1=0
longseg=5
iii=0

while (t<T):

    #print("ENTRE \n")
    print("\n ITERACIÓN #",t+1,"-----------------------","\n")
    print("w(inertia) = ",wwi)
    print("c1 = ",c1)
    print("c2 = ",c2)
    print("No. de iteraciones = ",T,"\n")
    print("r1_new = ",r1,"\n")
    #print(r1.iloc[(len(r1)-n):len(r1)],"\n")
    print("r2_new = ",r2,"\n")
    #print(r2.iloc[(len(r2)-n):len(r2)],"\n")
    print("Rango de valores: (",rangoMin,",",rangoMax,") \n")
    Fxce=[]
    ii=0
    longVel=a*t
    #print("tr12",tr12)
    for j in range(a):
        #print("entre for 2 \n")
        otroV=[]
        otroCP=[]
        #print(len(r1),len(r2))
        tr12=(len(r1)-n)
        CAA=(len(CP)-a)
        GBP12=(len(GBP)-n)
        #print("                                                  CAA",CAA)
        #print("                                                  tr12",tr12)
        #print("                                                  GBP12",GBP12)
        for i in range(n):
            #print("Entre for 1=",i, "de ",n)
            #print("                                             j,i ", j ,i)
            # 1-a) ACTUALIZANDO LA VELOCIDAD            
            #Vtt1=0
            Vtt1=float(V.iat[CAA,i])
            #print("Vtt1",Vtt1)
            #print("wwi",wwi)
            Vt11=float((wwi*Vtt1))
            #print("    Vt11",round((Vt11),3))

            PBESTtt=float((PBEST.iat[CAA,i]))
            #print("          PBESTtt",PBESTtt)
            rr1=float(r1.iat[tr12,0])
            #print("          rr1",rr1)
            CPtt=float((CP.iat[CAA,i])) 
            #print("          CPtt",CPtt)
            #print("          c1",c1)
            Vt12=float((c1*rr1*(PBESTtt-CPtt)))
            #print("    Vt12",round((Vt12),3))
            
            GBPtt=float(GBP.loc[GBP12])
            rr2=float(r2.iat[tr12,0])
            #print("c2",c2)
            #print("rr2",rr2)
            #print("GBPtt",GBPtt)
            #print("CPtt",CPtt)
            Vt13=float((c2*rr2*(GBPtt-CPtt)))          
            #print("    Vt13",round((Vt13),3))
            #print("--- \n")

            VFn=round((float(Vt11+Vt12+Vt13)),3)
            #print("    VFn",round((VFn),3))
            otroV.append(float(VFn))

            # 2-a) ACTUALIZANDO LA PRIMERA  POSICIÓN
            CPtt2=float((CP.iat[CAA,i])) 
            #print("CPtt2", CPtt2,"\n ")
            #print("VFn",VFn,"\n ")
            CPFn=round((float(VFn)+float(CPtt2)),3)
            #print("CPFn",round((CPFn),3),"\n ")
            
            # 2-b) Verificar el rango de los valores
            if CPFn<rangoMin: #<-5
                CPFn=(rangoMin)+.2
            if CPFn>rangoMax: #>5
                CPFn=(rangoMax)-0.2
            #print(" --- Actualizado CPFn",CPFn)
            #print("+++++++++++++++++++++++++++ \n")
            otroCP.append(float(CPFn))
            tr12=tr12+1
            GBP12=GBP12+1
        #print("Salir for 1 \n")

        V.loc[len(V.index)]=otroV
        CP.loc[len(CP.index)]=otroCP
        CAA=CAA+1
        
        #print("------ \n")
    #print("V = \n", V)
    #print("CP= \n", CP)
    #print("Sali for 2 \n")   


    # FUNCIÓN OBJETIVO, CURRENT FITNESS (CF = Fx)
    # Normalizamos con distancia euclidiana
    N1t2 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
    tiempo=a*t
    for j in range(a):
        P1t2=0
        Stt2=[]
        for i in range(n):
            #print("tiempo",tiempo)
            #print("CP.iat[j*t,i]",CP.iat[tiempo,i])
            P1t2 = float(CP.iat[tiempo,i]**2)
            #print("P1",P1t2)
            Stt2.append(round((float(P1t2)),3))
            #print("Stt2",Stt2)
        tiempo=tiempo+1
        N0t2 = pd.DataFrame({'C1':[Stt2[0]],'C2':[Stt2[1]],'C3':[Stt2[2]],'C4':[Stt2[3]],'C5':[Stt2[4]]})
        #print("Norma",Normap)
        N1t2 = pd.concat([N1t2,N0t2], ignore_index=True)
        #print("Norma",N1t2)        
    #print(N1t2,"\n")

    Suma1t2 = round((N1t2.sum()),3)
    #print("Suma \n", Suma1t2)
    Raizt2=[]
    for i in range(n):
        #print("Suma1t2[i]",Suma1t2[i])
        Raiz1t2 = round((math.sqrt(Suma1t2[i])),3)
        #print("Raiz1t2",Raiz1t2)
        Raizt2.append(float(Raiz1t2))
    #print("Raiz \n", Raizt2)
    #print()

    #print("CP \n",CP)
    tiempo=a*t
    N5t2 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
    for j in range(a):
        N3t2=[]
        for i in range(n):
            N2t2 = round((float(CP.iat[tiempo,i]/Raizt2[i])),3)
            #print("CP",CP.iat[tiempo,i],"raiz",Raizt2[i])
            #print("N2t2", N2t2)
            N3t2.append(float(N2t2))
        tiempo=tiempo+1
        #print("Norma", N3t2)
        N4t2 = pd.DataFrame({'C1':[N3t2[0]],'C2':[N3t2[1]],'C3':[N3t2[2]],'C4':[N3t2[3]],'C5':[N3t2[4]]})
        #print("Norma",N4t2)
        N5t2 = pd.concat([N5t2,N4t2], ignore_index=True)
    #print("Normalización" )
    #print(N5t2,"\n")

    #tiempo=a*t
    #Ponderamos la matriz normalizada por los pesos de los criterios
    P4t2 = pd.DataFrame(columns=['C1','C2','C3','C4','C5'])
    for j in range(a):
        P2t2=[]
        for i in range(n):
            P1t2= round((N5t2.iat[j,i]*w[i]),3)
            #print("w     ",w[i])
            #print("Norma ",N5t2.iat[j,i])
            #print("          Ponderación",P1t2)
            P2t2.append(float(P1t2))
        #print("Norma", P3t2)
        P3t2 = pd.DataFrame({'C1':[P2t2[0]],'C2':[P2t2[1]],'C3':[P2t2[2]],'C4':[P2t2[3]],'C5':[P2t2[4]]})
        #print("Norma",P4t2)
        P4t2 = pd.concat([P4t2,P3t2], ignore_index=True)
        #print("\n ------------------")
    #print("Ponderamos la matriz normalizada por los pesos de los criterios" )
    #print(P4t2,"\n")

    #Obtenemos la evaluación de cada alternativa a través de la función de agregación
    E4t2 = pd.DataFrame(columns=['Value'])
    for j in range(a):
        E2t2=[]
        CFt3=[]
        EVLt2=0.0
        EVLSt2 = 0.0
        EVLRt2 = 0.0
        for i in range(n):
            #print("EV[i]",EV[i])
            if EV[i]=="Max":
                #print("valor inicial",EVLSt2)
                #print("P4[i]",P4t2.iat[j,i])
                EVLSt2 = round((float(EVLSt2) + float(P4t2.iat[j,i])),3)
                #print("SUMA",EVLSt2)
            else:
                #print("valor inicial",EVLRt2)
                #print("P4[i]",P4t2.iat[j,i])
                EVLRt2 = round((float(EVLRt2) + float(P4t2.iat[j,i])),3)
                #print("RESTA",EVLRt2)
        EVLt2=round((float(EVLSt2) - float(EVLRt2)),3)
        #print("      TOTAL",EVLt2)
        E2t2.append(float(EVLt2))
        CFt3.append(float(EVLt2))
        #print("----------------------------")
        #print()

        E3t2 = pd.DataFrame({'Value':[E2t2[0]]})
        E4t2= pd.concat([E4t2,E3t2], ignore_index=True)

        #Este valor también corresponde a la PRIMERA mejor posicion local (CF) y Funcion objetivo(Fx)
        CFxe = pd.Series(CFt3)
        #print("CF")
        #print(CF)
        CF = pd.concat([CF,CFxe], ignore_index=True)
        #print("CF NUEVO=")
        #print(CF,"\n")
        Fx12 = pd.Series(CFt3)
        Fx = pd.concat([Fx,Fx12], ignore_index=True)
        #print("LBF=")
    #print("Fx",Fx)
    #print()
    #print("E4t2",E4t2)
    #E4.index = ['A1','A2','A3','A4','A5','A6','A7','A8','A9']
    E4t2['Alternative'] = [1,2,3,4,5,6,7,8,9]
    #print("Obtenemos la evaluación de cada alternativa a través de la función de agregación")
    #print(E4t2,"\n")

    #print("Ordenar alternativas")
    RankFint2  = pd.DataFrame(columns=['Value'])
    #print("Alternativas clasificadas \n",RankFint2)
    RankFint2  = E4t2.sort_values('Value',ascending=False)
    #print("Alternativas clasificadas \n",RankFint2)
    #print()
    ResultadosMoora = pd.concat([ResultadosMoora,RankFint2], ignore_index=True)  

    #PAra valores comparativos en EXCEL
    ValorFin = []
    ValorFin.append(int(RankFint2.iat[0,1])) 

    # verificamos si la posición actual es mejor que la anterior
    zz1=0
    z1=0
    CFactual=len(CF)-a
    CFAnterior=(CFactual)-a
    #print("CP \n")
    #print(CP)
    par=0
    for j in range(a):
        LxCP=[]
        #print(("CF antual, CFAnterior"),CFactual,CFAnterior)
        actual=float(CF.iat[CFactual])
        anterior=float(CF.iat[CFAnterior])

        #print(actual,"<" ,anterior)
        if (actual<anterior) or (actual==anterior): #CP(2)
            #print("entre al IF")
            for z in range(n):
                x1=CP.iat[CFactual,z]
                LxCP.append(round((x1),3))
                #print("CP Actual",round((x1),3))
                #print()

        else:  # CP(1)
            #print("entre al ELSE")
            for z in range(n):
                #print("CFAnterior",CFAnterior)
                x1=CP.iat[CFAnterior,z]
                LxCP.append(round((x1),3))
                #print("CP anterior",round((x1),3))
        #print("LxCP",LxCP)
        PBEST.loc[len(PBEST.index)]=LxCP
        #new_CPLxCont = pd.Series(LxCP)
        #PBEST = pd.concat([PBEST,new_CPLxCont], ignore_index=True)

        CFactual=CFactual+1
        CFAnterior=CFAnterior+1

    
    # GLOBAL BEST FITNESS OF ITERATION 
    #print(RankFint2.iloc[:, 0])
    #print(E4t2)
    #pbestt2=float(max(E4t2))
    pbestt2=float(min(RankFint2.iloc[:, 0]))  
    #print("pbestt2",pbestt2)  
    GBF.append(pbestt2)
    #print("GBF", GBF)

  
    # GLOBAL BEST POSITION OF ITERATION 
    Fx_index=0
    temp_GBP=len(Fx)-a
    for j in range(a):
        val1=round(float(GBF[t]),3)
        val2=round(float(Fx[temp_GBP]),3)
        #print(val1,"=",val2)
        if(val1==val2):
            Fx_index=j
        temp_GBP=temp_GBP+1
    Fx_index=Fx_index+(a*t)
    
    #print(A1)
    #print("++++Entre")
    columna=[]
    for i in range(n):    
        #print("Fx_index,i",Fx_index,i)
        Fx_index2 = Fx_index - (a*t)
        Fx_P1=float(A1.iat[Fx_index2,i])
        columna.append(Fx_P1)
        #print(Fx_P1)
    #print(columna)
    GBP12 = pd.Series(columna)
    GBP = pd.concat([GBP,GBP12], ignore_index=True)
    #print("gbest(1)=")
    #print(GBP,"\n")
    Fx_index=Fx_index-(a*t)
    #print(Fx_index)
    Resultados.append(Fx_index+1)
    #print("           Mejor alternativa= A", Fx_index+1," para la iteración 1")
    #print("      ---------------------------------------------------------------")
    #print()

    # IMPRESIÓN DE RESULTADOS  
    seg=a*t #5*1=5
    #print("V(",t+1,") =")
    #print(V.iloc[seg:seg+a,:],"\n")
    #print("CP(",t+1,") =")
    #print(CP.iloc[seg:seg+a,:],"\n")
    #print("pbest(",t+1,") =")
    #print(PBEST.iloc[seg:seg+a],"\n")
    #print("Fx")
    #print(Fx.iloc[(len(Fx)-a):len(Fx)],"\n")
    #print("GBF =", GBF[t],"\n")
    #print("gbest(",t+1,") =")
    #print(GBP.iloc[(len(GBP)-n):len(GBP)],"\n")
    
    #Mejor=(Fx_index2+1)-(a*t) si fuera CP
    Mejor=(Fx_index+1)
    #print("           Mejor alternativa= A", Mejor," para la iteración",t+1)
    #print("      ---------------------------------------------------------------")
    
    ii=ii+1
    iii=iii+1
    t=t+1

    # Dato para comparativos de EXCEL
    ValorFin.append(Mejor)
    #print("ValorFin",ValorFin)
    #print()
    CMp1 = pd.DataFrame({'MOORA':[ValorFin[0]],'MOORAFIN':[ValorFin[1]]})
    Comparativo = pd.concat([Comparativo,CMp1], ignore_index=True)
    #print("Comparativo")
    #print(Comparativo)    


print()
print()
print("**************************")
print("Resultados Finales")
print("**************************")
#print("   Mejor posición=")
#print(GBP.iloc[(len(GBP)-n):len(GBP)],"\n")
#print("   Mejor óptimo=", GBF[t-1], "\n")
#print(RankFin)

RMOORA=[]
for j in range(a):
    MOORA1=int(RankFin.iat[j,1])
    #print("MM", MOORA1)
    RMOORA.append(MOORA1)
print("   Resultados preliminares de MOORA ",RMOORA, "\n")
#print("   Resultados preliminares de MOORA ",ResultadosMoora, "\n")


print("   Iteración","  Mejor_alternativa")
print("  ---------------------------------")
dd=0
for i in range(T):
    print("       ",i+1,"        ","A",Resultados[i])
print("  --------------------------------- \n")
#print("Comparativo \n", Comparativo)


#######################################################################3
# Para guardar datos en EXCEL

dI={"w(inertia)":wwi, "c1":c1, "c2":c2, "No. de iteraciones":T, "Función Objetivo": [' '], "Rango_Min":rangoMin,"Rango_Max":rangoMax}
dataI = pd.DataFrame(dI)
#dr={"r1":r1,"r2":r2}
#datar = pd.DataFrame(dr)
dataGBF = pd.DataFrame(GBF)
dataGBP = pd.DataFrame(GBP)
dataResult = pd.DataFrame(Resultados)
dataResultM = pd.DataFrame(ResultadosMoora)

with pd.ExcelWriter('Experimentos2/MOORAPSO.xlsx', engine='xlsxwriter') as writer:
    dataI.to_excel(writer, sheet_name='Iniciales')
    dataResult.to_excel(writer, sheet_name='Resultados')
    dataResultM.to_excel(writer, sheet_name='ResultadosMoora')
    r1.to_excel(writer, sheet_name='r1')
    r2.to_excel(writer, sheet_name='r2')
    A1.to_excel(writer, sheet_name='Matriz')
    V.to_excel(writer, sheet_name='Velocity')
    CP.to_excel(writer, sheet_name='Position')
    PBEST.to_excel(writer, sheet_name='PBEST')
    Fx.to_excel(writer, sheet_name='Fx')
    dataGBF.to_excel(writer, sheet_name='GBF')
    dataGBP.to_excel(writer, sheet_name='gbest')

print("  --------------------------------- \n")
print(' Datos guardados el archivo:PSO.xlsx')
print()