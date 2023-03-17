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
graphe.attr(rankdir='LR')

# initialisation du graphe complet
graphe_complet = gv.Digraph()
graphe_complet.attr(rankdir='LR')


def lecture_fichier():
    with open("automate.txt", 'r') as f:
        global alphabet, etats, etats_initiaux, etats_finaux, regles, les_regles
        alphabet = f.readline().strip().split(",")
        etats = f.readline().strip().split(",")
        etats_initiaux = f.readline().strip().split()
        etats_finaux = f.readline().strip().split(",")
        regles = f.read().strip()
        segments = regles.split(';')
        for segment in segments:
            elements = segment.split('>')
            les_regles.append(elements)


def etats_accessibles():
    accessibles = set()
    accessibles.add(etats_initiaux[0])
    for regle in les_regles:
        origine, c, destination = regle
        if origine in accessibles:
            accessibles.add(destination)
    print(f"États accessibles : {accessibles}")


def etats_co_accessibles():
    co_accessibles = set(etats_finaux)
    for regle in les_regles:
        origine, c, destination = regle
        if destination in co_accessibles:
            co_accessibles.add(origine)
    print(f"États co-accessibles : {co_accessibles}")


def afficher_automate(g, r):
    g.node('dummy', shape='point')
    for etat in etats:
        if etat in etats_initiaux:
            g.node(etat, shape='circle')
            g.edge('dummy', etat)
        elif etat in etats_finaux:
            g.node(etat, shape='doublecircle')
        else:
            g.node(etat, shape='circle')

    for regle in r:
        origine, c, destination = regle
        graphe.edge(origine, destination, label=c)
    graphe.render('graph', view=True)


def completer_automate():
    for regles in les_regles:
        for etat in etats:
            for lettre in alphabet:
                if regles[0] != etat & regles[1] != lettre:

    afficher_automate(graphe_complet, les_regles_complete)


lecture_fichier()
afficher_automate(graphe, les_regles)
