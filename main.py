import graphviz as gv

alphabet = []
etats = []
etats_initiaux = []
etats_finaux = []
regles = []
les_regles = []
les_regles_complete = []

# initialisation du graphe
graphe = gv.Digraph()

# initialisation du graphe complet
graphe_complet = gv.Digraph()

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
        origine , c, destination = regle
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
    g.node('dummy', shape='point')
    for etat in etats:
        if etat in etats_initiaux:
            g.node(etat, shape='circle', style='bold')
            g.edge('dummy', etat)
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
            if origine2 == origine and destination2 == destination and  c2 != c:
                lettres += str(regle2[1])
                lettres += ","
                regles_doublons.remove(regle2)
                compteur += 1
        if compteur == 0:
            g.edge(origine, destination, label=c)
        else:
            if lettres[len(lettres)-1] == ",":
                lettres = lettres[:len(lettres)-1]
            g.edge(origine, destination, label=c+","+lettres, constraint='false')
    if g == graphe:
        g.render('graphe', view=True)
    else:
        g.render('graphe_complet', view=True)

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

lecture_fichier()
completer_automate()
afficher_regles(les_regles)
print("-------------------------")
afficher_regles(les_regles_complete)
afficher_automate(graphe, les_regles)
afficher_automate(graphe_complet, les_regles_complete)