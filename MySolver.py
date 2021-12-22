import numpy as np
from scipy.optimize import minimize

# initialisation
fmax = 1900
f = np.linspace(700, fmax, 50)
T1 = 0.25
T2 = 0.5
T3 = 0.75
T4 = 0.25
T5 = 0.10
T = [T1, T2, T3, T4, T5]


# Calcule de puissance en fonction de f et m
def puiss(x0): # x0 = [m,f]
    m = x0[0]
    f = x0[1]
    return (0.0012*m + 0.0001)*f - (0.7669*m - 0.0557) # objectif

# Calcule de contrainte
def contrainte (x0,U):
    m = x0[0]
    f = x0[1]
    return (fmax/f)*U - m

# calcule de la charge totale U
U = 0.0
for i in range(len(T)) :
    U = U + float(T[i])

# Determination de nombre de cores necessaire
if U > 4 or U < 0 :
    print('Erreur : la charge U > NbrCoeurs')
    exit()

#m = entier juste superieur à U
m = ceil(U)

# boucle de calcule de la puissance pour tout fréquence et m > U
P = []
for i in range(m):
    for j in range(len(f)):
            x0 = [m,f[j]]
            if contrainte (x0,U) > 0 :
                p1 = 10.0
                P.append(p1)
            else :
                p1 = puiss(x0)
                P.append(p1)

# Extraire la puissance minimale calculé ci-dessus
min_P = min(P)

# extract la fréquence équivalent au puissance minimale
for i in range(m):
    for j in range(len(f)):
            x0 = [m,f[j]]
            p1 = puiss(x0)
            if p1 == min_P :
                f_opt = f[j]
                break


# affichage de la charge totale et le nombre de coeur
print('Solution optimal personnel trouvé.')
print('La charge totale : ' + str(U))
print('Nombre de coeurs necessaire :' + str(m))
print('fréquence necessaire : ' + str(f_opt))
print('puissance min : ' + str(min_P))
# Calcule de facteur de ralentissement
s = fmax/f_opt
print('facteur de ralentissement : '+ str(s))