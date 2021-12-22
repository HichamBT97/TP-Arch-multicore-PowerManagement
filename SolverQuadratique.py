# Import the necessary packages
import numpy as np
from cvxopt import matrix
from cvxopt import solvers
from math import *
import knapsack

# initialisation
fmax = 1900
T1 = 0.25
T2 = 0.75
T3 = 0.5
T4 = 0.75
T5 = 1.0
"""
T1 = 0.25
T2 = 0.5
T3 = 0.75
T4 = 0.25
T5 = 0.1
"""

T = np.array([T1, T2, T3, T4, T5])

# calcule de la charge totale de processeur pour les tâches saisie
U = 0.0
for i in range(len(T)) :
    U = U + float(T[i])

# Determination de nombre de cores necessaire
if U < 0 or U > 4 :
    print('Erreur : Charge totale superieur aux capacités des coeurs')
    exit()

#m = entier juste superieur à U
m = ceil(U)

# Calcule de -1/(U*fmax)
h = -1/(U*fmax)

# Define QP parameters (directly)
P = 2*matrix([[0.0, 0.0012/2],[0.0012/2, 0.0]])
q = matrix([0.0001, -0.7669])
G = matrix([[-1.0, 1.0, 0.0, 0.0, h, 0] , [0.0, 0.0, -1.0, 1.0, 0.0, -1]])
h = matrix([-700.0, 1900.0, -1.0, 4.0, -1/m, -U])

# Construct the QP, invoke solver
sol = solvers.qp(P,q,G,h)

# Extract optimal value and solution
(f, n) = sol['x']
sol_min = sol['primal objective']+0.0557

# affichage de la charge totale
print('\n\nla charge totale : '+ str(U))
print('nombre de coeur necessaire : ' + str(m))
print('fréquence necessaire : ' + str(f))
print('Puissance minimale :' + str(sol_min))
print('Facteur de ralentissement : ' + str(fmax/f))


#------------------------------------------------------
# Affectation des tâches : méthode de sac à dos
print('\n\nAffectation des poids au taches : ')
# Calcule des charge en pourcentage
charges = T.T * 100

#affectation des poids : 1 pour charge <= 25 ...
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

print('numero des taches :     ' + str(data_pb[0]))
print('La charges des taches : ' + str(charges))
print('Poids de ces taches :   ' + str(poids))

#Affectation core 0
sol = knapsack.knapsack(charges, poids).solve(capacity)
print('Core0 : ' + str(sol[1]))

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
    print('Core1 : ' + str(list2))

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
    print('Core2 : ' + str(list3))

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
    print('Core3 : ' + str(list4))
