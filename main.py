import os
import graphviz as gv


def creer_graphe():
    with open("automate.txt", 'r') as f:
        alphabet = f.readline().strip().split()
        etats = f.readline().strip().split()
        etats_initiaux = f.readline().strip().split()
        etats_finaux = f.readline().strip().split()
        regles = f.read().strip()
        segments = regles.split(',')
        les_regles = []
        for segment in segments:
            elements = segment.split('>')
            les_regles.append(elements)

    graphe = gv.Digraph()

    # Ajouter les états finaux en forme de double cercle
    # for etat in etats_finaux:
    #     graphe.node(etat, shape='doublecircle')

    # Afficher les états accessibles
    accessibles = set()
    accessibles.add(etats_initiaux[0])
    for regle in les_regles:
        origine, c, destination = regle
        if origine in accessibles:
            accessibles.add(destination)
    print(f"États accessibles : {accessibles}")

    # Afficher les états co-accessibles
    co_accessibles = set(etats_finaux)
    for regle in les_regles:
        origine, c, destination = regle
        if destination in co_accessibles:
            co_accessibles.add(origine)
    print(f"États co-accessibles : {co_accessibles}")

    # Ajouter les états
    # for etat in etats:
    #     if etat in etats_initiaux:
    #         graphe.node(etat, shape='circle')
    #         graphe.edge('dummy', etat)
    #     elif etat in etats_finaux:
    #         graphe.node(etat, shape='doublecircle')
    #     else:
    #         graphe.node(etat, shape='circle')

    for regle in les_regles:
        origine, c, destination = regle
        #graphe.edge(origine, destination, label=c)

    # Rendre le graphique
    graphe.render('graph', view=True)
    os.system('start graph.pdf')


creer_graphe()
