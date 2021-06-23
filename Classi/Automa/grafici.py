from graphviz import Digraph


def stampa_automa(automa):
    f = Digraph('finite_state_machine', filename='nome file', format='png')

    for s in automa.stati:
        f.node(s.nome, shape='circle')

    for state in fsm.final_states:
        if state != "":
            f.node(state, shape='doublecircle')

    for edge_fsm in fsm.edges:
        f.edge(edge_fsm.source, edge_fsm.destination, edge_fsm.label)

    f.render(directory="Output/" + filename + "/FSM_graph")

    summary = open("Output/" + filename + "/FSM_graph/" + fsm.name + "_summary.txt", "w")
    summary.write("Numero di stati:" + str(len(fsm.states)) + "\n")
    i = 1
    for state in fsm.states:
        summary.write(str(i) + ") " + str(state) + "\n")
        i = i + 1
    summary.write("Numero di transizioni:" + str(len(fsm.edges)) + "\n")
    i = 1
    for e in fsm.edges:
        summary.write(str(i) + ") " + str(e.source) + " -> " + e.label + " -> " + e.destination + "\n")
        i = i + 1
    summary.close()