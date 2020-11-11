# Jeu de cartes appelé "Pouilleux"

# L'ordinateur est le donneur des cartes.

# Une carte est une chaine de 2 caractères.
# Le premier caractère représente une valeur et le deuxième une couleur.
# Les valeurs sont des caractères comme '2','3','4','5','6','7','8','9','10','J','Q','K', et 'A'.
# Les couleurs sont des caractères comme : ♠, ♡, ♣, et ♢.
# On utilise 4 symboles Unicode pour représenter les 4 couleurs: pique, coeur, trèfle et carreau.
# Pour les cartes de 10 on utilise 3 caractères, parce que la valeur '10' utilise deux caractères.

import random


def compare(string, list):
    compteur = 0
    j = 0
    temp = []
    while j < len(list):
        if list[j] == string:
            compteur = compteur + 1
            temp.append(j)
        j = j + 1
    if compteur % 2 != 0:
        del temp[len(temp) - 1]
        return temp
    else:
        return temp


def attend_le_joueur():
    '''()->None
    Pause le programme jusqu'au l'usager appui Enter
    '''
    try:
        input("Appuyez Enter pour continuer. ")
    except SyntaxError:
        pass


def prepare_paquet():
    '''()->list of str
        Retourne une liste des chaines de caractères qui représente tous les cartes,
        sauf le valet noir.
    '''
    paquet = []
    couleurs = ['\u2660', '\u2661', '\u2662', '\u2663']
    valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for val in valeurs:
        for couleur in couleurs:
            paquet.append(val + couleur)
    paquet.remove('J\u2663')  # élimine le valet noir (le valet de trèfle)
    return paquet


def melange_paquet(p):
    '''(list of str)->None
       Melange la liste des chaines des caractères qui représente le paquet des cartes
    '''
    random.shuffle(p)


def donne_cartes(p):
    '''(list of str)-> tuple of (list of str,list of str)

    Retournes deux listes qui représentent les deux mains des cartes.
    Le donneur donne une carte à l'autre joueur, une à lui-même,
    et ça continue jusqu'à la fin du paquet p.
    '''
    i = 1
    donneur = []
    autre = []
    for x in p:
        if (i % 2 == 0):
            donneur.append(x)
        elif (i % 2 != 0):
            autre.append(x)
        i = i + 1

    return (donneur, autre)


def elimine_paires(l):
    '''
     (list of str)->list of str

     Retourne une copy de la liste l avec tous les paires éliminées
     et mélange les éléments qui restent.

     Test:
     (Notez que l’ordre des éléments dans le résultat pourrait être différent)
    '''

    suits = []
    resultat = []
    i = 0
    while i < len(l):
        if '\u2660' in l[i]:
            l[i] = l[i].strip('\u2660')
            suits.append('\u2660')
        elif '\u2661' in l[i]:
            l[i] = l[i].strip('\u2661')
            suits.append('\u2661')
        elif '\u2662' in l[i]:
            l[i] = l[i].strip('\u2662')
            suits.append('\u2662')
        elif '\u2663' in l[i]:
            l[i] = l[i].strip('\u2663')
            suits.append('\u2663')
        i = i + 1
    i = 0
    index = []
    while i < len(l):
        a = l[i]
        index = index + compare(a, l)
        i = i + 1
    index = list(dict.fromkeys(index))
    index.sort()
    i = len(index) - 1
    while i >= 0:
        del suits[index[i]]
        del l[index[i]]
        i = i - 1

    i = 0
    while i < len(l):
        resultat.append(l[i] + suits[i])
        i = i + 1

    random.shuffle(resultat)
    return resultat


def affiche_cartes(p):
    '''
    (list)-None
    Affiche les éléments de la liste p séparées par d'espaces
    '''
    for x in p:
        if (x == p[len(p) - 1]):
            print(x)
        else:
            print(x, end=" ")


def entrez_position_valide(n):
    '''
    (int)->int
    Retourne un entier du clavier, de 1 à n (1 et n inclus).
    Continue à demander si l'usager entre un entier qui n'est pas dans l'intervalle [1,n]

    Précondition: n>=1
    '''
    choix = int(input("SVP entrez un entier de 1 a {}".format(n)))
    while choix > n or choix < 1:
        choix = int(input("Vous devez absolument entrez un entier de 1 a {}".format(n)))
    print("Vous avez demandez ma ", choix, "eme carte")
    return choix


def robotParle(list):
    n = len(list)
    print("J'ai", n, "cartes. Si 1 est la position de ma premiere carte et", n,
          "la postion de ma derniere carte, laquelle de mes cartes voulez-vous?")
    choix = entrez_position_valide(n)
    return choix


def ajouteCarte(list1, list2, choix):
    a = list2[choix - 1]
    list1.append(a)
    print("La voila. Cest un ", a)
    print("Avec ", a, "ajoute, votre main est:")
    affiche_cartes(list1)
    return list1


def randomNumber(n):
    n = random.randint(1, n)
    return n


def joue():
    '''()->None
    Cette fonction joue le jeu'''

    p = prepare_paquet()
    melange_paquet(p)
    tmp = donne_cartes(p)
    donneur = tmp[0]
    humain = tmp[1]

    print("Bonjour. Je m'appelle Robot et je distribue les cartes.")
    print("Votre main est:")
    affiche_cartes(humain)
    print("Ne vous inquiétez pas, je ne peux pas voir vos cartes ni leur ordre.")
    print("Maintenant défaussez toutes les paires de votre main. Je vais le faire moi aussi.")
    attend_le_joueur()

    donneur = elimine_paires(donneur)
    humain = elimine_paires(humain)
    while (len(humain) > 0) and (len(donneur) > 0):
        print("***************************************")
        print("Votre tour.")
        print("Votre main est:")
        affiche_cartes(humain)
        choix = robotParle(donneur)
        humain = ajouteCarte(humain, donneur, choix)
        del donneur[choix - 1]
        if (len(donneur) == 0):
            break
        print("Après avoir défaussé toutes les paires et mélangé les cartes, votre main est:")
        humain = elimine_paires(humain)
        affiche_cartes(humain)
        attend_le_joueur()
        print("***************************************")
        print("Mon tour")
        n = randomNumber(len(humain))
        print("Jai pris votre ", n, " eme carte")
        a = humain[n - 1]
        donneur.append(a)
        del humain[n - 1]
        donneur = elimine_paires(donneur)
        attend_le_joueur()
    if len(humain) == 0:
        print("***************************************")
        print("J'ai terminé toutes les cartes.")
        print("Félicitations! Vous, Humain, vous avez gagné.")
    elif len(donneur) == 0:
        print("***************************************")
        print("J'ai terminé toutes les cartes.")
        print("Vous avez perdu! Moi, Robot, j'ai gagné.")


# programme principale
joue()

