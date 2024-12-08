import random

def initialisation(taille):
    """Crée une grille vide de la taille spécifiée."""
    return [[0 for _ in range(taille)] for _ in range(taille)]

def Grille(grille):
    """Affiche la grille dans un format lisible."""
    print("-" * (len(grille) * 4 + 1))
    for ligne in grille:
        print("|" + "|".join(f"{case:^3}" if case != 0 else "   " for case in ligne) + "|")
        print("-" * (len(grille) * 4 + 1))

def nv_tuile(grille):
    """Ajoute une nouvelle tuile (2 ou 4) dans une case vide."""
    cases_vides = [(i, j) for i in range(len(grille)) for j in range(len(grille[i])) if grille[i][j] == 0]
    if not cases_vides:
        return grille  # aucun espace vide, on ne peut rien ajouter

    i, j = random.choice(cases_vides)
    grille[i][j] = 4 if random.random() < 0.1 else 2  # 10% pour 4, 90% pour 2
    return grille

def mouvements():
    """Demande une direction au joueur."""
    directions = {'z': 'haut', 's': 'bas', 'q': 'gauche', 'd': 'droite'}
    while True:
        direction = input("Entrez une direction (z=haut, s=bas, q=gauche, d=droite) : ").lower()
        if direction in directions:
            return directions[direction]
        print("Entrée invalide. Veuillez réessayer.")

def decale_ligne(ligne):
    """Décale les tuiles vers la gauche en supprimant les zéros."""
    return [num for num in ligne if num != 0] + [0] * ligne.count(0)

def fusionner_ligne(ligne):
    """Fusionne les tuiles identiques."""
    compressée = decale_ligne(ligne)
    for i in range(len(compressée) - 1):
        if compressée[i] == compressée[i + 1] and compressée[i] != 0:
            compressée[i] *= 2
            compressée[i + 1] = 0
    return decale_ligne(compressée)

def deplacer_gauche(grille):
    """Déplace les tuiles vers la gauche."""
    return [fusionner_ligne(ligne) for ligne in grille]

def deplacer_droite(grille):
    """Déplace les tuiles vers la droite."""
    grille_inversée = [ligne[::-1] for ligne in grille]
    grille_déplacée = deplacer_gauche(grille_inversée)
    return [ligne[::-1] for ligne in grille_déplacée]

def transposer(grille):
    """Transpose la grille."""
    return [list(ligne) for ligne in zip(*grille)]

def deplacer_haut(grille):
    """Déplace les tuiles vers le haut."""
    transposée = transposer(grille)
    transposée_déplacée = deplacer_gauche(transposée)
    return transposer(transposée_déplacée)

def deplacer_bas(grille):
    """Déplace les tuiles vers le bas."""
    transposée = transposer(grille)
    transposée_déplacée = deplacer_droite(transposée)
    return transposer(transposée_déplacée)

def est_pleine(grille):
    """Vérifie si la grille est pleine."""
    for ligne in grille:
        for case in ligne:
            if case == 0:  # si une case est vide, la grille n'est pas pleine
                return False
    return True

def mouvement_possible(grille):
    """Vérifie si au moins un mouvement est possible."""
    taille = len(grille)

    # vérifier les cases vides (déplacement possible)
    for ligne in grille:
        if 0 in ligne:
            return True

    # vérifier les fusions possibles
    for i in range(taille):
        for j in range(taille):
            if i < taille - 1 and grille[i][j] == grille[i + 1][j]:  # Vérifier verticalement
                return True
            if j < taille - 1 and grille[i][j] == grille[i][j + 1]:  # Vérifier horizontalement
                return True

    return False

def dommage(grille):
    """Vérifie si le jeu est terminé."""
    if est_pleine(grille) and not mouvement_possible(grille):  # Grille pleine et aucun mouvement possible
        return True
    return False

def GG(grille):
    """Vérifie si une tuile atteint ou dépasse 2048."""
    for ligne in grille:
        for case in ligne:
            if case >= 2048:  # Vérifie si une case atteint ou dépasse 2048
                return True
    return False


ELEMENTS = {
    2: "H",
    4: "He",
    8: "Li",
    16: "Be",
    32: "B",
    64: "C",
    128: "N",
    256: "O",
    512: "F",
    1024: "Ne",
    2048: "Na"
}

def periode(grille):
    """Affiche la grille avec un thème périodique."""
    print("-" * (len(grille) * 5 + 1))
    for ligne in grille:
        print("|" + "|".join(f"{ELEMENTS.get(case, case):^4}" if case != 0 else "    " for case in ligne) + "|")
        print("-" * (len(grille) * 5 + 1))


if __name__ == "__main__":
    size = int(input("Entrez la taille de la grille : "))
    grille = initialisation(size)
    grille = nv_tuile(grille)
    grille = nv_tuile(grille)
    Grille(grille)

    while True:

        periode(grille)  # utiliser l'affichage avec le thème

        mouvement = mouvements()
        grille_originale = [ligne[:] for ligne in grille]  # copie pour vérifier si un mouvement est effectué

        if GG(grille):
            print("GG 😃! Vous avez atteint 2048 !")
            break

        if dommage(grille):
            print("Game Over 😔! vous avez perdu .")
            break

        if mouvement == "gauche":
            grille = deplacer_gauche(grille)
        elif mouvement == "droite":
            grille = deplacer_droite(grille)
        elif mouvement == "haut":
            grille = deplacer_haut(grille)
        elif mouvement == "bas":
            grille = deplacer_bas(grille)

        if grille != grille_originale:  # si la grille a changé après le mouvement
            grille = nv_tuile(grille)
        else:
            print("Déplacement invalide, essayez à nouveau.")

        periode(grille) # affiche du theme obligatoire

        Grille(grille) # interface de debug
        print("⬆⬆⬆⬆C'est juste une interface de débug pas prendre en cpte ⬆⬆⬆⬆.")

