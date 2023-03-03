import graphviz as gv
import os

alphabet = []
states = []
initial_states = []
final_states = []
rules = []


def create_graph():
    with open("automate.txt", 'r') as f:
        alphabet = f.readline().strip().split()
        states = f.readline().strip().split()
        initial_states = f.readline().strip().split()
        final_states = f.readline().strip().split()
        rules = f.readline().strip()
    # Créer un objet graphique
    graph = gv.Digraph()
    graph.node('dummy', style='invisible')

    # Ajouter les états
    for state in states:
        if state in initial_states:
            graph.node(state, shape='circle')
            graph.edge('dummy', state)
        elif state in final_states:
            graph.node(state, shape='doublecircle')
        else:
            graph.node(state)

    # Ajouter les règles
    rule_parts = rules.split('>')
    start_state = rule_parts[0].strip()
    end_state = rule_parts[-1].strip()
    symbol = rule_parts[1].strip()
    graph.edge(start_state, end_state, label=symbol)

    # Rendre le graphique
    graph.render('graph', view=True)
    os.system('start graph.pdf')


create_graph()
