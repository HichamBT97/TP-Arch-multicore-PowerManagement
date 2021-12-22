# Import the necessary packages
import numpy as np
from cvxopt import matrix
from cvxopt import solvers
from math import *
import knapsack

#fonction basé sur Solver quadratique
def Solv_Q (m, U, fmax) :
    # Calcule de -1/(U*fmax)
    h = -1/(U*fmax)

    P = 2*matrix([[0.0, 0.0012/2],[0.0012/2, 0.0]])
    q = matrix([0.0001, -0.7669])
    G = matrix([[-1.0, 1.0, 0.0, 0.0, h, 0] , [0.0, 0.0, -1.0, 1.0, 0.0, -1]])
    h = matrix([-700.0, 1900.0, -1.0, 4.0, -1/m, -U])

    # Construct the QP, invoke solver
    sol = solvers.qp(P,q,G,h)
    (f, n) = sol['x']
    sol_min = sol['primal objective']+0.0557

    # affichage de la charge totale
    print('\tla charge totale : '+ str(U))
    print('\tnombre de coeur necessaire : ' + str(m))
    print('\tfréquence necessaire : ' + str(f))
    print('\tPuissance minimale :' + str(sol_min))
    print('\tFacteur de ralentissement : ' + str(fmax/f))
    return sol_min

def Calc_U(T) :
    # calcule de la charge totale de processeur pour les tâches saisie
    U = 0.0
    for i in range(len(T)) :
        U = U + float(T[i])
    return U

# initialisation
fmax = 1900
T1 = 0.25
T2 = 0.75
T3 = 0.5
T4 = 0.75
T5 = 1.0

T = np.array([T1, T2, T3, T4, T5])
U = Calc_U(T)

# Determination de nombre de cores necessaire
if U < 0 or U > 4 :
    print('Erreur : Charge totale superieur aux capacités des coeurs')
    exit()

#m = entier juste superieur à U
m = ceil(U)
#Solution générale pour toute les taches
print('\nSolution générale pour toutes les tâches :')
Solv_Q(m, U, fmax)


# Affectation des tâches : méthode de sac à dos
# Calcule des charge en pourcentage
charges = T.T * 100

#affectation des poids : 1 pour charge <= 25 ...
print('\nAffectation des poids au taches : ')
poids = []
for i in range(len(charges)):
    if  0 <= charges[i] <= 25 :
        p = 1
        poids.append(p)
    elif 25 <= charges[i] <= 50:
        p = 2
        poids.append(p)
    elif 50 <= charges[i] <= 75:
        p = 3
        poids.append(p)
    else :
        p = 4
        poids.append(p)

#capacity représente le poids, ici par core 100%
capacity=100
data_pb=np.array([[0,1,2,3,4],poids,charges])

print('\tnumero des taches :     ' + str(data_pb[0]))
print('\tLa charges des taches : ' + str(charges))
print('\tPoids de ces taches :   ' + str(poids))

#Allocation des taches
print('\nAllocation des taches : ')

#Affectation core 0
sol = knapsack.knapsack(charges, poids).solve(capacity)
list1 = sol[1]
print('\tCore0 : ' + str(list1))

#Affectation core 1
if m > 1 :
    data_pb2=np.delete(data_pb,sol[1],1)
    poids2=data_pb2[1]
    charges2=data_pb2[2]
    sol2 = knapsack.knapsack(charges2, poids2).solve(capacity)
    list2=[]
    for i in range(len(sol2[1])):
        j=sol2[1][i]
        list2.append(int(data_pb2[0][j]))
    print('\tCore1 : ' + str(list2))

#Affectation core 2
if m  > 2 :
    data_pb3=np.delete(data_pb2,sol2[1],1)
    poids3=data_pb3[1]
    charges3=data_pb3[2]
    sol3 = knapsack.knapsack(charges3, poids3).solve(capacity)

    list3=[]
    for i in range(len(sol3[1])):
        j=sol3[1][i]
        list3.append(int(data_pb3[0][j]))
    print('\tCore2 : ' + str(list3))

#Affectation core 2
if m  > 3 :
    data_pb4=np.delete(data_pb3,sol3[1],1)
    poids4=data_pb4[1]
    charges4=data_pb4[2]
    sol4 = knapsack.knapsack(charges3, poids3).solve(capacity)

    list4=[]
    for i in range(len(sol4[1])):
        j=sol4[1][i]
        list4.append(int(data_pb4[0][j]))
    print('\tCore3 : ' + str(list4))

#Recherche d'une solution minimale pour chaque core
print('\nSolution optimale pour chaque cores :')
#charge totale core 1
print('Core 0 :')
U1 = []
for i in range(len(list1)):
    ui = data_pb[2][list1[i]]
    U1.append(ui)

#Calcul charge totale de coeur 1
Uc1 = Calc_U(U1)/100 
Solv_Q(1, Uc1, fmax)

#charge totale core 2
if m > 1 :
    print('\nCore 1 :')
    U2 = []
    for i in range(len(list2)):
        ui = data_pb[2][list2[i]]
        U2.append(ui)
    #Calcul charge totale de coeur 2
    Uc2 = Calc_U(U2)/100 
    Solv_Q(1, Uc2, fmax)

#charge totale core 3
if m > 2 :
    print('\nCore 2 :')
    U3 = []
    for i in range(len(list3)):
        ui = data_pb[2][list2[i]]
        U3.append(ui)
    #Calcul charge totale de coeur 2
    Uc3 = Calc_U(U3)/100 
    Solv_Q(1, Uc3, fmax)

#charge totale core 4
if m > 3 :
    print('\nCore 3 :')
    U4 = []
    for i in range(len(list4)):
        ui = data_pb[2][list4[i]]
        U4.append(ui)
    #Calcul charge totale de coeur 2
    Uc4 = Calc_U(U4)/100 
    Solv_Q(1, Uc4, fmax)



