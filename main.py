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
    global les_regles_complete, alphabet, etats, etats_initiaux, etats_finaux, les_regles_deterministe, etat_initial_deterministe, etats_finaux_deterministe
    if est_deterministe():
        print("L'automate est déjà déterministe.")
        etat_initial_deterministe = etats_initiaux
        etats_finaux_deterministe = etats_finaux
        les_regles_deterministe = les_regles
        return
    etat_initial_deterministe.append(etats_initiaux[0])
    etats_deterministes = [etat_initial_deterministe]
    for etats_deterministe in etats_deterministes:
        for lettre in alphabet:
            nouvel_etat = set()
            for etat in etats_deterministe:
                for regle in les_regles_complete:
                    origine, c, destination = regle
                    if origine == etat and c == lettre:
                        nouvel_etat.add(destination)
            if nouvel_etat:
                les_regles_deterministe.append(
                    [",".join(etats_deterministe), lettre, ",".join(sorted(nouvel_etat))])
                if sorted(nouvel_etat) not in etats_deterministes:
                    etats_deterministes.append(sorted(nouvel_etat))
    for etats_deterministe in etats_deterministes:
        if set(etats_deterministe) & set(etats_finaux):
            etats_finaux_deterministe.append(",".join(etats_deterministe))
    for etat in etats_deterministes:
        graphe_deterministe.node(",".join(etat), shape='circle')
    for regle in les_regles_deterministe:
        origine, c, destination = regle
        graphe_deterministe.edge(origine, destination, label=c)
    for etat_initial in etat_initial_deterministe:
        graphe_deterministe.node("Etat"+str(etat_initial),
                                 shape='point', style='bold')
        graphe_deterministe.edge(
            "Etat"+str(etat_initial), etat_initial_deterministe[0])
    for etat_final in etats_finaux_deterministe:
        graphe_deterministe.node(
            etat_final, shape='doublecircle', style='bold')
    afficher_automate(graphe_deterministe, les_regles_deterministe)


def accepter_mot(mot):
    global les_regles_deterministe, etat_initial_deterministe, etats_finaux_deterministe
    etat_courant = etats_initiaux[0]
    for lettre in mot:
        for origine, c, destination in les_regles:
            if origine == etat_courant and c == lettre:
                etat_courant = destination
                print("la lettre", lettre, "est acceptée")
                break
        else:
            print("la lettre", lettre, "n'est pas acceptée")
            return False
    return etat_courant in etats_finaux


lecture_fichier()
completer_automate()
# afficher_regles(les_regles)
print("-------------------------")
print(est_deterministe())

# afficher_regles(les_regles_complete)
#afficher_automate(graphe, les_regles)
afficher_automate(graphe_complet, les_regles_complete)
determiniser_automate()
print("-------------------------")
# afficher_regles(les_regles_deterministe)
afficher_automate(graphe_deterministe, les_regles_deterministe)
print(accepter_mot("a.k@lacatholille.fr"))
