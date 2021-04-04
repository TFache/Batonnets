"""
	Jeu des bâtonnets

	joueur = 1  => ordinateur
	joueur = -1 => humain
"""

# Constantes globales

# RECOMPENSE = valeur donnée à un état terminal dans une partie gagnée
# si la partie est perdue, la valeur est -RECOMPENSE.
# Toutes les valeurs minimax sont comprises dans [-RECOMPENSE, RECOMPENSE]
import math

RECOMPENSE = 1


def affiche(N):
    # Affichage du jeu
    s = ""
    for i in range(N):
        s = s + "|"
    print(s)


def humainJoue(N):
    # Retourne le coup joué par l'humain
    coups = coupsPossibles(N)

    print("choix possibles : ")
    print(coups)

    n = None
    while n not in coups:
        n = int(input("combien de bâtonnets ? "))
    return n


def ordiJoue(N):
    # Retourne le coup joué par l'ordinateur
    coups = coupsPossibles(N)

    maxi = -math.inf

    # Détermination du meilleur coup
    meilleurCoup = 1
    for coup in coups:
        v = valeurMin(N - coup)
        if v > maxi:
            meilleurCoup = coup
            maxi = v

    if meilleurCoup == 1:
        print('Je vais gagner !')
    else:
        print('Je vais perdre...')
    return meilleurCoup


def coupsPossibles(N):
    coups = []
    for i in range(1, 4):
        if i <= N:
            coups.append(i)

    return coups


def valeurMax(N):
    """
	Retourne la valeur minimax d'un noeud MAX avec N batônnets

	Si le joueur précédent a perdu (N=0),
	    retourne RECOMPENSE car ordi a gagné
	"""

    # pour connaître le nombre total de noeuds explorés:
    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1
    valeur = -math.inf
    if N == 0:
        valeur = RECOMPENSE
    else:
        for coup in coupsPossibles(N):
            nval = valeurMin(N - coup)
            if nval > valeur:
                valeur = nval
    return valeur


def valeurMin(N):
    """
	Retourne la valeur minimax d'un noeud MINI avec N batônnets

	Si le joueur précédent a perdu (N=0),
	    retourne -RECOMPENSE car ordi a perdu
	"""

    # pour connaître le nombre total de noeuds explorés:
    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1
    valeur = math.inf
    if N == 0:
        valeur = -RECOMPENSE
    else:
        for coup in coupsPossibles(N):
            nval = valeurMax(N - coup)
            if nval < valeur:
                valeur = nval
    return valeur


def valeurMinAB(N, alpha, beta):

    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1

    val = math.inf

    if N == 0:
        return -RECOMPENSE
    for coup in coupsPossibles(N):
        val = min(val, valeurMaxAB(N - coup, alpha, beta))
        if alpha >= val:
            return val
        beta = min(beta, val)

    return val


def valeurMaxAB(N, alpha, beta):

    global nbNoeudsExplores
    nbNoeudsExplores = nbNoeudsExplores + 1

    val = -math.inf

    if N == 0:
        return RECOMPENSE
    for coup in coupsPossibles(N):
        val = max(val, valeurMinAB(N - coup, alpha, beta))
        if val >= beta:
            return val
        alpha = max(alpha, val)

    return val

def ordiJoueAlphaBeta(N):
	# Retourne le coup joué par l'ordinateur

	# Détermination du meilleur coup

	coups = coupsPossibles(N)

	# initialisation des variables (on prend le premier noeud possible)

	meilleurCoup = coups[0]
	valeurMeilleursCoup = valeurMinAB(N - meilleurCoup, -math.inf, math.inf)

	# comparaison avec les autres noeuds
	for coup in coups[1:]:

		valMax = valeurMinAB(N - coup, -math.inf, math.inf)

		if valMax > valeurMeilleursCoup:
			meilleurCoup = coup
			valeurMeilleursCoup = valMax

	if valeurMeilleursCoup == 1:
		print("Je vais gagner")
	else:
		print("Je vais perdre")

	# meilleur coup
	return meilleurCoup

######### Programme principal ##########

# Etat initial
N = 27

# Qui commence ?
joueur = int(input("Qui commence ? (1 pour ordinateur, -1 pour humain) "))

# Boucle de jeu (tant que la partie n'est pas finie)
while N > 0:
    # afficher l'état du jeu:
    affiche(N)

    if joueur == -1:
        n = humainJoue(N)
    else:
        nbNoeudsExplores = 0
        n = ordiJoueAlphaBeta(N)#n = ordiJoue(N)
        print("(après une réflexion basée sur l'exploration de " + str(nbNoeudsExplores) + " noeuds)")
        print("je prends " + str(n) + " batonnets")

    # jouer le coup
    N = N - n

    # passer à l'autre joueur:
    joueur = -joueur

# affichage final:
affiche(N)
if joueur == 1:
    print("PERDU (ordi a gagné) !")
else:
    print("GAGNE (ordi a perdu) !")
