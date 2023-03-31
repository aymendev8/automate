import graphviz as gv
from collections import deque

# variables provenan du fichier automate.txt
alphabet = []
etats = []
etats_initiaux = []
etats_finaux = []
regles = []

# tableau contenant les regles de transition de base
les_regles = []

# tableau contenant les regles de transition complete
les_regles_complete = []

# initialisation du graphe
graphe = gv.Digraph()

# initialisation du graphe complet
graphe_complet = gv.Digraph()

# initialisation du graphe deterministe
graphe_deterministe = gv.Digraph()


# lecture du fichier et remplissage des variables globales
def lecture_fichier():
    global alphabet, etats, etats_initiaux, etats_finaux, regles, les_regles
    with open("automate.txt", 'r') as f:
        alphabet = f.readline().strip().split(",")
        etats = f.readline().strip().split(",")
        etats_initiaux = f.readline().strip().split(",")
        etats_finaux = f.readline().strip().split(",")
        regles = f.read().strip()
    segments = regles.split(';')
    for segment in segments:
        elements = segment.split('>')
        les_regles.append(elements)


def etats_accessibles():
    global les_regles
    accessibles = set()
    accessibles.add(etats_initiaux[0])
    for regle in les_regles:
        origine, c, destination = regle
        if origine in accessibles:
            accessibles.add(destination)
    print(f"États accessibles : {accessibles}")


def etats_co_accessibles():
    global les_regles
    co_accessibles = set(etats_finaux)
    for regle in les_regles:
        origine, c, destination = regle
        if destination in co_accessibles:
            co_accessibles.add(origine)
    print(f"États co-accessibles : {co_accessibles}")


# affiche un automate, avec en parametre le graphe a afficher et les regles de transition
def afficher_automate(g, r):
    global etats, etats_initiaux, etats_finaux
    regles_doublons = r.copy()
    g.graph_attr['rankdir'] = 'LR'
    for etat in etats:
        if etat in etats_initiaux:
            if etat in etats_finaux:
                g.node(etat, shape='doublecircle', style='bold')
                g.node('Etat'+str(etat), shape='point')
            else:
                g.node(etat, shape='circle', style='bold')
                g.node('Etat'+str(etat), shape='point')
            g.edge('Etat'+str(etat), etat)
        elif etat in etats_finaux:
            g.node(etat, shape='doublecircle', style='bold')
        else:
            g.node(etat, shape='circle')
    for i, regle in enumerate(regles_doublons):
        compteur = 0
        lettres = ""
        origine, c, destination = regle
        for regle2 in regles_doublons[i:]:
            origine2, c2, destination2 = regle2
            if origine2 == origine and destination2 == destination and c2 != c:
                lettres += str(regle2[1]) + ","
                regles_doublons.remove(regle2)
                compteur += 1
        if compteur == 0:
            g.edge(origine, destination, label=c)
        else:
            if lettres[len(lettres)-1] == ",":
                lettres = lettres[:len(lettres)-1]
            g.edge(origine, destination, label=c +
                   ","+lettres, constraint='false')
    if g == graphe:
        g.render('graphe', view=True)
    elif g == graphe_complet:
        g.render('graphe_complet', view=True)
    elif g == graphe_deterministe:
        g.render('graphe_deterministe', view=True)


def automate_initial():
    lecture_fichier()
    afficher_automate(graphe, les_regles)

# completer l'automate en creant un nouveau tableau de regles appeler les_regles_complete


def completer_automate():
    global les_regles_complete, les_regles, alphabet, etats
    for regle in les_regles:
        les_regles_complete.append(regle)
    for etat in etats:
        for lettre in alphabet:
            for regle in les_regles:
                origine, c, destination = regle
                if origine == etat and lettre == c:
                    break
            else:
                les_regles_complete.append([etat, lettre, "p"])
    afficher_automate(graphe_complet, les_regles_complete)

# verifie si l'automate est deterministe


def est_deterministe():
    global les_regles, alphabet, etats
    if len(etats_initiaux) > 1:
        return False
    for etat in etats:
        for lettre in alphabet:
            compteur = 0
            for regle in les_regles:
                origine, c, destination = regle
                if origine == etat and lettre == c:
                    compteur += 1
            if compteur > 1:
                print(
                    f"État {etat} et lettre {lettre} : {compteur} transitions")
                return False
    return True

# determinise l'automate en modifiant les_regles par des regles deterministes


def determiniser_automate():
    global les_regles, alphabet, etats, etats_initiaux, etats_finaux, graphe_deterministe
    if not est_deterministe():
        print("L'automate n'est pas déterministe")
        nouveaux_etats = set()
        etats_a_traiter = deque()  # on utilise une file pour traiter les états dans l'ordre
        etats_a_traiter.append(tuple(etats_initiaux))
        nouveaux_etats.add(tuple(etats_initiaux))

        nouvelles_regles = []

        while etats_a_traiter:
            etat_courant = etats_a_traiter.popleft()
            for lettre in alphabet:
                etats_accessibles = set()
                for etat in etat_courant:
                    for regle in les_regles:
                        origine, c, destination = regle
                        if origine == etat and c == lettre:
                            etats_accessibles.add(destination)

                if etats_accessibles and tuple(etats_accessibles) not in nouveaux_etats:
                    etats_a_traiter.append(tuple(etats_accessibles))
                    nouveaux_etats.add(tuple(etats_accessibles))

                if etats_accessibles:
                    nouvelles_regles.append(
                        [etat_courant, lettre, tuple(etats_accessibles)])

        etats = [','.join(sorted(list(etat))) for etat in nouveaux_etats]
        etats_initiaux = [','.join(sorted(list(tuple(etats_initiaux))))]
        etats_finaux = [etat for etat in etats if any(
            e in etat.split(',') for e in etats_finaux)]
        les_regles = [[','.join(sorted(list(origine))), lettre, ','.join(sorted(
            list(destination)))] for origine, lettre, destination in nouvelles_regles]
    afficher_automate(graphe_deterministe, les_regles)

# verifie si l'automate accepte un mot donne


def accepter_mot(mot):
    global les_regles, etats_initiaux, etats_finaux
    etat_courant = etats_initiaux[0]
    for lettre in mot:
        for origine, c, destination in les_regles:
            if origine == etat_courant and c == lettre:
                etat_courant = destination
                #print("la lettre", lettre, "est acceptée") <--- debug
                break
        else:
            #print("la lettre", lettre, "n'est pas acceptée") <--- debug
            return False
    return etat_courant in etats_finaux


# verifie si l'automate accepte un mot (avec @lacatholille.fr)
def accepter_mot_lacatho(mot):
    global les_regles, etats_initiaux, etats_finaux
    etat_courant = etats_initiaux[0]
    lemot = mot.split("@", 1)
    for lettre in lemot[0]:
        for origine, c, destination in les_regles:
            if origine == etat_courant and c == lettre:
                etat_courant = destination
                break
        else:
            return False
    if lemot[1] == "lacatholille.fr":
        etat_courant = etats_finaux[len(etats_finaux)-1]
        return etat_courant in etats_finaux
    else:
        return False


automate_initial()  # lis le fichier et affiche l'automate
completer_automate()  # completer l'automate et affiche l'automate complet
determiniser_automate()  # determiniser l'automate et affiche l'automate deterministe
# print(accepter_mot("aaabd")) #verifie si le mot est accepté par l'automate


# verifie si le mot est accepté par l'automate ( unique pour les mail @lacatholille.fr)
print(accepter_mot_lacatho("aymen.kadri8@lacatholille.fr"))
