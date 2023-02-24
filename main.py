import graphviz as gv

alphabet = []
etats = []
etats_initiaux = []
etats_finaux = []
transitions = []


def lire_fichier():
    with open("automate.txt", "r") as f:
        alphabet = f.readline().split()
        etats = f.readline().split()
        etats_initiaux = f.readline().split()
        etats_finaux = f.readline().split()
        for line in f:
            transitions.append(line.split())
    # debug
    print(alphabet)
    print(etats)
    print(etats_initiaux)
    print(etats_finaux)
    print(transitions)


def creer_graph():
    dot = gv.Digraph(comment='The Round Table')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')
    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')
    dot.render('test-output/round-table.gv', view=True)


creer_graph()
