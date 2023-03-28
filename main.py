import graphviz as gv

alphabet = []
etats = []
etats_initiaux = []
etats_finaux = []
regles = []

les_regles = []

les_regles_complete = []

etat_initial_deterministe = []
etats_finaux_deterministe = []
les_regles_deterministe = []


# initialisation du graphe
graphe = gv.Digraph()

# initialisation du graphe complet
graphe_complet = gv.Digraph()

# initialisation du graphe deterministe
graphe_deterministe = gv.Digraph()


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


def afficher_regles(regles):
    for regle in regles:
        origine, c, destination = regle
        print(f"{origine} --{c}--> {destination}")


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


def afficher_automate(g, r):
    global etats, etats_initiaux, etats_finaux
    regles_doublons = r.copy()
    g.graph_attr['rankdir'] = 'LR'
    for etat in etats:
        if etat in etats_initiaux:
            g.node('Etat'+str(etat), shape='point')
            g.node(etat, shape='circle', style='bold')
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


def determiniser_automate():
    global alphabet, etats, etats_initiaux, etats_finaux, les_regles, les_regles_deterministe, etat_initial_deterministe, etats_finaux_deterministe
    if est_deterministe():
        print("L'automate est déjà déterministe.")
        les_regles_deterministe = les_regles_complete
        etat_initial_deterministe = etats_initiaux[0]
        etats_finaux_deterministe = etats_finaux
    else:
        pass


def accepter_mot(mot):
    global etats_initiaux, les_regles
    etat_courant = etats_initiaux[0]
    for lettre in mot:
        for regle in les_regles_deterministe:
            origine, c, destination = regle
            if origine == etat_courant and c == lettre:
                etat_courant = destination
                break
        else:
            return False
    if etat_courant in etats_finaux_deterministe:
        return True
    else:
        return False


lecture_fichier()
completer_automate()
afficher_regles(les_regles)
print("-------------------------")
afficher_regles(les_regles_complete)
afficher_automate(graphe, les_regles)
afficher_automate(graphe_complet, les_regles_complete)
determiniser_automate()
print("-------------------------")
afficher_regles(les_regles_deterministe)
afficher_automate(graphe_deterministe, les_regles_deterministe)
print(accepter_mot("aymen.kadri@"))
