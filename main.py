import graphviz as gv

alphabet = []
etats = []
etats_initiaux = []
etats_finaux = []
regles = []
les_regles = []

graphe = gv.Digraph()


def lecture_fichier():
    with open("automate.txt", 'r') as f:
        alphabet = f.readline().strip().split()
        etats = f.readline().strip().split(",")
        etats_initiaux = f.readline().strip().split()
        etats_finaux = f.readline().strip().split(",")
        regles = f.read().strip()
        segments = regles.split(',')
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


def afficher_automate():
    graphe.node('dummy', shape='point')
    for etat in etats:
        if etat in etats_initiaux:
            graphe.node(etat, shape='circle')
            graphe.edge('dummy', etat)
        elif etat in etats_finaux:
            graphe.node(etat, shape='doublecircle')
        else:
            graphe.node(etat, shape='circle')

    for regle in les_regles:
        origine, c, destination = regle
        graphe.edge(origine, destination, label=c)

    graphe.render('graph', view=True)


lecture_fichier()
afficher_automate()
